#include <cassert>
#include "string.h"
#include "math.h"
#include "fileFragment.h"
#include "data.h"
#include "windows.h"
using namespace std;

string FileDefragmentator::toSave = "D:/University/PKS/Protociol2/files";
bool setDefaultSavePath() {
    char modPath[MAX_PATH];
    GetModuleFileNameA(NULL, modPath, MAX_PATH);
    string dirPath = modPath;
    dirPath = dirPath.substr(0, dirPath.find_last_of("\\/"));
    dirPath.append("\\files");
    if (CreateDirectoryA(dirPath.c_str(), NULL) || GetLastError() == ERROR_ALREADY_EXISTS) {
        FileDefragmentator::toSave = dirPath;
        return true;
    }
    cout << "Error during default gateway folder creation: " << GetLastError() << "\n";
    return false;
}

FileFragmentator::FileFragmentator(FILE* file, string name) : file(file), sendSize(0), overhead(0) {
    headerTop = 0;

    u16 size = name.size();
    header = "";
    header.reserve(size+2);
    header.append(reinterpret_cast<char*>(&size), 2);
    header += name;
    printf("Header: %s, name: %s\n", header.c_str(), name.c_str());
}

FileFragmentator::~FileFragmentator() {
    if (file != NULL) {
        fclose(file);
        file = NULL;
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
        char last = fgetc(file);
        if (last == EOF) {
            u32 toDelete = seg->dataLength - red;
            seg->isNextFragment = false;
            seg->dataLength -= toDelete;
            seg = (DataSegment*)realloc(seg, seg->getFullLength());
        } else
            ungetc(last, file);
    }
    sendSize += seg->dataLength;
    overhead += seg->getFullLength() - seg->dataLength;
    return seg;
}

pair<u64, u64> FileFragmentator::getOverheads() {
    return {sendSize-header.size(), overhead+header.size()};
}

bool FileFragmentator::isFinished() {
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
}

pair<bool, DataSegment*> FileDefragmentator::addNextFrag(DataSegment* seg) {
    DefragmentatorI::addNextFrag(seg);
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
                filePath = FileDefragmentator::toSave + "\\" + fileName;
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
        printf("The file saved: %.*s, number of characters: %d\n", filePath.size(), filePath.c_str(), ftell(file));
        file = nullptr;
        return {true, nullptr};
    }
    return {false, nullptr};
}

pair<u64, u64> FileDefragmentator::getOverhead() {
    auto [size, overhead] = DefragmentatorI::getOverhead();
    return {size-bufferCap, overhead+bufferCap};
}