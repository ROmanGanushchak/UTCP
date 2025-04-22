#ifndef CRC_H
#define CRC_H
#include "types.h"
#include "data.h"

constexpr u16 generator = 1 << 15 | 1 << 4 | 1 << 1;
u16 getCrc(char* data, int size);
bool checkCrc(DataSegment *seg);
void initCrc(DataSegment* seg);

#endif