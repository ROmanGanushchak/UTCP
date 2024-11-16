#include <math.h>
#include <algorithm>

#include "fragmentator.h"
#include "data.h"
#include "structs.hpp"
using namespace std;

Fragmentator::Fragmentator(char* data, u16 size, DataTypes type, bool isHeader) {
    this->data = data;
    this->size = size;
    this->type = type;
    this->top = 0;
    this->fragmentSize = USHRT_MAX;
    this->isHeader = isHeader;
}

Fragmentator::~Fragmentator() {
    dprintf("Called fragment deconstructor\n");
    if (this->data) {
        free(this->data);
        this->data = NULL;
    }
}

Fragmentator::Fragmentator(Fragmentator&& other) noexcept : data(other.data) {
    other.data = nullptr; 
    dprintf("The ownership of Fragment was moved\n");
}

u16 Fragmentator::activate(u16 seq, u16 fragmentSize) {
    this->seq = seq;
    this->fragmentSize = fragmentSize;
    return _max(ceil((this->size-sizeof(DataSegment)*isHeader) / ((double)fragmentSize)), 1);
}

DataSegment* Fragmentator::getNextFragment() {
    DataSegment* seg; u16 size; bool isFirst = top == 0;
    if (isFirst && isHeader && fragmentSize+sizeof(DataSegment) >= this->size) {
        size = this->size - sizeof(DataSegment);
        top = sizeof(DataSegment);
        seg = reinterpret_cast<DataSegment*>(data);   
        this->data = NULL;
    } else {
        if (isFirst) top = sizeof(DataSegment);
        size = _min(fragmentSize, this->size-top);
        seg = createDataSegment(type, top+size == this->size, size);
        memcpy((char*)seg->getExtraData(), data+top, size);
    }
    seg->seq = this->seq++;
    seg->dataLength = size;
    seg->type = isFirst ? type : DataTypes::PureData;
    seg->isNextFragment = top + size != this->size;
    initCrc(seg);
    top += size;
    return seg;
}

bool Fragmentator::isFinished() {
    return size == top;
}

bool Fragmentator::isActivated() {
    return fragmentSize != USHRT_MAX;
}


Defragmentator::Defragmentator() : data(NULL), size(0), cap(0) {}

void Defragmentator::addData(char* data, int size) {
    if (this->size + size > cap) {
        this->cap = this->size + size;
        this->data = (char*) realloc(this->data, this->cap);
    }
    memcpy(this->data + this->size, data, size);
    this->size += size;
}

pair<bool, DataSegment*> Defragmentator::addNextFrag(DataSegment* data) {
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