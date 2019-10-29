#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <string.h>
#include <stdlib.h>

int main(int argc, string argv[])
{
    //Validate the key
    if (argc != 2)
    {
        printf("Usage: ./caesar key\n");
        return(1);
    }
    
    string key = argv[1];
    int intkey = atoi(argv[1]);
    
    if (argc == 2)
    {
        // Iterate over length of key, checking for non-digits
        for (int i = 0, n = strlen(key); i < n; i++)
        {
            if (isdigit(key[i]) == false)
            {
                printf("Usage: ./caesar key\n");
                return(1);
            }
        }
    }
    // Setup cipher
    string plaintext = get_string("plaintext: ");
    printf("ciphertext: ");
    // iterate over input of plaintext, seperating into uppor or lower cases, then implementing cypher
    for (int i = 0, n = strlen(plaintext); i < n; i++)
    {
        char c = plaintext[i];
        char temp = 'a';
        if (isalpha(c))
        {
            if (isupper(c))
            {
                temp = (((plaintext[i] - 'A') + intkey) % 26) + 'A';
            }
            else
            {
                temp = (((plaintext[i] - 'a') + intkey) % 26) + 'a';
            }
            printf("%c", temp);
        }
        else
        {
            printf("%c", c);
        }
    }
    printf("\n");
    return(0);
}