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
#include "fileFragment.h"

using namespace std;

int main() {
    bool inputIp = true;
    string ip;
    vector<string> inputs;
    u16 port;
    if (inputIp) {
        printf("Input your ip and port\n");
        cin >> ip >> port;
        if (port == 0) {
            ip = "147.175.162.225"; port = 8080;
        } else if (port == 1) {
            ip = "147.175.162.225"; port = 8082;
            inputs.push_back("connect 147.175.162.225 8080");
        }
    } else {
        ip = "147.175.162.1";
        port = 8080;
    }

    Connector process1(ip, port);

    thread processUnit(&Connector::start, &process1);
    ReceiveQueue<FragmentatorI*>& toSend = process1.getToSendQueue();

    printf("\nWrite the command to be executed\n");
    string input, command, params;
    std::cin.ignore();
    while (true) {
        if (!inputs.empty()) {
            input = inputs.back();
            inputs.pop_back();
        } else
            std::getline(std::cin, input);
        if (input.empty()) continue;
        u64 separator = input.find(' ');
        if (separator != std::string::npos) {
            command = input.substr(0, separator);
            params = input.substr(separator+1);
        } else {
            command = input;
            params = "";
        }
        std::istringstream data(params);
        
        if (command == "file") {
            FILE* file = fopen(params.c_str(), "rb");
            if (file == NULL) {
                printf("Failed to open the file.\n");
                continue;
            }
            fseek(file, 0, SEEK_END);
            printf("Len: %llu\n", ftell(file));
            fseek(file, 0, SEEK_SET);
            size_t pos = params.rfind('/');
            if (pos == std::string::npos) pos = -1;
            string name = params.substr(pos+1);
            printf("File: %p\n", file);
            toSend.push(new FileFragmentator(file, name));
        } else if (command == "connect") {
            string ip; u16 port;
            if (!(data >> ip >> port)) {
                printf("Invalid parans\n");
                continue;
            }
            process1.connect(ip, port);
        } else if (command == "exit") {
            break;
        } else if (command == "SetFragSize") {
            u32 maxFragmentSize;
            if (!(data >> maxFragmentSize)) {
                printf("Invalid params\n");
                continue;
            }
            auto [isError, errorPrint] = process1.setMaxFragmentSize(maxFragmentSize);
            if (isError) printf("Error: %s\n", errorPrint.c_str());
        } else if (command == "quit") {
            process1.quit();
        } else if (command == "savePlace") {
            FileDefragmentator::toSave = params;
        } else {
            DataSegment* segment = createDataSegment(DataTypes::String, false, input.size());
            memcpy((char*)segment->getExtraData(), input.c_str(), input.size());
            toSend.push(new Fragmentator(reinterpret_cast<char*>(segment), segment->getFullLength(), DataTypes::String, true));
        }
    }
    return 0;
}