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
    ReceiveQueue<FragmentatorI*> toSend;
    SentMessagesQueue sent;
    ReceivedMessagesQueue received;
    std::list<TimerUnit> timers;
    std::deque<DataSegment*> toResend;

    Socket sock;
    bool isWorking;
    
    DefragmentatorI *currentDef;

    u64 now;
    u64 lastReception;
    u64 lastSendedKeepAlive;
    bool isKeepAliveWarning;
    u16 nextSeq;
    int leastAck;
    int timeToMiss = 2000;
    int maxSentCount = 2;
    u16 maxDataSize = 1000;
    void sendConnectionMessage(std::string ip, u16 port, DataTypes type, bool isConfirmed);
    bool sysMessageHandler(DataSegment* segment);
    AddingStates trySendFragment(DataSegment *seg);
    void sendKeepAlive();
    void sendAck(u16 seq);
    void sendAck(u16 seq, std::string ip, u16 port);

public:
    Connector(std::string ip, u16 port);
    void start();
    void finish();
    void connect(std::string ip, u16 port);
    std::pair<bool, std::string> setMaxFragmentSize(u16 size);
    void quit(bool conf=true);
    void setError(u16 coef);

    ReceiveQueue<FragmentatorI*>& getToSendQueue() {return toSend;}
};

#endif