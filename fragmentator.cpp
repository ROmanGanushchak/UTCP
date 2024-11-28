#include <math.h>
#include <algorithm>

#include "fragmentator.h"
#include "data.h"
#include "structs.hpp"
using namespace std;

Fragmentator::Fragmentator(char* data, u32 size, DataTypes type, bool isHeader): sentSize(0), overhead(0) {
    this->data = data;
    this->size = size;
    this->type = type;
    this->top = 0;
    this->isHeader = isHeader;
}

Fragmentator::~Fragmentator() {
    if (this->data) {
        free(this->data);
        this->data = NULL;
    }
}

DataSegment* Fragmentator::getNextFragment(u16 maxSize) {
    DataSegment* seg; u16 size; bool isFirst = top == 0;
    if (isFirst && isHeader && maxSize+sizeof(DataSegment) >= this->size) {
        size = this->size - sizeof(DataSegment);
        top = sizeof(DataSegment);
        seg = reinterpret_cast<DataSegment*>(data);   
        this->data = NULL;
    } else {
        if (isFirst && isHeader) top = sizeof(DataSegment);
        size = _min(maxSize, this->size-top);
        seg = createDataSegment(type, false, size);
        memcpy((char*)seg->getExtraData(), data+top, size);
    }
    seg->dataLength = size;
    seg->type = isFirst ? type : DataTypes::PureData;
    seg->isNextFragment = top + size != this->size;
    top += size;
    sentSize += seg->dataLength;
    overhead += seg->getFullLength() - seg->dataLength;
    return seg;
}

bool Fragmentator::isFinished() {
    return size == top;
}

pair<u64, u64> Fragmentator::getOverheads() {
    return {sentSize, overhead};
}


Defragmentator::Defragmentator() : data(NULL), size(0), cap(0) {}
Defragmentator::~Defragmentator() {
    if (data) free(data);
}

void Defragmentator::addData(char* data, int size) {
    if (this->size + size > cap) {
        this->cap = this->size + size;
        this->data = (char*) realloc(this->data, this->cap);
    }
    memcpy(this->data + this->size, data, size);
    this->size += size;
}

pair<bool, DataSegment*> Defragmentator::addNextFrag(DataSegment* data) {
    DefragmentatorI::addNextFrag(data);
    dprintf("Defragmentator Received: type: %d, isNext: %d\n", data->type, data->isNextFragment);
    if (data->type != DataTypes::PureData && !data->isNextFragment) {
        this->data = NULL;
        return {true, reinterpret_cast<DataSegment*>(data)};
    }
    if (data->type != DataTypes::PureData)
        addData(reinterpret_cast<char*>(data), sizeof(DataSegment));
    addData((char*)data->getExtraData(), data->dataLength);
    if (data->isNextFragment) return {false, NULL};
    auto temp = reinterpret_cast<DataSegment*>(this->data);
    temp->dataLength = size - sizeof(DataSegment);
    this->data = NULL;
    return {true, temp};
}

DataSegment* Defragmentator::get() {
    return reinterpret_cast<DataSegment*>(data);
}


NoFragmentator::NoFragmentator(DataSegment* seg) {
    this->seg = seg;
    seg->seq = 0;
}
NoFragmentator::~NoFragmentator() {
    if (seg) {free(seg); seg=NULL;}
}

DataSegment* NoFragmentator::getNextFragment(u16 size) {
    auto temp = seg;
    seg = NULL;
    return temp;
}

pair<u64, u64> NoFragmentator::getOverheads() {
    return {INT_MAX, INT_MAX};
}

bool NoFragmentator::isFinished() {
    return seg == NULL;
}