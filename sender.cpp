#include <stdio.h>
#include <string>
#include <bits/stdc++.h>
#include <winsock2.h>
#include <ws2tcpip.h>
#include <iphlpapi.h>
#include <stdexcept>

#include "sender.h"
#include "types.h"
#include "data.h"

using namespace std;

inline SOCKET createWinSock() {
    WSADATA wsa{};
    if (WSAStartup(MAKEWORD(2, 2), &wsa)) {
        std::cerr << "Failed to initialize Winsock. Error: " << WSAGetLastError() << std::endl;
        throw invalid_argument("");
    }
    SOCKET sock = socket(AF_INET, SOCK_DGRAM, 0);
    if (sock == INVALID_SOCKET) {
        std::cerr << "Could not create socket. Error: " << WSAGetLastError() << std::endl;
        WSACleanup();
        throw invalid_argument("");
    }
    return sock;
}

sockaddr_in createSockAddr(string ip, uint port) {
    sockaddr_in serverAddr;
    serverAddr.sin_family = AF_INET;
    serverAddr.sin_port = htons(port);
    serverAddr.sin_addr.s_addr = inet_addr(ip.c_str()); 
    if (serverAddr.sin_addr.s_addr == INADDR_NONE) {
        std::cerr << "Invalid IP address: " << ip << std::endl;
    }

    return serverAddr;
}

SocketSender::SocketSender () : isConfigured(false) {
    sock = createWinSock();
}

void SocketSender::configure(string ip, uint port) {
    if (isConfigured) {
        printf("Trying to reConfigure the sender\n");
        return;
    } 
    addr = createSockAddr(ip, port);
    printf("Sock is configured to:\n");
    printAddr(&addr);
    isConfigured = true;
}

SocketSender::~SocketSender () {
    closesocket(sock);
    WSACleanup();
}

int SocketSender::sendSegment(DataSegment *segment) {
    if (!isConfigured) {
        printf("Trying to send message without initialization of sender data\n");
        return -1;
    }
#if DEBUG_PRINT
    printf("Sent message with seq: %d, type: %d with the addr:\n", segment->seq, segment->type);
    printAddr(&addr);
#endif
    int sentSize = sendto(sock, reinterpret_cast<char*>(segment), segment->getFullLength(), 0, (struct sockaddr*)&addr, sizeof(addr));
    if (sentSize == SOCKET_ERROR) 
        std::cerr << "sendto failed. Error: " << WSAGetLastError() << std::endl;
    return sentSize;
}

int SocketSender::sendSegmentCust(DataSegment *segment, string ip, u16 port) {
    sockaddr_in _addr = createSockAddr(ip, port);
    if (_addr.sin_addr.s_addr == INADDR_NONE) {
        std::cerr << "Invalid IP address: " << ip << std::endl;
        return -1;
    }
#if DEBUG_PRINT
    printf("Preparing to send message to %s:%d\n", ip.c_str(), port);
    printf("%d\n", segment->getFullLength());
    printAddr(&_addr);
#endif
    int sentSize = sendto(sock, reinterpret_cast<char*>(segment), segment->getFullLength(), 0, (struct sockaddr*)&_addr, sizeof(_addr));
    if (sentSize == SOCKET_ERROR) 
        std::cerr << "sendto failed. Error: " << WSAGetLastError() << std::endl;
    return sentSize;
}

void printAddr(sockaddr_in* addr) {
    char ipStr[INET_ADDRSTRLEN]; // Buffer for the IP string
    inet_ntop(AF_INET, &addr->sin_addr, ipStr, sizeof(ipStr));
    unsigned short fPort = ntohs(addr->sin_port);
    printf("Addr address %s, %hu\n", ipStr, fPort);
}