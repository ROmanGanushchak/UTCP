#include <thread>
#include <stdexcept>
#include <cassert>
#include <queue>
#include <iostream>
#include "crc.h"
#include "connector.h"
#include "types.h"
#include "fileFragment.h"
#include "windows.h"

using namespace std;

char* stringToAlloc(string text) {
    char* data = (char*) malloc (text.size()+1);
    memcpy(data, text.data(), text.size());
    data[text.size()] = '\0';
    return data;
}

Connector::Connector(string ip, u16 port) : queue(1), toSend(2),
    sock(queue, ip, port), 
    received(128), sent(128),
    isWorking(false),
    isKeepAliveWarning(false),
    currentDef(nullptr),
    lostCnt(0)
{
    nextSeq = 1;
    sock.startReading();
};

void Connector::start() {
    isWorking = true;
    while (isWorking) {
        auto nowFullTime = std::chrono::system_clock::now();
        now = std::chrono::duration_cast<std::chrono::milliseconds>(nowFullTime.time_since_epoch()).count();

        while (timers.size() && timers.front().endTime < now) {
            TimerUnit timer = timers.front();
            timers.pop_front();
            auto [elem, status] = sent.get(timer.seq);
            assert(status == States::Active && "The value is present in timer but was deleted from SentQueue");
            
            toResend.push_back(elem->segment);
            sent.changeState(elem->segment->seq, States::Suppresed);
            assert(sent.get(elem->segment->seq).second == States::Suppresed);
            printf("The message with seq: %d was resended\n", elem->segment->seq);
        }

        vector<DataSegment*> packets;
        bool isReceivedMessage = !queue.isEmpty();
        for (int i=0; i<3 && !queue.isEmpty(); i++) {
            DataSegment* segment = queue.front();
            queue.pop();
            if (segment->crc != 0) {
                if (segment->isNextFragment || segment->type == DataTypes::PureData) 
                    lostCnt++;
                if (segment->type != DataTypes::KeepAlive) {
                    segment->type = DataTypes::Resend;
                    initCrc(segment);
                    sock.sendSegment(segment);
                }
                printf("The fragment seq: %d, type: %d was received with an error\n", segment->seq, segment->type);
                free(segment);
                continue;
            }
            sent.setWindow(segment->window);
            printf("Fragment received: seq: %d, type: %d, size: %hu, isNext: %d, first: %d\n", segment->seq, segment->type, segment->dataLength, segment->isNextFragment, received.getFirst());
            if (sysMessageHandler(segment)) {
                if ((segment->seq != 0 && segment->type != DataTypes::ACK) || segment->type == DataTypes::EndConnection)
                    sendAck(segment->seq);
                free(segment);
                continue;
            }
            if (segment->seq < received.getFirst()) {
                if (segment->type != DataTypes::ACK)
                    sendAck(segment->seq);
                free(segment);
                continue;
            }

            auto [isAdded, fragments] = received.add(segment);
            if (!isAdded) break;
            sendAck(segment->seq);
            for (auto fragment : fragments) {
                // if (fragment->type != DataTypes::PureData && !fragment->isNextFragment && fragment->type != DataTypes::File) {
                //     packets.push_back(fragment);
                //     continue;
                // }
                if (fragment->type != DataTypes::PureData) {
                    if (fragment->type == DataTypes::File)
                        currentDef = new FileDefragmentator();
                    else 
                        currentDef = new Defragmentator();
                }
                auto [isFinished, packet] = currentDef->addNextFrag(fragment);
                if (packet != fragment) free(fragment);
                if (!isFinished) continue;
                if (packet != NULL) packets.push_back(packet);
                auto [datasize, overhead] = currentDef->getOverhead();
                printf("For received message overhead: %llu, datasize: %llu the percent of useful data: %lf\n", 
                        overhead, datasize, (datasize*100) / (double)(overhead+datasize));
                delete currentDef;
                currentDef = nullptr;

                printf("The fragments in the packet lost: %d\n", lostCnt);
                lostCnt++;
            }
        }

        for (auto packet : packets) {
            dprintf("Received packet with seq: %d, type: %d\n", packet->seq, packet->type);
            switch (packet->type) {
            case DataTypes::String: {
                printf("%.*s\n", packet->dataLength, (char*)packet->getExtraData());
                break;
            }
            default:
                printf("The packet with unsuportable default handler was called\n");
            }
            free(packet);
        }

        // keep-alive
        if (sock.getIsConfigured()) {
            if (isReceivedMessage) {
                lastReception = now;
                if (isKeepAliveWarning) {
                    printf("The other side is back\n");
                    isKeepAliveWarning = false;
                }
            }
            if (now - lastReception > 5000 && now - lastSendedKeepAlive > 5000) 
                sendKeepAlive();
            if (!isKeepAliveWarning && now - lastReception > 20000) {
                printf("The other side doesnt correspond to sended messages\nIf u with to quit the connection write 'quit' command\n");
                isKeepAliveWarning = true;
            }
        }

        u16 maxSent = 7 * !isKeepAliveWarning;
        for (; maxSent>0 && !toResend.empty(); maxSent--) {
            DataSegment* seg = toResend.front();
            toResend.pop_front();
            AddingStates state = trySendFragment(seg);
            if (!(state == Added || state == Incorrect))
                toResend.push_back(seg);
            if (state == NoSize || state == Incorrect) 
                maxSent = 1;
        }
        FragmentatorI* toPush = nullptr;
        while (maxSent > 0 && !toSend.isEmpty()) {
            FragmentatorI* fr = toSend.front();
            assert(fr != nullptr && "WTF how fr can be NULLLL");
            for (; maxSent>0 && !fr->isFinished(); maxSent--) {
                DataSegment* seg = fr->getNextFragment(maxDataSize);
                if (seg == NULL) {printf("Received seg is NULL\n"); break;}
                AddingStates state = trySendFragment(seg);
                if (state == Added) continue;
                if (state == Incorrect) {printf("Trying to add incorrect segment\n"); continue;}
                toPush = new NoFragmentator(seg);
                maxSent = 0;
                break;
            }
            if (fr && fr->isFinished()) {
                auto [datasize, overhead] = fr->getOverheads();
                if (!(datasize == INT_MAX && overhead == INT_MAX)) {
                    printf("For the sent message overhead: %llu, datasize: %llu the percent of useful data: %lf\n", 
                        overhead, datasize, (datasize*100) / (double)(overhead+datasize));
                }
                delete fr;
                toSend.pop();
            } else break;
        }
        if (toPush) toSend.pushFront(toPush);
    }
}

