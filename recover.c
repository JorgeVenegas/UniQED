#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./recover image\n");
        return 1;
    }

    FILE *infile = fopen(argv[1], "r");
    if (file == NULL)
    {
        printf("Could not open %s.\n", infile);
        return 4;
    }

    FILE *outfile;

    const int blockSize = 512;
    bool foundFirstJpeg = false;
    int jpegCount = 0;
    BYTE buffer[blockSize];
    while (fread(buffer, blockSize, 1, infile)) // Read from the 512 B block
    {
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0) // Check if it is a .jpeg
        {
            if(!foundFirstJepg) // Check if it is the first .jpeg
            {
                foundFirstJpeg = true;
            }
            else // If it is not first .jpeg but has already found jpeg then close previous jpeg file
            {
                fclose(outfile);
            }

            char fileName[8];
            sprintf(filename, "%03i.jpg", jpegCount++); // Format the name of the output jpeg file
            outfile = fopen(filename, "w"); // Create jpeg file with filename previously formatted
            if (outfile == NULL)
            {
                return 1;
            }
            fwrite(buffer, blockSize, 1, outfie); // Write data in outfile
        }
        else if(foundFirstJpeg) // If we have found the first jpeg and it is not the beggining of a new jpeg, keep writing on the first one.
        {
            fwrite(buffer, blockSize, 1, outfie);
        }
    }
    fclose(infile);
    fclose(outfile);
}