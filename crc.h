#ifndef CRC_H
#define CRC_H
#include "types.h"

constexpr u16 generator = 1 << 15 | 1 << 4 | 1 << 1;
u16 getCrc(char* data, int size);
bool checkCrc(u16 crc, char *data, int size);

#endif