AddingStates Connector::trySendFragment(DataSegment *seg) {
    auto [descriptor, state] = (seg->seq == 0) ? make_pair(nullptr, States::Empty) : sent.get(seg->seq);
    printf("Received toSend seq: %d, state: %hhu, type: %d, isNext: %d\n", seg->seq, state, seg->type, seg->isNextFragment);
    if (state == States::Deleted) return AddingStates::Incorrect;
    if (state == States::Suppresed) {
        AddingStates _state = sent.changeState(seg->seq, States::Active);
        if (_state != AddingStates::Added) return _state;
    } else if (state == States::Empty) {
        seg->seq = nextSeq;
        auto [_state, _descp] = sent.add((DataSegmentDescriptor){.segment=seg, .sentCount=0});
        if (_state != AddingStates::Added) return _state;
        nextSeq++;
        seg->window = received.getWindow();
        initCrc(seg);
        descriptor = _descp;
    } else return AddingStates::Incorrect;
    timers.push_back((TimerUnit){.seq=seg->seq, .endTime=now + timeToMiss});
    descriptor->timer = std::prev(timers.end());
    sock.sendSegment(seg);
    return AddingStates::Added;
}

bool Connector::sysMessageHandler(DataSegment* seg) {
    switch(seg->type) {
    case DataTypes::ACK: {
        auto [elem, status] = sent.get(seg->seq);
        if (status == States::Active) {
            // printf("Received ACK seq: %d\n", elem->segment->seq);
            assert(elem->segment->seq == seg->seq && "Returned seq doesnt match\n");
            timers.erase(elem->timer);
            sent.markAsProcessed(seg->seq, true);
            assert(sent.get(seg->seq).second != States::Active && "The element was not deleted from the sent\n");
        }
        return true;
    }
    case DataTypes::KeepAlive: {
        DataSegment _seg = (DataSegment){.dataLength=0, .seq=0, .type=DataTypes::UnKnown, .isNextFragment=false};
        initCrc(&_seg);
        sock.sendSegment(&_seg);
        return true;
    }
    case DataTypes::Resend: {
        auto seq = seg->seq;
        auto [descp, state] = sent.get(seq);
        if (state != States::Active && state != States::Suppresed) return false;
        sock.sendSegment(descp->segment);
        return true;
    }
    // sendNextWithErr
    // send D:/failed.txt
    case DataTypes::Connection: {
        if (sock.getIsConfigured()) {
            printf("Trying to connect while last connection is still active\n");
            return true;
        }
        ReceivedConnectionData *data = reinterpret_cast<ReceivedConnectionData*>(seg->getExtraData());
        dprintf("Got data to connect ip: %s, port: %d\n", connection.tIp.c_str(), connection.tPort);
        received.iniq(seg->seq+1);
        timers.clear();
        sendConnectionMessage(data->ip, data->port, DataTypes::ConnectionApproval, true);
        lastReception = now;
        lastSendedKeepAlive = now;
        return true;
    }
    case DataTypes::ConnectionApproval: {
        ReceivedConnectionData *data = reinterpret_cast<ReceivedConnectionData*>(seg->getExtraData());
        auto [ip, port] = sock.getSenderData();
        if (data->ip != ip || data->port != port) {
            printf("The connection approval receined for incorrect ip address or port");
            return true;
        }
        received.iniq(seg->seq+1);
        sock.confirmConfiguration();
        timers.clear();
        lastReception = now;
        lastSendedKeepAlive = now;
        return true;
    }
    case DataTypes::EndConnection: {
        printf("The other side decided to end the connection\n");
        quit(false);
        return true;
    }
    case DataTypes::UnKnown: 
        return true;
    }
    return false;
}

