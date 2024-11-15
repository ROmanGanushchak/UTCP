#include <stdexcept>
#include <vector>
#include <cassert>
#include <list>
#include <stdexcept>
#include "structs.hpp"
#include "types.h"

using namespace std;

template <typename T>
ModQueue<T>::ModQueue(int initCapacity, int firstIndex) 
    : first(firstIndex), elemCount(0), arr(initCapacity), states(initCapacity, States::Empty) {}

template <typename T>
void ModQueue<T>::resize(int newSize) {
    if (states[first] == States::Empty) {
        arr.resize(newSize);
        return;
    }
    vector<T> newArr(newSize);
    vector<char> newStates(newSize, States::Empty);
    for (int i=0; i<arr.size(); i++) {
        if (states[i] == States::Empty) continue;
        int index = getAck(arr[i]) % newArr.size();
        if (states[index] != States::Empty) 
            throw std::length_error("The new container size is not big enough for all elements from prev conteiner in ModQueue");
        newStates[index] = states[i];
        newArr[index] = arr[i];
    }
    arr = newArr;
    states = newStates;
}

template <typename T>
int ModQueue<T>::getIndex(int seq) {
    if (seq < first || seq > first + arr.size())
        return -2;
    return seq % arr.size();
}

template <typename T>
pair<T*, ReturnCodes> ModQueue<T>::get(int seq) {
    if (seq < first || seq > first + arr.size())
        return {NULL, ReturnCodes::ACKWasAlreadyProceed};
    if (states[seq % arr.size()] != States::Active)    
        return {NULL, ReturnCodes::ACKWasAlreadyProceed};
    return {&arr[seq % arr.size()], ReturnCodes::Success};
}

template <typename T>
void ModQueue<T>::updateFirstValue() {
    int n = arr.size(), start = first;
    for (; first - n != start && states[first%n] == States::Deleted; first++) 
        states[first%n] = States::Empty;
}

template <typename T>
bool ModQueue<T>::add(T elem) {
    int index = getIndex(getAck(elem));
#if DEBUG_PRINT
    printf("Added at ModQueue at index: %d, for seq: %d\n", index, getAck(elem));
#endif
    if (index < first || states[index] != States::Empty)
        return false;
    arr[index] = elem;
    states[index] = States::Active;
    elemCount++;
    return true;
}

template <typename T>
int ModQueue<T>::del(int seq) {
    int index = getIndex(seq);
    if (index < 0 || states[index] != States::Active)
        return -1;
#if DEBUG_PRINT
    printf("Del at index: %d, first: %d, with seq: %d\n", index, first, seq);
#endif
    if (first == seq) {
        states[index] = States::Deleted;
        updateFirstValue();
    } else 
        states[index] = States::Deleted;
    return index;
}



SentMessagesQueue::SentMessagesQueue(int initCapacity) : ModQueue(initCapacity) {}
SentMessagesQueue::~SentMessagesQueue() {
    for (int i=0; i<arr.size(); i++) {
        if (states[i] == States::Active) 
            free(arr[i].segment);
    }
}

void SentMessagesQueue::markAsProcessed(int seq, bool toFree) {
    int index = del(seq);
    dprintf("Marked as proceed %d\n", seq);
    if (index >= 0 && toFree)
        free(arr[index].segment);
}

bool SentMessagesQueue::add(DataSegmentDescriptor segment) {
    return ModQueue<DataSegmentDescriptor>::add(segment);
}

int SentMessagesQueue::getAck(DataSegmentDescriptor elem) {
    return elem.segment->seq;
}


ReceivedMessagesQueue::ReceivedMessagesQueue (int initCapacity)
    : ModQueue(initCapacity) {}

int ReceivedMessagesQueue::getAck(DataSegment* elem) {
    return elem->seq;
}

ReceivedMessagesQueue::~ReceivedMessagesQueue() {
    for (int i=0; i<arr.size(); i++) 
        if (states[i] == States::Active)
            free(arr[i]);
}

vector<DataSegment*> ReceivedMessagesQueue::add(DataSegment *elem) {
    if (!ModQueue<DataSegment*>::add(elem)) 
        return {};
    int index = elem->seq % arr.size();
    if (index != first) return {};
    int n = arr.size();
    vector<DataSegment*> rez;
    for (; states[first%n] == States::Active; first++) {
        rez.push_back(arr[first%n]);
        states[first%n] = States::Empty;
    }
    return rez;
}