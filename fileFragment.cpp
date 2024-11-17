#include "string.h"
#include "math.h"
#include "fileFragment.h"
#include "data.h"
using namespace std;

string FileDefragmentator::toSave = "D:/University/PKS/Protociol2/files";

FileFragmentator::FileFragmentator(string filePath) {
    printf("%s", filePath.c_str());
    cout << filePath << endl;
    file = fopen(filePath.c_str(), "rb");
    if (file == NULL) {
        printf("Failed to open the file.\n");
        return;
    }
    fseek(file, 0, SEEK_END);
    fileSize = ftell(file);
    fseek(file, 0, SEEK_SET);
    headerTop = 0;

    size_t pos = filePath.rfind('/');
    if (pos == std::string::npos) pos = -1;
    string name = filePath.substr(pos+1);
    u16 size = name.size();
    header.assign(name.size()+2, '0');
    memcpy(header.data(), (char*)&size, sizeof(size));
    strcpy(header.data()+2, name.c_str());
}

FileFragmentator::~FileFragmentator() {
    if (file != NULL) 
        fclose(file);
}

DataSegment* FileFragmentator::getNextFragment(u16 seq, u16 dataSize) {
    int top = ftell(file);
    bool isFirst = top == 0 && headerTop == 0;
    Seg seg;
    printf("Header size: %d, top: %d\n", header.size(), headerTop);
    if (headerTop < header.size()) {
        seg = getSeg(seq, isFirst ? DataTypes::File : DataTypes::PureData, 
            true, header.size()-headerTop, dataSize);
        memcpy(seg.data, header.data()+headerTop, seg.dataSize);
        headerTop += seg.dataSize;
    } else {
        seg = getSeg(seq, isFirst ? DataTypes::File : DataTypes::PureData, false, fileSize-top, dataSize);
        size_t bytesRead = fread(seg.data, 1, seg.dataSize, file);
        seg.seg->isNextFragment = ftell(file) != fileSize;
    }
    initCrc(seg.seg);
    printf("For seq: %d, is next: %d, %d, %d\n", seg.seg->seq, seg.seg->isNextFragment);
    printf("First bait: %hhu, second: %hhu\n", ((char*)seg.seg->getExtraData())[0], ((char*)seg.seg->getExtraData())[1]);
    printf("Header: %hhu, %hhu\n", header[0], header[1]);
    return seg.seg;
}

bool FileFragmentator::isFinished() {
    printf("On finish check -> %d %d\n", ftell(file), fileSize);
    return ftell(file) == fileSize;
}


FileDefragmentator::FileDefragmentator() : file(NULL), bufferTop(0) {
    buffer = (char*) malloc (sizeof(FileHeader));
    bufferCap = sizeof(FileHeader);
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
    char *data = (char*) seg->getExtraData();
    u16 size = seg->dataLength;
    printf("buffer: %d %d\n", bufferTop, bufferCap);
    while (bufferTop != bufferCap) {
        u16 _size = _min(size, bufferCap-bufferTop);
        memcpy(buffer+bufferTop, data, _size);
        bufferTop += _size;
        printf("buffer1: %d %d\n", bufferTop, bufferCap);
        if (bufferTop == bufferCap) {
            printf("Level up\n");
            u16 nameSize = ((FileHeader*)buffer)->fileNameLength;
            printf("nameSize: %hu\n", nameSize);
            if (bufferCap == sizeof(FileHeader)) {
                bufferCap += nameSize;
                buffer = (char*) realloc(buffer, bufferCap);
            } else {
                string fileName(buffer + sizeof(FileHeader), nameSize);
                filePath = FileDefragmentator::toSave + '/' + fileName;
                file = fopen(filePath.c_str(), "wb");
                printf("openning file in: %s\n", filePath.c_str());
            }
            data = data + _size;
            size -= _size;
        } else break;
    }
    if (file) fwrite(data, sizeof(char), size, file);
    if (!seg->isNextFragment) {
        file = NULL;
        printf("The file saved: %s\n", filePath.c_str());
        return {true, NULL};
    }
    printf("Received fragment of file %hu\n", seg->seq);
    return {false, NULL};
}