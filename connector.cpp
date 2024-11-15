#include <thread>
#include <stdexcept>
#include <cassert>
#include <queue>
#include <iostream>
#include "crc.h"
#include "connector.h"
#include "types.h"

using namespace std;

Connector::Connector(string ip, u16 port) : queue(1), toSend(2),
    reader(queue, ip, port), sent(128), 
    isListenerActive(true),
    listener(&SocketReader::startReading, &reader, std::ref(isListenerActive)),
    sender(),
    isWorking(false),
    connection((Connection){.ip=ip, .port=port, .tIp="", .tPort=0})
{
    leastAck = -1;
    nextAck = 0;
};

void Connector::start() {
    isWorking = true;
    while (isWorking) {
        if (!timers.size() && sent.empty() && queue.isEmpty() && toSend.isEmpty()) continue;
        auto nowFullTime = std::chrono::system_clock::now();
        auto now = std::chrono::duration_cast<std::chrono::milliseconds>(nowFullTime.time_since_epoch()).count();

        while (timers.size() && timers.front().endTime < now) {
            TimerUnit timer = timers.front();
            // printf("Timer finished for %d\n", timer.seq);
            auto [elem, status] = sent.get(timer.seq);
            assert(status == ReturnCodes::Success && "The value is present in timer but was deleted from SentQueue");

            if (elem->sentCount == maxSentCount) {
                printf("The message with seq: %d was sent to many times and is considered gone\n", elem->segment->seq);
                sent.markAsProcessed(elem->segment->seq, true);
                timers.pop_front();
                break;
            } else {
                sender.sendSegment(elem->segment);
                elem->sentCount++;
                timers.pop_front();
                timers.push_back((TimerUnit){.seq=timer.seq, .endTime=now + timeToMiss});
            }
        }

        vector<DataSegment*> packets;
        // printf("Got %d fragments\n");
        while (!queue.isEmpty()) {
            DataSegment* segment = queue.front();
            queue.pop();
            printf("Fragment received: type: %d, seq: %d\n", segment->type, segment->seq);
            if (segment->type == DataTypes::ACK) {
                auto [elem, status] = sent.get(segment->seq);
                dprintf("Received ACK, status: %d, isSucess: %d\n", status, status == ReturnCodes::Success);
                if (status == ReturnCodes::Success) {
                    timers.erase(elem->timer);
                    sent.markAsProcessed(segment->seq, true);
                }
                continue;
            }

            auto fragments = received.add(segment);
            dprintf("Added fragments %d, received fragments:\n", segment->seq);
            for (auto fragment : fragments) {
                dprintf("Fragment from received: %d\n", fragment->seq);
                sendAck(fragment->seq);
                if (fragment->type != DataTypes::PureData && !fragment->isNextFragment) {
                    packets.push_back(fragment);
                    continue;
                }
                if (fragment->type != DataTypes::PureData) 
                    currentDef = new Defragmentator();
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
            case DataTypes::Connection: {
                if (connection.tPort != 0) {
                    printf("Trying to connect while last connection is still active\n");
                    break;
                }
                ReceivedConnectionData *data = reinterpret_cast<ReceivedConnectionData*>(packet->getExtraData());
                connection.tIp = data->ip;
                connection.tPort = data->port;
                connection.isApproved = true;
                printf("Got data to connect ip: %s, port: %d\n", connection.tIp.c_str(), connection.tPort);
                sendConnectionMessage(connection.tIp, connection.tPort, DataTypes::ConnectionApproval);
                break;
            }
            case DataTypes::ConnectionApproval: {
                ReceivedConnectionData *data = reinterpret_cast<ReceivedConnectionData*>(packet->getExtraData());
                if (data->ip != connection.tIp || data->port != connection.tPort) {
                    printf("The connection approval receined for incorrect ip address or port");
                    return;
                }
                connection.isApproved = true;
                break;
            }
            case DataTypes::String: {
                printf("Got data: %s\n", (char*)packet->getExtraData());
                break;
            }
            default:
                printf("The packet with unsuportable default handler was called\n");
            }
            free(packet);
        }

        // if (connection.tPort !=0 && connection.isActive && connection.lastReception - now > 5000 && connection.lastReceivedKeepAlive - now > 5000) {
        //     DataSegment* keep = (DataSegment*) malloc(sizeof(DataSegment));
        //     *keep = (DataSegment){.dataLength=0, .seq=nextAck++, .type=DataTypes::KeepAlive, .isNextFragment=false};
        //     keep->crc = getCrc(((char*)keep)+4, sizeof(DataSegment)-4);
        //     toSend.add(new Fragmentator((char*)keep, sizeof(DataSegment), DataTypes::KeepAlive, true));
        // }

        while (!toSend.isEmpty()) {
            Fragmentator* fr = toSend.front();
            dprintf("Received frame %hu\n", fr->fragmentSize);

            dprintf("Size: %d IsActivated: %d\n", fr->fragmentSize, fr->isActivated());
            if (!fr->isActivated())
                nextAck += fr->activate(nextAck, 1);
            while (!fr->isFinished()) {
                DataSegment* segment = fr->getNextFragment();
                printf("ToSend sending: %d, %d\n", segment->seq, segment->type);
                dprintf("Adding element with seq: %d\n", segment->seq);
                timers.push_back((TimerUnit){.seq=segment->seq, .endTime=now + timeToMiss});

                bool wasAdded = sent.add((DataSegmentDescriptor){.segment=segment, .timer=--timers.end(), .sentCount=0});
                if (!wasAdded) {
                    // toSend.add(segment);
                    printf("Critical error, the element was not added\n");
                    break;
                }
                sender.sendSegment(segment);
            }
            if (fr->isFinished()) {
                delete fr;
                toSend.pop();
            }
            else break;
        }
    }
}

