#ifndef FRAGMENTATOR_H
#define FRAGMENTATOR_H
#include "types.h"
#include "data.h"
#include "crc.h"

class FragmentatorI {
public:
    virtual DataSegment* getNextFragment(u16 maxSize) = 0;
    virtual bool isFinished() = 0;
    virtual ~FragmentatorI() = default;
};

class Fragmentator : public FragmentatorI {
private:
    u32 top;
    char *data;
    u32 size;
    DataTypes type;
    bool isHeader;
public:
    Fragmentator(char* data, u32 size, DataTypes type, bool isHeader=false);
    ~Fragmentator();
    DataSegment* getNextFragment(u16 maxSize) override;
    bool isFinished() override;
};

class NoFragmentator : public FragmentatorI {
private:
    DataSegment* seg;
public:
    NoFragmentator(DataSegment *seg);
    ~NoFragmentator();
    DataSegment* getNextFragment(u16 maxSize) override;
    bool isFinished() override;
};

class DefragmentatorI {
public:
    virtual std::pair<bool, DataSegment*> addNextFrag(DataSegment* data) = 0;
    virtual ~DefragmentatorI() = default;
};

class Defragmentator : public DefragmentatorI {
private:
    char *data;
    int size;
    int cap;
    void addData(char* data, int size);
public:
    Defragmentator();
    ~Defragmentator();
    std::pair<bool, DataSegment*> addNextFrag(DataSegment* data);
    DataSegment* get();
};

// add file de/fragmentator
#endif