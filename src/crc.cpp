#include <cstring>
#include <iostream>
#include "crc.h"
using namespace std;

u16 getCrc(char* data, int size) {
    u16 crc = 0;
    for (int i=0; i<size; i++) {
        crc ^= data[i];
        for (int q=0; q<8; q++) {
            if (crc & 0x8000) crc = (crc << 1) ^ generator;
            else crc <<= 1;
        }
    }
    return crc;
}

bool checkCrc(DataSegment *seg) {
    return seg->crc == getCrc(((char*)seg)+4, seg->dataLength + sizeof(DataSegment) - 4);
}

void initCrc(DataSegment* seg) {
    seg->crc = getCrc(((char*)seg)+4, seg->dataLength + sizeof(DataSegment) - 4);
}