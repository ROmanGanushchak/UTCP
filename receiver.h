#ifndef RECEIVER_H
#define RECEIVER_H
#include <thread>
#include <queue>
#include <chrono>
#include <ctime>
#include <string>

#include "structs.hpp"
#include "data.h"
#include "sender.h"
#include "types.h"

struct ReceivedConnectionData {
    u16 port;
    std::string ip;
};

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
    static std::pair<sockaddr_in, bool> initListenSock(SOCKET sock, std::string ip, uint port, bool async=false);
};


#endif