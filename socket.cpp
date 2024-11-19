#include <stdexcept>
#include <stdio.h>
#include <iostream>
#include "socket.h"
#include "crc.h"
using namespace std;

pair<string, u16> getAddrData(sockaddr_in* addr) {
    char ipStr[INET_ADDRSTRLEN]; // Buffer for the IP string
    inet_ntop(AF_INET, &addr->sin_addr, ipStr, sizeof(ipStr));
    u16 tPort = ntohs(addr->sin_port);
    return {ipStr, tPort};
}

void printAddr(sockaddr_in* addr) {
    char ipStr[INET_ADDRSTRLEN]; // Buffer for the IP string
    inet_ntop(AF_INET, &addr->sin_addr, ipStr, sizeof(ipStr));
    unsigned short fPort = ntohs(addr->sin_port);
    printf("Addr address %s, %hu\n", ipStr, fPort);
}

sockaddr_in createSockAddr(string ip, uint port) {
    sockaddr_in addr;
    addr.sin_family = AF_INET;
    addr.sin_port = htons(port);
    addr.sin_addr.s_addr = inet_addr(ip.c_str()); 
    if (addr.sin_addr.s_addr == INADDR_NONE)
        std::cerr <<  "Invalid IP address: " << ip << " " << WSAGetLastError() << std::endl;
    return addr;
}

Socket::Socket(ReceiveQueue<DataSegment*> &queue, std::string ip, u16 port) : queue(queue), isListening(false), sendState(SenderStates::InActive){
    WSADATA wsa{};
    if (WSAStartup(MAKEWORD(2, 2), &wsa)) 
        throw invalid_argument("Failed to initialize Winsock. Error: " + WSAGetLastError());
    sock = socket(AF_INET, SOCK_DGRAM, 0);
    if (sock == INVALID_SOCKET) {
        WSACleanup();
        throw invalid_argument("Could not create socket. Error: " + WSAGetLastError());
    }

    addr = createSockAddr(ip, port);
    if (bind(sock, (struct sockaddr*)&addr, sizeof(addr)) == SOCKET_ERROR) {
        std::cerr << "Bind failed!" << std::endl;
        closesocket(sock);
        WSACleanup();
    }
}

Socket::~Socket() {
    if (isListening) stopReading();
    if (listener.joinable()) listener.join();
    closesocket(sock);
    WSACleanup();
}

void Socket::reading() {
    sockaddr_in _senderAddr;
    int clientAddrLen = sizeof(_senderAddr);
    while (isListening) {
        auto [ip, port] = getListeningData();
        // printf("Listening on %s, %d\n", ip.c_str(), port);
        int recvSize = recvfrom(sock, buffer, sizeof(buffer), 0, (struct sockaddr*)&_senderAddr, &clientAddrLen);
        if (recvSize == SOCKET_ERROR) {
            std::cerr << "Recvfrom failed!" << std::endl;
            continue;
        }
        DataSegment *tempSegment = reinterpret_cast<DataSegment*>(buffer);
        if (!checkCrc(tempSegment) || tempSegment->getFullLength() != recvSize) {
            printf("The received was damaged or has incorrect size\n");
            continue;
        }
        printf("Received the segment seq: %d, type: %d, dataSize: %d\n", tempSegment->seq, tempSegment->type, tempSegment->dataLength);
        if (tempSegment->type == DataTypes::Connection || tempSegment->type == DataTypes::ConnectionApproval) {
            char senderIP[INET_ADDRSTRLEN];
            inet_ntop(AF_INET, &(_senderAddr.sin_addr), senderIP, INET_ADDRSTRLEN);
            u16 senderPort = ntohs(_senderAddr.sin_port);
            ReceivedConnectionData data = {.port=senderPort, .ip=senderIP};
            memcpy(buffer+recvSize, (char*)&data, sizeof(ReceivedConnectionData));
            tempSegment->dataLength += sizeof(ReceivedConnectionData);
        }
        DataSegment *segment = reinterpret_cast<DataSegment*>(malloc (sizeof(DataSegment) + tempSegment->dataLength));
        memcpy(segment, tempSegment, sizeof(DataSegment));
        memcpy(segment->getExtraData(), buffer+sizeof(DataSegment), tempSegment->dataLength);
        dprintf("Received segment with seq: %hu, type: %d\n", segment->seq, segment->type);
        this->queue.push(segment);
    }
}

void Socket::startReading() {
    if (isListening) {
        printf("Trying to create multyple listening threads for single socket\n");
        return;
    }
    isListening = true;
    listener = thread(&Socket::reading, this);
}

void Socket::stopReading() {
    if (!isListening) return;
    isListening = false;
    auto [ip, port] = getListeningData();
    DataSegment seg = (DataSegment){.dataLength=0, .seq=0, .type=DataTypes::UnKnown, .isNextFragment=false};
    for (int i=0; i<3; i++)
        sendSegmentCust(&seg, ip, port);
}

void Socket::configure(string ip, u16 port, SenderStates state) {
    if (state != InActive) 
        senderAddr = createSockAddr(ip, port);
    sendState = state;
}

void Socket::confirmConfiguration() {
    if (sendState == SenderStates::ConfirmAwait) {
        sendState = SenderStates::Active;
    }
}

int Socket::sendSegment(DataSegment *segment) {
    if (sendState != SenderStates::Active && !(segment->type == DataTypes::Connection && sendState == SenderStates::ConfirmAwait)) {
        printf("Trying to send message without initialization of sender data\n");
        return -1;
    }
    // printf("Sending message with seq: %d, type: %d size: %d with\n", segment->seq, segment->type, segment->dataLength);
    // printAddr(&senderAddr);

    std::lock_guard<std::mutex> lock(sendingMutex);
    int sentSize = sendto(sock, reinterpret_cast<char*>(segment), segment->getFullLength(), 0, (struct sockaddr*)&senderAddr, sizeof(senderAddr));
    if (sentSize == SOCKET_ERROR) 
        std::cerr << "sendto failed. Error: " << WSAGetLastError() << std::endl;
    return sentSize;
}

int Socket::sendSegmentCust(DataSegment *segment, string ip, u16 port) {
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
    std::lock_guard<std::mutex> lock(sendingMutex);
    int sentSize = sendto(sock, reinterpret_cast<char*>(segment), segment->getFullLength(), 0, (struct sockaddr*)&_addr, sizeof(_addr));
    if (sentSize == SOCKET_ERROR) 
        std::cerr << "sendto failed. Error: " << WSAGetLastError() << std::endl;
    return sentSize;
}

pair<string, u16> Socket::getSenderData() {
    return getAddrData(&senderAddr);
}

pair<string, u16> Socket::getListeningData() {
    return getAddrData(&addr);
}

bool Socket::isSettedUp() {
    return sendState != SenderStates::InActive;
}