#ifndef SOCKET_HH
#define SOCKET_HH

#include <string>
#include <mutex>
#include <winsock2.h>
#include <ws2tcpip.h>
#include <iphlpapi.h>
#include <thread>

#include "structs.hpp"
#include "data.h"
#include "types.h"

struct ReceivedConnectionData {
    u16 port;
    char ip[22];
};

enum SenderStates : u8 {
    InActive = 0,
    ConfirmAwait = 1,
    Active = 2
};

class Socket {
private:
    SOCKET sock;
    sockaddr_in addr;
    sockaddr_in senderAddr;
    SenderStates sendState;
    bool isListening;
    char buffer[2048];
    ReceiveQueue<DataSegment*> &queue;
    std::mutex sendingMutex;
    std::thread listener;
    void reading();
public:
    Socket(ReceiveQueue<DataSegment*> &queue, std::string ip, u16 port);
    ~Socket();

    void startReading();
    void stopReading();
    int sendSegment(DataSegment *segment);
    int sendSegmentCust(DataSegment *segment, std::string ip, u16 port);
    void configure(std::string ip, u16 port, SenderStates state=SenderStates::ConfirmAwait);
    void confirmConfiguration();
    inline bool getIsConfigured() const { return sendState == SenderStates::Active; }
    inline bool isSettedUp();
    std::pair<std::string, u16> getSenderData();
    inline std::pair<std::string, u16> getListeningData();
};

#endif