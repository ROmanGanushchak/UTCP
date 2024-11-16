#include <stdio.h>
#include <string>
#include <bits/stdc++.h>
#include <iostream>
#include <vector>
#include <thread>
#include <unistd.h>
#include "string.h"

#include "types.h"
#include "connector.h"
#include "structs.hpp"

using namespace std;

int main() {
    bool inputIp = true;
    string ip;
    u16 port;
    if (inputIp) {
        printf("Input your ip and port\n");
        cin >> ip >> port;
    } else {
        ip = "147.175.162.1";
        port = 8080;
    }

    Connector process1(ip, port);

    thread processUnit(&Connector::start, &process1);
    ReceiveQueue<Fragmentator*>& toSend = process1.getToSendQueue();

    printf("\nWrite the command to be executed\n");
    string bufferStr;
    char buffer[1024];
    char ipBuffer[20];
    u16 _port;
    u16 maxFragmentSize;
    u16 ips[4];
    std::cin.ignore();
    while (true) {
        std::getline(std::cin, bufferStr);
        strcpy(buffer, bufferStr.c_str());
        if (buffer[0] == '\0') continue;
        if (!strcmp("exit", buffer))
            break;
        if (sscanf(buffer, "connect %d.%d.%d.%d %d", &ips[0], &ips[1], &ips[2], &ips[3], &_port) == 5) {
            sprintf(ipBuffer, "%d.%d.%d.%d", ips[0], ips[1], ips[2], ips[3]);
            string _ip = ipBuffer;
            process1.connect(_ip, _port);
            continue;
        }
        if (sscanf(buffer, "SetFragSize %u", &maxFragmentSize) == 1) {
            auto [isError, errorPrint] = process1.setMaxFragmentSize(maxFragmentSize);
            if (isError) printf("Error: %s\n", errorPrint.c_str());
            continue;   
        }
        if (strcmp(buffer, "quit") == 0) {
            process1.quit();
            continue;
        }
        u16 len = strlen(buffer);
        DataSegment* segment = createDataSegment(DataTypes::String, false, len);
        memcpy((char*)segment->getExtraData(), buffer, len);
        Fragmentator *f = new Fragmentator(reinterpret_cast<char*>(segment), segment->getFullLength(), DataTypes::String, true);
        toSend.add(f);
    }
    return 0;
}