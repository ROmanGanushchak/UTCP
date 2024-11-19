#include "string.h"
#include "math.h"
#include "fileFragment.h"
#include "data.h"
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
    if (file != NULL) 
        fclose(file);
}

DataSegment* FileFragmentator::getNextFragment(u16 dataSize) {
    u64 top = ftell(file);
    bool isFirst = top == 0 && headerTop == 0;
    Seg seg;
    if (headerTop < header.size()) {
        seg = getSeg(0, isFirst ? DataTypes::File : DataTypes::PureData, 
            true, header.size()-headerTop, dataSize);
        if (seg.seg == NULL) return NULL;
        memcpy(seg.data, header.data()+headerTop, seg.dataSize);
        headerTop += seg.dataSize;
    } else {
        seg = getSeg(0, isFirst ? DataTypes::File : DataTypes::PureData, false, fileSize-top, dataSize);
        if (seg.seg == NULL) return NULL;
        printf("Allowed space: %d, allocated space: %d\n", dataSize, seg.dataSize);
        size_t bytesRead = fread(seg.data, 1, seg.dataSize, file);
        seg.seg->isNextFragment = ftell(file) != fileSize;
    }
    // printf("SENDING %d: %.*s\n", seg.seg->seq, seg.seg->dataLength, (char*)seg.seg->getExtraData());
    if (!seg.seg->isNextFragment) printf("It is last fragment");
    return seg.seg;
}

bool FileFragmentator::isFinished() {
    printf("On finish check -> %llu %llu, remainingBaits: %d, isFinished: %d\n", ftell(file), fileSize, getRemainingBaits(file),  feof(file));
    return ftell(file) == fileSize;
}


FileDefragmentator::FileDefragmentator() : file(NULL), bufferTop(0) {
    bufferCap = sizeof(FileHeader);
    buffer = (char*) malloc (bufferCap);
}
FileDefragmentator::~FileDefragmentator() {
    free(buffer);
    if (file) {
        fflush(file);
        if (ferror(file)) printf("Error flushing file!\n");
        fclose(file);
        file = NULL;
    }
    printf("The file receiption clear was called, the new file val: %d\n", file);
}

pair<bool, DataSegment*> FileDefragmentator::addNextFrag(DataSegment* seg) {
    // printf("DataReceived %d: %.*s\n!!!END!!!\n", seg->seq, seg->dataLength, (char*)seg->getExtraData());
    char *data = (char*) seg->getExtraData();
    u16 size = seg->dataLength;
    printf("Buffer Data: %d %d\n", bufferTop, bufferCap);
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
    printf("FILE: %p\n", file);
    if (file) {fwrite(data, sizeof(char), size, file); fflush(file);}
    if (!seg->isNextFragment) {
        file = NULL;
        printf("The file saved: %s\n", filePath.c_str());
        return {true, NULL};
    }
    // printf("Received fragment of file %hu\n", seg->seq);
    return {false, NULL};
}