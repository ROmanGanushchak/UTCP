#ifndef CONNECTOR_H
#define CONNECTOR_H
#include "types.h"
#include "data.h"
#include "structs.hpp"
#include "socket.h"
#include "fragmentator.h"

class Connector {
private:
    ReceiveQueue<DataSegment*> queue;
    ReceiveQueue<Fragmentator*> toSend;
    SentMessagesQueue sent;
    ReceivedMessagesQueue received;
    std::list<TimerUnit> timers;

    Socket sock;
    bool isWorking;
    
    Defragmentator *currentDef;

    u64 lastReception;
    u64 lastSendedKeepAlive;
    bool isKeepAliveWarning;
    u16 nextSeq;
    int leastAck;
    int timeToMiss = 1000;
    int maxSentCount = 2;
    u16 maxDataSize = 1;
    void sendConnectionMessage(std::string ip, u16 port, DataTypes type, bool isConfirmed);
    bool sysMessageHandler(DataSegment* segment, u64 now);

public:
    Connector(std::string ip, u16 port);
    void start();
    void finish();
    void connect(std::string ip, u16 port);
    void endConncetion();
    std::pair<bool, std::string> setMaxFragmentSize(u16 size);
    void sendAck(u16 seq);
    void sendAck(u16 seq, std::string ip, u16 port);
    void quit(bool conf=true);

    ReceiveQueue<Fragmentator*>& getToSendQueue() {return toSend;}
};

#endif