#ifndef RECEIVED_QUEUE_H
#define RECEIVED_QUEUE_H

#include <stdexcept>
#include <queue>
#include <mutex>
#include <list>
#include <optional>
#include "data.h"
#include "types.h"


template <typename T>
class ReceiveQueue {
private:
    std::queue<T> segments;
    std::mutex mtx;
    char deconstructType;
public:
    bool isEmpty() {
        return segments.empty();
    }
    ReceiveQueue(char type=0) {
        this->deconstructType = type;
    }
    ~ReceiveQueue() {
        if (!segments.size() || deconstructType == 0) return;
        while (segments.size()) {
            auto elem = segments.front();
            if (deconstructType == 1)
                free(elem);
            else if (deconstructType == 2)
                delete elem;
            segments.pop();
        }
    }
    void add(T segment) {
        std::lock_guard<std::mutex> lock(mtx);
        segments.push(std::move(segment));
    }
    void pop() {
        std::lock_guard<std::mutex> lock(mtx);
        segments.pop();
        dprintf("Pop was called\n");
        return;
    }
    T front() {return segments.front();}
};

enum ReturnCodes {
    Success = 0,
    ACKWasAlreadyProceed = 1,
    ACKCantBeStoredInThisWindow = 2
};

template <typename T>
class ModQueue {
protected:
    struct States {
        static constexpr int Active = 0;
        static constexpr int Deleted = 1;
        static constexpr int Empty = 2;
    };
    int first;
    int elemCount;
    std::vector<T> arr;
    std::vector<char> states;

    inline int getIndex(int seq);
    virtual int getAck(T elem) = 0;
    bool add(T elem);
    // returns index of deleted or -1 if nothing was deleted
    int del(int seq);
    void updateFirstValue();
public:
    ModQueue(int initCapacity=64, int firstIndex=0);
    void resize(int newSize);
    std::vector<T> iniq(u16 seq);
    void initFirst(u16 seq);
    // may return NULL as T* if index is invalid
    std::pair<T*, ReturnCodes> get(int seq);
    bool empty() {return elemCount != 0;}
    bool isFull() {return arr.size() == elemCount;}
    void setFirst(int _first) { first = _first; }
};


class TestModQueue : public ModQueue<int> {
protected:
    virtual int getAck(int elem) override {
        return elem;
    };
public:
    TestModQueue(int initCapacity=64) : ModQueue(initCapacity) {};
};


class SentMessagesQueue : public ModQueue<DataSegmentDescriptor> {
protected:
    int getAck(DataSegmentDescriptor elem) override;
public:
    SentMessagesQueue(int initCapacity=128);
    ~SentMessagesQueue();
    bool add(DataSegmentDescriptor segment);
    void markAsProcessed(int seq, bool free=false);
};


class ReceivedMessagesQueue : public ModQueue<DataSegment*> {
protected:
    int getAck(DataSegment* elem) override;
public:
    ReceivedMessagesQueue(int initCapacity=128);
    ~ReceivedMessagesQueue();
    std::vector<DataSegment*> add(DataSegment *elem);
};


template class ModQueue<int>;
template class ModQueue<DataSegmentDescriptor>;
template class ModQueue<DataSegment*>;

#endif