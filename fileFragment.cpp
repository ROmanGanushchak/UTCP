#include "string.h"
#include "math.h"
#include "fileFragment.h"
#include "data.h"
#include <cassert>
using namespace std;

u32 getRemainingBaits(FILE* file) {
    long currentPos = ftell(file);
    fseek(file, 0, SEEK_END);
    long endPos = ftell(file);
    fseek(file, currentPos, SEEK_SET);
    return endPos - currentPos;
}

string FileDefragmentator::toSave = "D:/University/PKS/Protociol2/files";

FileFragmentator::FileFragmentator(FILE* file, string name) : file(file) {
    copy = fopen("D:/University/PKS/Protociol2/files/copy.py", "wb");

    fseek(file, 0, SEEK_END);
    fileSize = ftell(file);
    fseek(file, 0, SEEK_SET);
    headerTop = 0;

    u16 size = name.size();
    header.assign(name.size()+2, '0');
    memcpy(header.data(), (char*)&size, sizeof(size));
    strcpy(header.data()+2, name.c_str());
}

FileFragmentator::~FileFragmentator() {
    printf("FileDefragCalled\n");
    if (file != NULL) {
        fclose(file);
        file = NULL;
    }
    if (copy) {
        fclose(copy); 
        copy=NULL;
    }
}

DataSegment* FileFragmentator::getNextFragment(u16 dataSize) {
    u64 top = ftell(file);
    bool isFirst = top == 0 && headerTop == 0;
    DataSegment* seg;
    if (headerTop < header.size()) {
        seg = getSeg(0, isFirst ? DataTypes::File : DataTypes::PureData, true, header.size()-headerTop, dataSize);
        if (seg == NULL) return NULL;
        memcpy(seg->getExtraData(), header.data()+headerTop, seg->dataLength);
        headerTop += seg->dataLength;
    } else {
        seg = getSeg(0, isFirst ? DataTypes::File : DataTypes::PureData, true, dataSize);
        if (seg == NULL) return NULL;
        size_t red = fread(seg->getExtraData(), 1, seg->dataLength, file);
        assert(red <= dataSize && "More baits where rad from file then allowed");
        fwrite(seg->getExtraData(), 1, red, copy);
        char last = fgetc(file);
        if (last == EOF) {
            u32 toDelete = seg->dataLength - red;
            seg = (DataSegment*)realloc(seg, seg->getFullLength()-toDelete);
            seg->dataLength -= toDelete; 
            seg->isNextFragment = false;
        } else
            ungetc(last, file);
    }
    return seg;
}

bool FileFragmentator::isFinished() {
    // printf("On finish check -> %llu %llu, remainingBaits: %d, isFinished: %d\n", ftell(file), fileSize, getRemainingBaits(file),  feof(file) != 0);
    return feof(file) != 0;
}


FileDefragmentator::FileDefragmentator() : file(NULL), bufferTop(0) {
    bufferCap = sizeof(FileHeader);
    buffer = (char*) malloc (bufferCap);
}
FileDefragmentator::~FileDefragmentator() {
    if (buffer) {
        free(buffer);
        buffer = NULL;
    }
    if (file) {
        fflush(file);
        if (ferror(file)) printf("Error flushing file!\n");
        fclose(file);
        file = NULL;
    }
    printf("The file receiption clear was called, the new file val: %p\n", file);
}

pair<bool, DataSegment*> FileDefragmentator::addNextFrag(DataSegment* seg) {
    char *data = (char*) seg->getExtraData();
    u16 size = seg->dataLength;
    while (bufferTop != bufferCap) {
        u64 _size = _min(size, bufferCap-bufferTop);
        memcpy(buffer+bufferTop, data, _size);
        bufferTop += _size;
        if (bufferTop == bufferCap) {
            u16 nameSize = ((FileHeader*)buffer)->fileNameLength;
            printf("Name size: %d, buffer cap: %d\n", nameSize, bufferCap);
            if (bufferCap == sizeof(FileHeader)) {
                bufferCap += nameSize;
                buffer = (char*) realloc(buffer, bufferCap);
            } else {
                string fileName(buffer + sizeof(FileHeader), nameSize);
                filePath = FileDefragmentator::toSave + '/' + fileName;
                file = fopen(filePath.c_str(), "wb");
                if (file == NULL) 
                    printf("File was not opened\n");
                printf("openning file in: %s\n", filePath.c_str());
            }
            data = data + _size;
            size -= _size;
        } else break;
    }
    if (file) {
        fwrite(data, sizeof(char), size, file); 
        fflush(file);
    }
    if (!seg->isNextFragment) {
        file = NULL;
        printf("The file saved: %s\n", filePath.c_str());
        return {true, NULL};
    }
    return {false, NULL};
}