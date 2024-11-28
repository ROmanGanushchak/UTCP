#ifndef FILE_FRAGMENTATOR_H
#define FILE_FRAGMENTATOR_H
#include <iostream>
#include <stdio.h>

#include "types.h"
#include "data.h"
#include "fragmentator.h"

class FileFragmentator : public FragmentatorI {
private:
    FILE *file;
    std::string header;
    u16 headerTop;
    u64 sendSize; u64 overhead;
public:
    FileFragmentator(FILE* file, std::string name);
    ~FileFragmentator();
    std::pair<u64, u64> getOverheads() override;
    DataSegment* getNextFragment(u16 maxSize) override;
    bool isFinished() override;
};

class FileDefragmentator : public DefragmentatorI {
private:
    char *buffer;
    u16 bufferTop;
    u16 bufferCap;
    FILE* file;
    std::string filePath;
public:
    static std::string toSave;
    FileDefragmentator();
    ~FileDefragmentator();
    std::pair<bool, DataSegment*> addNextFrag(DataSegment* data);
    std::pair<u64, u64> getOverhead() override;
};

bool setDefaultSavePath();

#endif