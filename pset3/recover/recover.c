#include <stdio.h>
#include <stdlib.h>
#include <cs50.h>


int main(int argc, char *argv[])
{
    // check if valid argument counter
    if (argc != 2)
    {
        printf("Usage: ./recover file.jpg\n");
        return(1);
    }

    // initialize input as variable
    FILE *inptr = fopen(argv[1], "r");

    // open up the file and check if valid file
    if ( inptr == NULL )
    {
        printf("Could not open file\n");
        return(2);
    }

    //global variables
    unsigned char buffer[512];
    FILE *img = NULL;
    int counter = 0;
    char filename[8];

    //Setup loop
    while (true)
    {
        int read = fread(&buffer, 512, 1, inptr);
        // break if at EOF
        if (read != 1)
        {
            break;
        }
        // check if at start of file
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            // If not at first run, close last file
            if (img != NULL)
            {
                fclose(img);
            }
            // open up new file since we are at start
            sprintf(filename, "%03i.jpg", counter);
            img = fopen(filename, "w");
            counter ++;
        }
        // only write to the file if we are not in the first run!!!!
        if (img != NULL)
        {
            fwrite(&buffer, 512, 1, img);
        }


    }
    fclose(img);
    fclose(inptr);
}

