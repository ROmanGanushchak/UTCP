#include <stdexcept>
#include <vector>
#include <cassert>
#include <list>
#include <stdexcept>
#include "structs.hpp"
#include "types.h"

using namespace std;

template <typename T>
ModQueue<T>::ModQueue(int initCapacity, u32 window, int firstIndex) 
    : first(firstIndex), elemCount(0), arr(initCapacity), states(initCapacity, States::Empty),
    window(window), windowUsed(0) {}

template <typename T>
void ModQueue<T>::resize(int newSize) {
    if (states[first%arr.size()] == States::Empty) {
        arr.resize(newSize);
        return;
    }
    vector<T> newArr(newSize);
    vector<char> newStates(newSize, States::Empty);
    for (int i=0; i<arr.size(); i++) {
        if (states[i] != States::Active) continue;
        int index = getAck(arr[i]) % newSize;
        if (newStates[index] != States::Empty) {
            for (int j=0; j<arr.size(); j++) {
                if (states[j] == States::Active)
                    printf("Seq: %d\n", getAck(arr[j]));   
            }
            printf("Broke on seq: %d, size: %d, newSize: %d\n", getAck(arr[i]), arr.size(), newSize);
            throw std::length_error("The new container size is not big enough for all elements from prev conteiner in ModQueue");
        }
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
    if (seq < first || seq >= first + arr.size() || states[seq % arr.size()] != States::Active)
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
bool ModQueue<T>::add(T elem, u32 size) {
    int seq = getAck(elem);
    int index = getIndex(seq);
    if (seq < first || seq > first + 2*arr.size()) {// windowUsed + size > window,     states[index] != States::Empty 
        // printf("Not added, seq: %d, size: %d, window: %d, index: %d, first: %d, arrSize: %d\n", seq, windowUsed+size, window, index, first, arr.size());
        return false;
    }
    if (states[index] != States::Empty) {
        if (seq < first + arr.size()) return false;
        printf("Resized called, old size: %d, first: %d, newSeq: %d\n", arr.size(), first, seq);
        resize(arr.size() * 3);
        index = getIndex(seq);
        printf("Resize called, new index: %d\n", index);
    }
    arr[index] = elem;
    states[index] = States::Active;
    elemCount++;
    // windowUsed += size;
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
    states[index] = States::Deleted;
    if (first == seq) updateFirstValue();
    return index;
}

template <typename T>
vector<T> ModQueue<T>::iniq(u16 seq) {
    vector<T> _deleted;
    for (int i=0; i<states.size(); i++) {
        if (states[i] == States::Empty) continue;
        if (states[i] == States::Active) {
            _deleted.push_back(arr[i]);
            elemCount--;
        }
        states[i] = States::Empty;
    }
    first = seq;
    return _deleted;
}

template <typename T> // no delete adopted for this func
void ModQueue<T>::initFirst(u16 seq) {
    if (elemCount != 0) 
        throw invalid_argument("The sent queue has messages so it cant change the first element");
    first = seq;
}

template <typename T>
u32 ModQueue<T>::getWindow() {
    return window;
}

template <typename T>
u32 ModQueue<T>::getWindowSize() {
    return window - windowUsed;
}

template <typename T>
void ModQueue<T>::setWindow(u32 size) {
    this->window = window;
}

template <typename T>
bool ModQueue<T>::isAddable(u16 size) {
    return window - windowUsed >= size;
}


SentMessagesQueue::SentMessagesQueue(int initCapacity, u32 window) : ModQueue(initCapacity, window) {}
SentMessagesQueue::~SentMessagesQueue() {
    for (int i=0; i<arr.size(); i++) {
        if (states[i] == States::Active) 
            free(arr[i].segment);
    }
}

void SentMessagesQueue::markAsProcessed(int seq, bool toFree) {
    int index = del(seq);
    dprintf("Marked as proceed %d\n", seq);
    windowUsed -= arr[index].segment->getFullLength() * (index >= 0);
    if (index >= 0 && toFree)
        free(arr[index].segment); 
}

DataSegmentDescriptor* SentMessagesQueue::add(DataSegmentDescriptor segment) {
    if (ModQueue<DataSegmentDescriptor>::add(segment, segment.segment->getFullLength())) 
        return &arr[getIndex(segment.segment->seq)];
    return NULL;
}

int SentMessagesQueue::getAck(DataSegmentDescriptor elem) {
    return elem.segment->seq;
}


ReceivedMessagesQueue::ReceivedMessagesQueue (int initCapacity, u32 window)
    : ModQueue(initCapacity, window) {}

int ReceivedMessagesQueue::getAck(DataSegment* elem) {
    return elem->seq;
}

ReceivedMessagesQueue::~ReceivedMessagesQueue() {
    for (int i=0; i<arr.size(); i++) 
        if (states[i] == States::Active)
            free(arr[i]);
}

pair<bool, vector<DataSegment*>> ReceivedMessagesQueue::add(DataSegment *elem) {
    printf("Sending seq: %d, size: %d, first: %d\n", elem->seq, arr.size(), first);
    if (!ModQueue<DataSegment*>::add(elem, elem->getFullLength())) 
        return {false, {}};
    if (elem->seq != first) return {true, {}};
    int n = arr.size();
    vector<DataSegment*> rez;
    for (; states[first%n] != States::Empty; first++) {
        if (states[first%n] == States::Active) {
            rez.push_back(arr[first%n]);
            windowUsed -= arr[first%n]->getFullLength();
        }
        states[first%n] = States::Empty;
    }
    return {true, rez};
}