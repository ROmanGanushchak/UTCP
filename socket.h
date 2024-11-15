#ifndef SOCKET_HH
#define SOCKET_HH

#include <string>
#include <mutex>
#include <winsock2.h>
#include <ws2tcpip.h>
#include <iphlpapi.h>

#include "structs.hpp"
#include "data.h"
#include "sender.h"
#include "types.h"

struct ReceivedConnectionData {
    u16 port;
    std::string ip;
};

std::mutex sendingMutex;

// think how to stop socket reader
class SocketReader {
private:
    SOCKET sock;
    sockaddr_in addr;
    char buffer[2048];
    ReceiveQueue<DataSegment*> &queue;
public:
    SocketReader(ReceiveQueue<DataSegment*> &queue, std::string ip, uint port);
    ~SocketReader();

    void startReading(bool &isActive);
    void send();
    static std::pair<sockaddr_in, bool> initListenSock(SOCKET sock, std::string ip, uint port, bool async=false);
};

class SocketSender {
private:
    SOCKET sock;
    sockaddr_in addr;
    bool isConfigured;
public:
    SocketSender();
    ~SocketSender();
    void configure(std::string ip, uint port);
    int sendSegment(DataSegment *segment);
    int sendSegmentCust(DataSegment *segment, std::string ip, u16 port);
    bool getIsConfigured() const { return isConfigured; }
};

SOCKET createWinSock();
sockaddr_in createSockAddr(std::string ip, uint port);
void printAddr(sockaddr_in* addr);

#endif