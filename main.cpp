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
    setDefaultSavePath();
    string ip;
    u16 port;
    printf("Input your ip and port: \n");
    cin >> ip >> port;

    Connector process1(ip, port);
    thread processUnit(&Connector::start, &process1);
    ReceiveQueue<FragmentatorI*>& toSend = process1.getToSendQueue();

    printf("\nTo see the list of commands write the word 'info'\nWrite the command to be executed\n");
    string command, input;
    while (true) {
        cin >> command;
        if (command.empty() || command == "\n") continue;
        if (command == "file") {
            string path; cin >> path;
            FILE* file = fopen(path.c_str(), "rb");
            if (file == NULL) {
                printf("Failed to open the file.\n");
                continue;
            }
            size_t pos = path.rfind('/');
            if (pos == std::string::npos) pos = -1;
            string name = path.substr(pos+1);
            printf("File: %p\n", file);
            toSend.push(new FileFragmentator(file, name));
        } else if (command == "connect") {
            string ip; u16 port;
            if (!(cin >> ip >> port)) {
                printf("Invalid parans\n");
                continue;
            }
            process1.connect(ip, port);
        } else if (command == "exit") {
            break;
        } else if (command == "SetFragSize") {
            u32 maxFragmentSize;
            if (!(cin >> maxFragmentSize)) {
                printf("Invalid params\n");
                continue;
            }
            auto [isError, errorPrint] = process1.setMaxFragmentSize(maxFragmentSize);
            if (isError) printf("Error: %s\n", errorPrint.c_str());
        } else if (command == "quit") {
            process1.quit();
        } else if (command == "savePlace") {
            cin >> input;
            DWORD attrs = GetFileAttributesA(input.c_str());
            if (!(attrs != INVALID_FILE_ATTRIBUTES && (attrs & FILE_ATTRIBUTE_DIRECTORY))) {
                printf("Such folder was not found\n");
                continue;
            }
            FileDefragmentator::toSave = input;
        } else if (command == "setError") {
            u16 errorChance;
            if (!(cin >> errorChance)) {
                printf("Invalid parans\n");
                continue;
            }
            process1.setError(errorChance);
        } else if (command == "info") {
            cout << 
            "1. connect <ip> <port> - creates the connection between 2 hosts, works only if both host dont participate in other conversation\n" <<
            "2. SetFragSize <size> - sets the max payload size of the fragment\n" <<
            "3. savePlace <path> - sets the default save place for the files\n" <<
            "4. setError <chance> - sets the chance of the frame to be lost to 1 / chance, is chance is 0 their is no artificial fragment lost\n" <<
            "5. send <string> - sends the string to the other host\n" <<
            "6. file <path> - sends the file to the other host, the file name is not changed. \n" <<
            "7. move <fileName> <destinationFolder> - moves the file from the destination folder to the specified place" <<
            "8. quit - ends the connection without closing the program\n" <<
            "9. exit - exists the program\n";
        } else if (command == "send") {
            getline(std::cin, input);
            char* data = (char*) malloc (input.size());
            memcpy(data, input.data()+1, input.size()-1);
            data[input.size()-1] = '\0';
            toSend.push(new Fragmentator(data, input.size(), DataTypes::String, false));
        } else if (command == "sendNextWithErr") {
            process1.sendNextWithErr();
        } else if (command == "move") {
            string name, path;
            cin >> name >> path;
            string srcPath = FileDefragmentator::toSave + "/" + name;
            string dstPath = path + "/" + name;
            if (MoveFile(srcPath.c_str(), dstPath.c_str())) 
                printf("The file %.*s was moved succesfully, the new path: %.*s\n", name.size(), name.c_str(), dstPath.size(), dstPath.c_str());
            else 
                printf("Unable to move the file, double check the file name or destination location\n");
        }else {
            printf("Unknown command\n");
        }
    }
    return 0;
}