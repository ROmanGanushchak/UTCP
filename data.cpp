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

Seg getSeg(int seq, DataTypes type, bool isNext, u32 wantedSize, u32 maxSize) {
    u32 size = _min(maxSize, wantedSize);
    DataSegment* seg = (DataSegment*)malloc (sizeof(DataSegment)+size);
    if (seg == NULL) return (Seg){.seg=NULL, .data=NULL, .dataSize=0};
    *seg = (DataSegment){.dataLength=size, .seq=seq, .type=type, .isNextFragment=isNext};
    return (Seg){.seg=seg, .data=((char*)seg)+sizeof(DataSegment), size};
}
