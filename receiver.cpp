#include <winsock2.h>
#include <ws2tcpip.h>
#include <iphlpapi.h>
#include <iostream>
#include <thread>
#include <cstdlib>
#include <stdio.h>
#include <cstdio>
#include <stdexcept>

#include "data.h"
#include "receiver.h"
#include "sender.h"
#include "structs.hpp"

using namespace std;

SocketReader::SocketReader(ReceiveQueue<DataSegment*> &queue, string ip, uint port) : queue(queue) {
    sock = createWinSock();
    auto state = initListenSock(sock, ip, port);
    if (!state.second) 
        throw std::invalid_argument("The addr was not created for this data");
    addr = state.first;
};

SocketReader::~SocketReader() {
    closesocket(sock);
    WSACleanup();
}

void SocketReader::startReading(bool &isActive) {
    sockaddr_in senderAddr = {};
    int senderAddrSize = sizeof(senderAddr);
    while (isActive) {
        int adrSize = sizeof(addr);
#if DEBUG_PRINT
        printf("Listening for: ");
        printAddr(&addr);
#endif
        int recvSize = recvfrom(sock, buffer, 1024, 0, (struct sockaddr*)&senderAddr, &senderAddrSize);
        dprintf("Received message from network with size: %d\n", recvSize);
        if (recvSize == SOCKET_ERROR) {
            if (WSAGetLastError() != WSAEWOULDBLOCK) {
                printf("Recvfrom failed, the rad length: %d, maybe buffer was not big enogh. Error: %d\n", recvSize, WSAGetLastError());
            }
            // printf("NonBlock");
            continue;
        }
        DataSegment *tempSegment = reinterpret_cast<DataSegment*>(buffer);
        if (sizeof(DataSegment) + tempSegment->dataLength != recvSize) {
            printf("The received fragment doesnt have enough size or was damaged");
            continue;
        }
        if (tempSegment->type == DataTypes::Connection || tempSegment->type == DataTypes::ConnectionApproval) {
            char senderIP[INET_ADDRSTRLEN];
            inet_ntop(AF_INET, &(senderAddr.sin_addr), senderIP, INET_ADDRSTRLEN);
            printf("Received port: %d\n", tempSegment->dataLength);
            ReceivedConnectionData data = {.port=tempSegment->dataLength, .ip=senderIP};
            memcpy(buffer+recvSize, (char*)&data, sizeof(ReceivedConnectionData));
            tempSegment->dataLength = sizeof(ReceivedConnectionData);
        }

        DataSegment *segment = reinterpret_cast<DataSegment*>(malloc (sizeof(DataSegment) + tempSegment->dataLength));
        memcpy(segment, tempSegment, sizeof(DataSegment));
        memcpy(segment->getExtraData(), buffer+sizeof(DataSegment), tempSegment->dataLength);
        dprintf("Received segment with seq: %hu, type: %d\n", segment->seq, segment->type);
        this->queue.add(segment);
    }
}

pair<sockaddr_in, bool> SocketReader::initListenSock(SOCKET sock, string ip, uint port, bool async) {
    sockaddr_in listenerAddr = createSockAddr(ip, port);

    if (bind(sock, (struct sockaddr*)&listenerAddr, sizeof(listenerAddr)) == SOCKET_ERROR) {
        std::cerr << "Bind failed. Error: " << WSAGetLastError() << std::endl;
        closesocket(sock);
        WSACleanup();
        return {{}, false};
    }

    ULONG nonBlock = 1;
    if (async && ioctlsocket(sock, FIONBIO, &nonBlock) == SOCKET_ERROR) {
        printf("Error occured while setting socket to non-stoping mode\n");
        return {{}, false};
    }

    return {listenerAddr, true};
}