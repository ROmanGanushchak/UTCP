#ifndef CONNECTOR_H
#define CONNECTOR_H
#include "types.h"
#include "data.h"
#include "structs.hpp"
#include "sender.h"
#include "receiver.h"
#include "fragmentator.h"

struct Connection {
    std::string ip;
    u16 port;
    std::string tIp;
    u16 tPort;
    u64 lastReception;
    u64 lastReceivedKeepAlive;
    bool isApproved;
};

class Connector {
private:
    ReceiveQueue<DataSegment*> queue;
    ReceiveQueue<Fragmentator*> toSend;

    SocketReader reader;
    SocketSender sender;
    SentMessagesQueue sent;
    ReceivedMessagesQueue received;
    std::list<TimerUnit> timers;
    bool isListenerActive;
    bool isWorking;

    std::thread listener;
    Connection connection;
    Defragmentator *currentDef;

    int leastAck;
    int nextAck;
    int timeToMiss = 1000;
    int maxSentCount = 2;
    u16 maxDataSize = 300;
    void sendConnectionMessage(std::string ip, u16 port, DataTypes type);

public:
    Connector(std::string ip, u16 port);
    void start();
    void finish();
    void connect(std::string ip, u16 port);
    void endConncetion();
    std::pair<bool, std::string> setMaxFragmentSize(u16 size);
    void sendAck(u16 seq);
    void quit();

    ReceiveQueue<Fragmentator*>& getToSendQueue() {return toSend;}
};

#endif