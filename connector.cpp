#include <thread>
#include <stdexcept>
#include <cassert>
#include <queue>
#include <iostream>
#include "windows.h"
#include "crc.h"
#include "connector.h"
#include "types.h"
#include "fileFragment.h"

using namespace std;

Connector::Connector(string ip, u16 port) : queue(1), toSend(2),
    sock(queue, ip, port), sent(128), 
    isWorking(false),
    isKeepAliveWarning(false)
{
    leastAck = -1;
    nextSeq = 0;
    sock.startReading();
};

void Connector::start() {
    isWorking = true;
    while (isWorking) {
        // if (!timers.size() && sent.empty() && queue.isEmpty() && toSend.isEmpty()) continue;
        auto nowFullTime = std::chrono::system_clock::now();
        auto now = std::chrono::duration_cast<std::chrono::milliseconds>(nowFullTime.time_since_epoch()).count();

        while (timers.size() && timers.front().endTime < now) {
            TimerUnit timer = timers.front();
            auto [elem, status] = sent.get(timer.seq);
            assert(status == ReturnCodes::Success && "The value is present in timer but was deleted from SentQueue");

            if (elem->sentCount == maxSentCount) {
                printf("The message with seq: %d was sent to many times and is considered gone\n", elem->segment->seq);
                sent.markAsProcessed(elem->segment->seq, true);
                timers.pop_front();
                break;
            } else {
                sock.sendSegment(elem->segment);
                elem->sentCount++;
                timers.pop_front();
                timers.push_back((TimerUnit){.seq=timer.seq, .endTime=now + timeToMiss});
            }
        }

        vector<DataSegment*> packets;
        bool isReceivedMessage = !queue.isEmpty();
        while (!queue.isEmpty()) {
            DataSegment* segment = queue.front();
            queue.pop();
            sent.setWindow(segment->window);
            dprintf("Fragment received: type: %d, seq: %d\n", segment->type, segment->seq);
            if (sysMessageHandler(segment, now)) {
                free(segment);
                continue;
            }

            auto [isAdded, fragments] = received.add(segment);
            if (!isAdded) break;
            sendAck(segment->seq);
            dprintf("Added fragments %d, received fragments:\n", segment->seq);
            for (auto fragment : fragments) {
                printf("Fragment from received: %d\n", fragment->seq);
                if (fragment->type != DataTypes::PureData && !fragment->isNextFragment && fragment->type != DataTypes::File) {
                    packets.push_back(fragment);
                    continue;
                }
                if (fragment->type != DataTypes::PureData) {
                    if (fragment->type == DataTypes::File)
                        currentDef = new FileDefragmentator();
                    else 
                        currentDef = new Defragmentator();
                }
                auto [isFinished, packet] = currentDef->addNextFrag(fragment);
                if (!isFinished) continue;
                if (packet != NULL) packets.push_back(packet); 
                delete currentDef;
                currentDef = NULL;
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
        // if (sock.getIsConfigured()) {
        //     if (isReceivedMessage) {
        //         lastReception = now;
        //         if (isKeepAliveWarning) {
        //             printf("The other side is back\n");
        //             isKeepAliveWarning = false;
        //         }
        //     }
        //     if (now - lastReception > 5000 && now - lastSendedKeepAlive > 5000) 
        //         sendKeepAlive(now);
        //     if (!isKeepAliveWarning && now - lastReception > 50000) {
        //         printf("The other side doesnt correspond to sended messages\nIf u with to quit the connection write 'quit' command\n");
        //         isKeepAliveWarning = true;
        //     }
        // }

        if (!sent.getWindow() && now - lastSendedKeepAlive > 150)
            sendKeepAlive(now);
        while (!toSend.isEmpty() && sent.getWindow()) {
            FragmentatorI* fr = toSend.front();
            dprintf("Received frame %hu\n", fr->fragmentSize);
            dprintf("Size: %d IsActivated: %d\n", fr->fragmentSize, fr->isActivated());

            while (sent.getWindow() - sizeof(DataSegment) > 0 && !fr->isFinished()) {
                DataSegment* segment = fr->getNextFragment(_min(maxDataSize, sent.getWindow() - sizeof(DataSegment)));
                if (segment == NULL) break;
                segment->seq = nextSeq;
                dprintf("Adding element with seq: %d\n", segment->seq);
                auto descriptor = sent.add((DataSegmentDescriptor){.segment=segment, .sentCount=0});
                if (descriptor) {
                    nextSeq++;
                    descriptor->segment->window = received.getWindow();
                    initCrc(descriptor->segment);
                    timers.push_back((TimerUnit){.seq=segment->seq, .endTime=now + timeToMiss});
                    descriptor->timer = --timers.end();
                    sock.sendSegment(descriptor->segment);
                    Sleep(200);
                    // sleep(0.2);
                } else {
                    toSend.pushFront(new NoFragmentator(segment));
                    printf("Critical error, the element was not added\nTrying to add seq: %d\n", segment->seq);
                    break;
                }
            }
            if (fr && fr->isFinished()) {
                delete fr;
                toSend.pop();
            } else break;
        }
    }
}

bool Connector::sysMessageHandler(DataSegment* seg, u64 now) {
    switch(seg->type) {
    case DataTypes::ACK: {
        auto [elem, status] = sent.get(seg->seq);
        if (status == ReturnCodes::Success) {
            timers.erase(elem->timer);
            sent.markAsProcessed(seg->seq, true);
        }
        return true;
    }
    case DataTypes::KeepAlive: {
        DataSegment _seg = (DataSegment){.dataLength=0, .seq=0, .type=DataTypes::UnKnown, .isNextFragment=false};
        initCrc(&_seg);
        sock.sendSegment(&_seg);
        return true;
    }
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
        sendAck(seg->seq, data->ip, data->port);
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
        sendAck(seg->seq);
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
    initCrc(seg);
    printf("Connection message seq: %d\n", seg->seq);
    toSend.push(new Fragmentator(reinterpret_cast<char*>(seg), (u16)seg->getFullLength(), type, true));
}

void Connector::sendAck(u16 seq) {
    DataSegment seg = (DataSegment){.dataLength=0, .seq=seq, .type=DataTypes::ACK, .isNextFragment=false};
    seg.window = received.getWindow();
    initCrc(&seg);
    sock.sendSegment(&seg);
}

void Connector::sendKeepAlive(u64 now) {
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
    if (size <= 0 || size + sizeof(DataSegment) > 1500) 
        return {true, "The provided value has to be in the range of 0 and 1490"}; // 1500-sizeof(DataSegment)
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