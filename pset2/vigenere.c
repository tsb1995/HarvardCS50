#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <string.h>
#include <stdlib.h>
int shift(char c);

int main(int argc, string argv[])
{
    //Validate the key
    string key = argv[1];
    if (argc != 2)
    {
        printf("Usage: ./vigenere keyword\n");
        return(1);
    }
    else
    {
        // Iterate over length of key, checking for non-digits
        for (int i = 0, n = strlen(key); i < n; i++)
        {
            if (isalpha(key[i]) == false)
            {
                printf("Usage: ./vigenere keyword\n");
                return(1);
            }
        }
    }
    // Setup cipher
    int length = strlen(key);
    int k = 0;
    string plaintext = get_string("plaintext: ");
    printf("ciphertext: ");
    // iterate over input of plaintext, seperating into uppor or lower cases, then implementing cypher
    for (int i = 0, n = strlen(plaintext); i < n;i++)
    {
        char c = plaintext[i];
        char temp = 'a';
        int intkey = shift(argv[1][(k % length)]);
        if (isalpha(c))
        {
            if (isupper(c))
            {
                temp = (((plaintext[i] - 'A') + intkey) % 26) + 'A';
                k++;
            }
            else if (islower(c))
            {
                temp = (((plaintext[i] - 'a') + intkey) % 26) + 'a';
                k++;
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

//Tells us how much to shift based on individual characters
int shift(char c)
{
    if isupper(c)
    {
        int temp = c - 65;
        return(temp);
    }
    else if islower(c)
    {
        int temp = c - 97;
        return(temp);
    }
    else
    {
        return(0);
    }
    
}