void Connector::sendConnectionMessage(string ip, u16 port, DataTypes type) {
    sender.configure(ip, port);
    DataSegment *seg = (DataSegment*) malloc(sizeof(DataSegment));
    *seg = {.dataLength=connection.port, .seq=0, .type=type, .isNextFragment=false};
    seg->crc = getCrc(((char*)seg)+4, sizeof(DataSegment)-4);
    Fragmentator *f = new Fragmentator(reinterpret_cast<char*>(seg), (u16)seg->getFullLength(), type, true);
    toSend.add(f);
}

void Connector::sendAck(u16 seq) {
    DataSegment seg = (DataSegment){.dataLength=0, .seq=seq, .type=DataTypes::ACK, .isNextFragment=false};
    seg.crc = getCrc(reinterpret_cast<char*>(&seg)+4, sizeof(DataSegment)-4);
    sender.sendSegment(&seg);
}

void Connector::connect(string ip, u16 port) {
    if (connection.isApproved == true || connection.port == 0) {
        printf("Curently the device is connected or tryes to connect, end the connection first to connect to other device\n");
        return;
    }
    connection.tIp = ip;
    connection.tPort = port;
    connection.isApproved = false;
    sendConnectionMessage(ip, port, DataTypes::Connection);
}

void Connector::finish() {
    this->isWorking = false;
}

void Connector::endConncetion() {
    DataSegment* segment = (DataSegment*)malloc (sizeof(DataSegment*));
    Fragmentator *f = new Fragmentator(reinterpret_cast<char*>(segment), segment->getFullLength(), DataTypes::EndConnection, true);
    toSend.add(f);
}

pair<bool, string> Connector::setMaxFragmentSize(u16 size) {
    if (size <= 0 || size + sizeof(DataSegment) > 1500) 
        return {true, "The provided value has to be in the range of 0 and 1490"}; // 1500-sizeof(DataSegment)
    this->maxDataSize = size;
    return {false, ""};
}

void Connector::quit() {

}