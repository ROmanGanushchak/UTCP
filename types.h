#ifndef TYPES_H
#define TYPES_H

#define uint unsigned int
#define u8 unsigned char
#define u16 unsigned short
#define u32 unsigned int
#define u64 unsigned long long int
#define i32 int
#define i16 short
#define f32 float
#define f64 double
#define uchar unsigned char
#define DEBUG_PRINT false
#define _min(a, b) (((a) < (b)) ? (a) : (b))
#define _max(a, b) (((a) > (b)) ? (a) : (b))

#if DEBUG_PRINT
    #define dprintf(fmt, ...) printf(fmt, ##__VA_ARGS__)
#else
    #define dprintf(fmt, ...) // No operation
#endif

#endif