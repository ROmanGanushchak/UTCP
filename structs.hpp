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

enum AddingStates : u8 {
    Added,
    NoSize,
    Incorrect,
};

enum class States : u8 {
    Active,
    Deleted,
    Empty,
    Suppresed,
};

template <typename T>
class ModQueue {
protected:
    int first;
    int elemCount;
    std::vector<T> arr;
    std::vector<States> states;
    u32 window;
    u32 windowUsed;

    inline int getIndex(int seq);
    virtual int getSeq(T elem) = 0;
    virtual DataSegment* getSeg(T elem) = 0;
    AddingStates add(T elem, u32 size);
    // returns index of deleted or -1 if nothing was deleted
    int del(int seq);
    void updateFirstValue();
public:
    ModQueue(int initCapacity=4, u32 window=65000, int firstIndex=1);
    void resize(int newSize);
    std::vector<T> iniq(u16 seq);
    void initFirst(u16 seq);
    int getFirst();
    // may return NULL as T* if index is invalid
    std::pair<T*, States> get(int seq);
    bool empty() {return elemCount != 0;}
    bool isFull() {return arr.size() == elemCount;}
    void setFirst(int _first) { first = _first; }
    u32 getWindow();
    u32 getWindowSize();
    void setWindow(u32 size);
    inline bool isAddable(u16 size);
};


class TestModQueue : public ModQueue<int> {
protected:
    virtual int getSeq(int elem) override {
        return elem;
    };
public:
    TestModQueue(int initCapacity=4) : ModQueue(initCapacity, 5000) {};
};


class SentMessagesQueue : public ModQueue<DataSegmentDescriptor> {
protected:
    int getSeq(DataSegmentDescriptor elem) override;
    DataSegment* getSeg(DataSegmentDescriptor elem) override;
public:
    SentMessagesQueue(int initCapacity=4, u32 window=5000);
    ~SentMessagesQueue();
    std::pair<AddingStates, DataSegmentDescriptor*> add(DataSegmentDescriptor segment);
    void markAsProcessed(int seq, bool free=false);
    AddingStates changeState(int seq, States state);
};


class ReceivedMessagesQueue : public ModQueue<DataSegment*> {
protected:
    int getSeq(DataSegment* elem) override;
    DataSegment* getSeg(DataSegment* elem) override;
public:
    ReceivedMessagesQueue(int initCapacity=16, u32 window=5000);
    ~ReceivedMessagesQueue();
    std::pair<bool, std::vector<DataSegment*>> add(DataSegment *elem);
};


template class ModQueue<int>;
template class ModQueue<DataSegmentDescriptor>;
template class ModQueue<DataSegment*>;

#endif