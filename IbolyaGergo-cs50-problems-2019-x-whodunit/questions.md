# Questions

## What's `stdint.h`?

Declares sets of integer types having specified widths.

## What's the point of using `uint8_t`, `uint32_t`, `int32_t`, and `uint16_t` in a program?

We can manage the memory usage, if we know, how many bits do we need to represent integers.

## How many bytes is a `BYTE`, a `DWORD`, a `LONG`, and a `WORD`, respectively?

1, 4, 4, 2.

## What (in ASCII, decimal, or hexadecimal) must the first two bytes of any BMP file be? Leading bytes used to identify file formats (with high probability) are generally called "magic numbers."

Specify the size of the file.

## What's the difference between `bfSize` and `biSize`?

bfSize - size, in bytes, of the bitmap file
biSize - the number of bytes required by the structure

## What does it mean if `biHeight` is negative?

The bitmap is a top-down DIB and its origin is the upper-left corner.

## What field in `BITMAPINFOHEADER` specifies the BMP's color depth (i.e., bits per pixel)?

biBitCount

## Why might `fopen` return `NULL` in `copy.c`?

Input file cannot be found.

## Why is the third argument to `fread` always `1` in our code?

1 file needs to be readed.

## What value does `copy.c` assign to `padding` if `bi.biWidth` is `3`?

3

## What does `fseek` do?

Sets the file position to a given offset.

## What is `SEEK_CUR`?

Current position of the file pointer.