void Connector::sendConnectionMessage(string ip, u16 port, DataTypes type, bool isConfirmed) {
    sock.configure(ip, port, (isConfirmed) ? Active : ConfirmAwait);
    DataSegment *seg = (DataSegment*) malloc(sizeof(DataSegment));
    *seg = {.dataLength=0, .seq=0, .type=type, .isNextFragment=false};
    printf("Connection message seq: %d\n", seg->seq);
    toSend.push(new NoFragmentator(seg));
}

void Connector::sendAck(u16 seq) {
    DataSegment seg = (DataSegment){.dataLength=0, .seq=seq, .type=DataTypes::ACK, .isNextFragment=false};
    seg.window = received.getWindow();
    initCrc(&seg);
    sock.sendSegment(&seg);
}

void Connector::sendKeepAlive() {
    DataSegment keep = (DataSegment){.dataLength=0, .seq=0, .type=DataTypes::KeepAlive, .isNextFragment=false};
    keep.window = received.getWindow();
    initCrc(&keep);
    sock.sendSegment(&keep);
    lastSendedKeepAlive = now;
}

void Connector::sendAck(u16 seq, string ip, u16 port) {
    DataSegment seg = (DataSegment){.dataLength=0, .seq=seq, .type=DataTypes::ACK, .isNextFragment=false};
    initCrc(&seg);
    sock.sendSegmentCust(&seg, ip, port);
}

void Connector::connect(string ip, u16 port) {
    if (sock.getIsConfigured()) {
        printf("Curently the device is connected or tryes to connect, end the connection first to connect to other device\n");
        return;
    }
    sendConnectionMessage(ip, port, DataTypes::Connection, false);
}

void Connector::finish() {
    this->quit(true);
    this->isWorking = false;
}

pair<bool, string> Connector::setMaxFragmentSize(u16 size) {
    if (size <= 0 || size + sizeof(DataSegment) > 1452) 
        return {true, "The provided value has to be in the range of 1 to 1452-sizeof(DataSegment){probably 11}"}; // 1500-sizeof(DataSegment)
    this->maxDataSize = size;
    return {false, ""};
}

void Connector::quit(bool conf) {
    if (!sock.getIsConfigured()) return;
    printf("The quit was executed\n");
    if (conf) {
        DataSegment _seg = (DataSegment){.dataLength=0, .seq=0, .type=DataTypes::EndConnection, .isNextFragment=false};
        initCrc(&_seg);
        sock.sendSegment(&_seg);
    }
    sock.configure("", 0, SenderStates::InActive);
    vector<DataSegmentDescriptor> sended = sent.iniq(0);
    for (auto elem : sended) {
        free(elem.segment);
        timers.erase(elem.timer);
    }
    vector<DataSegment*> _received = received.iniq(0);
    for (auto elem : _received) free(elem);
    timers.clear();
}

void Connector::setError(u16 coef) { 
    sock.setError(coef);
    printf("The error chance is set to 1 / %d\n", coef);
}

void Connector::sendNextWithErr() {
    sock.sendNextWithErr();
}