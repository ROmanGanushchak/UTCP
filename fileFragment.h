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
    u64 fileSize;
    std::string header;
    u16 headerTop;
public:
    FileFragmentator(FILE* file, std::string name);
    ~FileFragmentator();
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
};

#endif