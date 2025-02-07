#ifndef PURE_DATA
#define PURE_DATA

#include <string>
#include <vector>
#include <utility>
#include <cstddef>
#include <cstdint>
#include "types.h"
#include <list>

enum class DataTypes : uint8_t {
    PureData = 0,
    Resend = 1,
    KeepAlive = 2,
    ACK = 3,
    Connection = 4,
    ConnectionApproval = 5,
    EndConnection = 6,
    String = 7,
    File = 8,
    UnKnown = 255,
};

struct DataSegment {
    u16 crc;
    u16 dataLength;
    u16 seq;
    DataTypes type;
    bool isNextFragment;
    u16 window;

    void* getExtraData() {
        return reinterpret_cast<void*>(this + 1);
    }
    int getFullLength() {
        return sizeof(DataSegment) + dataLength;
    }
};

typedef struct {
    u16 seq;
    int64_t endTime;
} TimerUnit;

typedef struct {
    DataSegment* segment;
    std::list<TimerUnit>::iterator timer;
    int sentCount;
} DataSegmentDescriptor;

struct FileHeader {
    u16 fileNameLength;
};

DataSegment* createDataSegment(DataTypes type, bool isNextFrag=false, int buffer=0);
DataSegment* getSeg(int seq, DataTypes type, bool isNext, u32 wantedSize, u32 maxSize=UINT_MAX);
#endif