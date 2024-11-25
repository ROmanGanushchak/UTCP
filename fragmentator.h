#ifndef FRAGMENTATOR_H
#define FRAGMENTATOR_H
#include <chrono>
#include "unordered_map"
#include "types.h"
#include "data.h"
#include "crc.h"

class FragmentatorI {
public:
    virtual DataSegment* getNextFragment(u16 maxSize) = 0;
    virtual bool isFinished() = 0;
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
private:
    std::unordered_map<int, int> sizes;
    u64 start;
public:
    DefragmentatorI() {
        auto nowFullTime = std::chrono::system_clock::now();
        start = std::chrono::duration_cast<std::chrono::milliseconds>(nowFullTime.time_since_epoch()).count();
    }
    virtual std::pair<bool, DataSegment*> addNextFrag(DataSegment* data) {
        sizes[data->dataLength]++;
        return {false, NULL};
    }
    virtual ~DefragmentatorI() {
        auto nowFullTime = std::chrono::system_clock::now();
        u64 now = std::chrono::duration_cast<std::chrono::milliseconds>(nowFullTime.time_since_epoch()).count();
        printf("The time of transfer the time taken: %lf\nThe sizes of the fragments (size, count): ", (now - start) / (double)1000);
        for (auto elem : sizes) 
            printf("(%d %d) ", elem.first, elem.second);
        printf("\n");
    }
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