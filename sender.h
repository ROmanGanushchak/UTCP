#ifndef SENDER_H
#define SENDER_H
#include <string>
#include <winsock2.h>
#include <ws2tcpip.h>
#include <iphlpapi.h>

#include "types.h"
#include "data.h"

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