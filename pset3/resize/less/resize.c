#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <ctype.h>

#include "bmp.h"

int main(int argc, char *argv[])
{
    // ensure proper usage
    if (argc != 4)
    {
        fprintf(stderr, "Usage: ./resize n infile outfile\n");
        return 1;
    }

    // remember resize factor n
    int n = atoi(argv[1]);

    // remember filenames
    char *infile = argv[2];
    char *outfile = argv[3];

    // open input file
    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", infile);
        return 2;
    }

    // open output file
    FILE *outptr = fopen(outfile, "w");
    if (outptr == NULL)
    {
        fclose(inptr);
        fprintf(stderr, "Could not create %s.\n", outfile);
        return 3;
    }

    // read infile's BITMAPFILEHEADER
    BITMAPFILEHEADER bf;
    fread(&bf, sizeof(BITMAPFILEHEADER), 1, inptr);

    // read infile's BITMAPINFOHEADER
    BITMAPINFOHEADER bi;
    fread(&bi, sizeof(BITMAPINFOHEADER), 1, inptr);

    // ensure infile is (likely) a 24-bit uncompressed BMP 4.0
    if (bf.bfType != 0x4d42 || bf.bfOffBits != 54 || bi.biSize != 40 ||
        bi.biBitCount != 24 || bi.biCompression != 0)
    {
        fclose(outptr);
        fclose(inptr);
        fprintf(stderr, "Unsupported file format.\n");
        return 4;
    }

    // store all old header info which we will change
    int oldWidth = bi.biWidth;
    int oldPadding = (4 - (oldWidth * sizeof(RGBTRIPLE)) % 4) % 4;
    int oldHeight = bi.biHeight;
    int oldSizeImage = bi.biSizeImage;
    int oldSize = bf.bfSize;

    // calculate and store new header info
    int newWidth = bi.biWidth * n;
    int newPadding = (4 - (newWidth * sizeof(RGBTRIPLE)) % 4) % 4;
    int newHeight = bi.biHeight * n;
    int newSizeImage = ((((newWidth * bi.biBitCount) + 31) & ~31) / 8) * abs(newHeight);
    int newSize = 54 + newWidth * abs(newHeight) * 3 + abs(newHeight) * newPadding;

    // update header info
    bi.biWidth = newWidth;
    bi.biHeight = newHeight;
    bi.biSizeImage = newSizeImage;
    bf.bfSize = newSize;


    // write outfile's BITMAPFILEHEADER
    fwrite(&bf, sizeof(BITMAPFILEHEADER), 1, outptr);

    // write outfile's BITMAPINFOHEADER
    fwrite(&bi, sizeof(BITMAPINFOHEADER), 1, outptr);


    // Go through reading each scanline
    for (int i = 0; i < abs(oldHeight); i++)
    {
        // process of reading and writing the line n times
        for (int j = 0; j < n; j++)
        {
            // go through each pixel to copy and write n times
            for  (int k = 0; k < oldWidth; k++)
            {
                // temporary triple
                RGBTRIPLE triple;

                fread(&triple, sizeof(RGBTRIPLE), 1, inptr);

                // Write the triple N times
                for (int l = 0; l < n; l++)
                {
                    fwrite(&triple, sizeof(RGBTRIPLE), 1, outptr);
                }
            }

            // add newPadding
            for (int k = 0; k < newPadding; k++)
            {
                fputc(0x00, outptr);
            }

            // Check whether we are on last one, and if not reset the file pointer
            if (j < n - 1)
            {
                fseek(inptr, -oldWidth * sizeof(RGBTRIPLE), SEEK_CUR);
            }
        }
        // skip reading the old padding once we are done reading/writing and ready to
        // move to the next line
        fseek(inptr, oldPadding, SEEK_CUR);

    }


    // close infile
    fclose(inptr);

    // close outfile
    fclose(outptr);

    // success
    return 0;
}