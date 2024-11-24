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
    assert(arr.size() == states.size() && "Arr and States sizes have to be the same");
    if (states[first%arr.size()] == States::Empty) {
        arr.resize(newSize);
        states.resize(newSize, States::Empty);
        return;
    }
    vector<States> newStates(newSize, States::Empty);
    vector<T> newArr(newSize);
    for (int i=0; i<arr.size(); i++) {
        if (states[i] != States::Active && states[i] != States::Suppresed) continue;
        int index = getSeq(arr[i]) % newSize;
        if (newStates.at(index) != States::Empty) {
            for (int j=0; j<arr.size(); j++) {
                if (states[j] == States::Active)
                    printf("Seq: %d\n", getSeq(arr[j]));   
            }
            printf("Broke on seq: %d, size: %d, newSize: %d\n", getSeq(arr[i]), arr.size(), newSize);
            throw std::length_error("The new container size is not big enough for all elements from prev conteiner in ModQueue");
        }
        newStates[index] = states[i];
        newArr[index] = arr[i];
    }
    states = std::move(newStates);
    arr = std::move(newArr);
}

template <typename T>
int ModQueue<T>::getIndex(int seq) {
    if (seq < first || seq > first + arr.size())
        return -2;
    return seq % arr.size();
}

template <typename T>
pair<T*, States> ModQueue<T>::get(int seq) {
    if (seq < first || seq >= first + arr.size() || 
        states[seq % arr.size()] != States::Active || getSeq(arr[seq%arr.size()]) != seq)
        return {NULL, States::Empty};
    return {&arr[seq % arr.size()], States::Active};
}

template <typename T>
void ModQueue<T>::updateFirstValue() {
    int n = arr.size(), start = first;
    for (; first - n != start && states[first%n] == States::Deleted; first++) 
        states[first%n] = States::Empty;
}

template <typename T>
AddingStates ModQueue<T>::add(T elem, u32 size) {
    if (windowUsed + size > window) return NoSize;
    int seq = getSeq(elem);
    int index = seq % arr.size();
    if (seq < first || seq > first + 2*arr.size() || 
        ((states[index] == States::Active || states[index] == States::Suppresed) && seq == getSeq(arr[index]))) 
        return Incorrect;
    if (states[index] != States::Empty) {
        if (seq < first + arr.size()) return NoSize;
        resize(arr.size() * 2);
        index = getIndex(seq);
        assert(states[index] == States::Empty);
    }
    arr[index] = elem;
    states[index] = States::Active;
    elemCount++;
    windowUsed += size;
    return Added;
}

template <typename T>
int ModQueue<T>::del(int seq) {
    int index = getIndex(seq);
    if (index < 0 || states[index] != States::Active)
        return -1;
    dprintf("Del at index: %d, first: %d, with seq: %d\n", index, first, seq);
    states.at(index) = States::Deleted;
    elemCount--;
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

template <typename T>
int ModQueue<T>::getFirst() {
    return first;
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
    if (index < 0) return;
    dprintf("Marked as proceed %d\n", seq);
    windowUsed -= arr[index].segment->getFullLength() * (index >= 0);
    if (toFree) free(arr[index].segment);
}

bool SentMessagesQueue::changeState(int seq, States state) {
    if (seq < first || seq > first + arr.size()) return false;
    int index = getIndex(seq);
    if (index < 0 || states[index] == States::Deleted || states[index] == States::Empty) return false;
    states[index] = state;
    return true;
}

pair<AddingStates, DataSegmentDescriptor*> SentMessagesQueue::add(DataSegmentDescriptor segment) {
    AddingStates state = ModQueue<DataSegmentDescriptor>::add(segment, segment.segment->getFullLength());
    if (state != Added) return {state, nullptr};
    return {Added, &arr[getIndex(segment.segment->seq)]};
}

int SentMessagesQueue::getSeq(DataSegmentDescriptor elem) {
    return elem.segment->seq;
}


ReceivedMessagesQueue::ReceivedMessagesQueue (int initCapacity, u32 window)
    : ModQueue(initCapacity, window) {}

int ReceivedMessagesQueue::getSeq(DataSegment* elem) {
    return elem->seq;
}

ReceivedMessagesQueue::~ReceivedMessagesQueue() {
    for (int i=0; i<arr.size(); i++) 
        if (states[i] == States::Active)
            free(arr[i]);
}

pair<bool, vector<DataSegment*>> ReceivedMessagesQueue::add(DataSegment *elem) {
    if (ModQueue<DataSegment*>::add(elem, elem->getFullLength()) != Added) 
        return {false, {}};
    if (elem->seq != first) return {true, {}};
    int n = arr.size();
    vector<DataSegment*> rez;
    for (; states[first%n] != States::Empty && states[first%n] != States::Suppresed; first++) {
        if (states[first%n] == States::Active) {
            rez.push_back(arr[first%n]);
            windowUsed -= arr[first%n]->getFullLength();
        }
        states[first%n] = States::Empty;
    }
    return {true, rez};
}