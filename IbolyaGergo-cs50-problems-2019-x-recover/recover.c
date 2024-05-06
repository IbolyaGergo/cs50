#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
    // ensure proper usage
    if (argc != 2)
    {
        fprintf(stderr, "Usage: recover file\n");
        return 1;
    }

    // remember memory card filename
    char *infile = argv[1];

    // open memory card file for reading
    FILE *inptr = fopen(infile, "r");

    // file must exist
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", infile);
        return 2;
    }

    // number of jpg files found
    int numjpg = 0;

    // temporary storage of blocks
    unsigned char buffer[520];
    int read = 512;

    // array storing the name of jpg files
    char filename[8];

    // creating a pointer to our jpg file
    FILE *img;

    // number of bytes read into the buffer must be equal to the size of a block(512 bytes)
    while (read == 512)
    {
        // read 1 block from memory card to a buffer
        read = fread(buffer, 1, 512, inptr);

        // check if in the current block is the start of a jpg
        if (buffer [0] == 0xff &&
            buffer [1] == 0xd8 &&
            buffer [2] == 0xff &&
            (buffer [3] & 0xf0) == 0xe0)
        {
            // close image file if there is any
            if (numjpg > 0)
            {
                fclose(img);
            }

            // create a new jpg file
            sprintf(filename, "%03i.jpg", numjpg);
            img = fopen(filename, "w");
            // writing the data from the buffer to the jpg file
            fwrite(buffer, 1, 512, img);
            // increment the number of files
            numjpg++;
        }
        // if already found a jpg, continue writing blocks in it
        else if (numjpg > 0 && read == 512)
        {
            fwrite(buffer, 1, 512, img);
        }
    }
    fclose(inptr);
    fclose(img);
    return 0;
}
