#include <string.h>
#include "data.h"
#include "types.h"
using namespace std;

void printData(DataSegment *segment) {
    printf("ACK: %d\nLength: %d\nType: %d\nData: ", segment->seq, segment->dataLength, segment->type);
    char *data = reinterpret_cast<char*>(segment) + sizeof(DataSegment);
    for (int i=0; i<segment->dataLength; i++)
        printf("(%d %c), ", data[i], data[i]);
    printf("\n");
}

DataSegment* createDataSegment(DataTypes type, bool isNextFrag, int buffer) {
    DataSegment* segment = reinterpret_cast<DataSegment*>(malloc (sizeof(DataSegment) + buffer));
    segment->dataLength = buffer;
    segment->isNextFragment = isNextFrag;
    segment->type = type;
    segment->seq = 0;
    return segment;
}

u32 ipToInt(string ip) {
    u32 a, b, c, d;
    sscanf(ip.c_str(), "%u.%u.%u.%u", &a, &b, &c, &d);
    return (a << 24) | (b << 16) | (c << 8) | d;
}

string ipToStr(u32 ip) {
    char buffer[16];
    snprintf(buffer, 16, "%u.%u.%u.%u", ip >> 24, ip >> 16 & 0xFF, ip >> 8 & 0xFF, ip & 0xFF);
    return string(buffer);
}