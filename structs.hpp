#ifndef RECEIVED_QUEUE_H
#define RECEIVED_QUEUE_H

#include <stdexcept>
#include <deque>
#include <mutex>
#include <list>
#include <optional>
#include "data.h"
#include "types.h"


template <typename T>
class ReceiveQueue {
private:
    std::deque<T> segments;
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
            segments.pop_back();
        }
    }
    void push(T segment) {
        std::lock_guard<std::mutex> lock(mtx);
        segments.push_back(segment);
    }
    void pushFront(T segment) {
        std::lock_guard<std::mutex> lock(mtx);
        segments.push_front(segment);
    }
    void pop() {
        std::lock_guard<std::mutex> lock(mtx);
        segments.pop_front();
        dprintf("Pop was called\n");
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
    u32 window;
    u32 windowUsed;

    inline int getIndex(int seq);
    virtual int getAck(T elem) = 0;
    bool add(T elem, u32 size);
    // returns index of deleted or -1 if nothing was deleted
    int del(int seq);
    void updateFirstValue();
public:
    ModQueue(int initCapacity=4, u32 window=65000, int firstIndex=0);
    void resize(int newSize);
    std::vector<T> iniq(u16 seq);
    void initFirst(u16 seq);
    // may return NULL as T* if index is invalid
    std::pair<T*, ReturnCodes> get(int seq);
    bool empty() {return elemCount != 0;}
    bool isFull() {return arr.size() == elemCount;}
    void setFirst(int _first) { first = _first; }
    u32 getWindow();
    void setWindow(u32 size);
    inline bool isAddable(u16 size);
};


class TestModQueue : public ModQueue<int> {
protected:
    virtual int getAck(int elem) override {
        return elem;
    };
public:
    TestModQueue(int initCapacity=4) : ModQueue(initCapacity, 5000) {};
};


class SentMessagesQueue : public ModQueue<DataSegmentDescriptor> {
protected:
    int getAck(DataSegmentDescriptor elem) override;
public:
    SentMessagesQueue(int initCapacity=4, u32 window=5000);
    ~SentMessagesQueue();
    DataSegmentDescriptor* add(DataSegmentDescriptor segment);
    void markAsProcessed(int seq, bool free=false);
};


class ReceivedMessagesQueue : public ModQueue<DataSegment*> {
protected:
    int getAck(DataSegment* elem) override;
public:
    ReceivedMessagesQueue(int initCapacity=16, u32 window=5000);
    ~ReceivedMessagesQueue();
    std::pair<bool, std::vector<DataSegment*>> add(DataSegment *elem);
};


template class ModQueue<int>;
template class ModQueue<DataSegmentDescriptor>;
template class ModQueue<DataSegment*>;

#endif