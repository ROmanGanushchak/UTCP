#ifndef FRAGMENTATOR_H
#define FRAGMENTATOR_H
#include "types.h"
#include "data.h"
#include "crc.h"

class Fragmentator {
private:
    u32 top;
    u16 seq;
    char *data;
    u16 size;
    DataTypes type;
    bool isHeader;
public:
    u16 fragmentSize;
    Fragmentator(char* data, u16 size, DataTypes type, bool isHeader=false);
    ~Fragmentator();
    Fragmentator(Fragmentator&& other) noexcept;
    u16 activate(u16 seq, u16 fragmentSize);
    DataSegment* getNextFragment();
    bool isFinished();
    bool isActivated();
};

class Defragmentator {
private:
    char *data;
    int size;
    int cap;
    void addData(char* data, int size);
public:
    Defragmentator();
    std::pair<bool, DataSegment*> addNextFrag(DataSegment* data);
    DataSegment* get();
};

// add file de/fragmentator
#endif