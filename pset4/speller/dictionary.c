// Implements a dictionary's functionality

#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h> // for isupper/islower

#include "dictionary.h"

// global variable to hold word count
int words = 0;
// Represents number of children for each node in a trie
#define N 27

// Represents a node in a trie
typedef struct node
{
    bool is_word;
    struct node *children[N];
}
node;

// Represents a trie
node *root;

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    // Initialize trie
    root = malloc(sizeof(node));
    if (root == NULL)
    {
        return false;
    }
    root->is_word = false;
    for (int i = 0; i < N; i++)
    {
        root->children[i] = NULL;
    }

    // Open dictionary
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        unload();
        return false;
    }

    // Buffer for a word
    char word[LENGTH + 1];

    // Insert words into trie
    while (fscanf(file, "%s", word) != EOF)
    {
        // write word into buffer
        fwrite(word, LENGTH, 1, file);

        // initialize a pointer to traverse the trie and have it point to root
        node *trav = root;

        // iterate through each letter in the string
        for (int i = 0, len = strlen(word); i < len; i++)
        {
            // convert letter to number 1-27
            int childnum = word[i];
            if (childnum == 39)
            {
                childnum = 26;
            }
            else
            {
                childnum = word[i] - 97;
            }

            // check if the c value points to null
            if (trav->children[childnum] == NULL)
            {
                // make a new node and initialize values
                node *fresh;
                fresh = malloc(sizeof(node));
                if (fresh == NULL)
                {
                    return false;
                }
                fresh->is_word = false;
                for (int k = 0; k < N; k++)
                {
                    fresh->children[k] = NULL;
                }

                // have last node point to this
                trav->children[childnum] = fresh;

                // point trav to this new node
                trav = fresh;
            }

            // for if there exists a node already
            else
            {
                // have trav point to the non null node
                trav = trav->children[childnum];
            }
        }

        // mark as end of a letter and increase word count
        trav->is_word = true;
        words ++;
    }

    // Close dictionary
    fclose(file);

    // Indicate success
    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    return words;
}

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    // create pointer trav starting at root to traverse the trie (root is itself a pointer so just set equal)
    node *trav = root;

    // iterate through each letter in the word
    for (int i=0, n = strlen(word); i < n; i++)
    {
        // convert letter to index number
        int childnum;
        if (isupper(word[i]))
        {
            childnum = word[i] - 65;
        }
        else if (islower(word[i]))
        {
            childnum = word[i] - 97;
        }
        else
        {
            childnum = 26;
        }

        // point trav at the corrosponding node
        trav = trav->children[childnum];

        // Deal with the case where we ran out of nodes to follow
        if (!trav)
        {
            return false;
        }
    }

    // when we have done all the letters, see if we are at a word
    if (trav->is_word)
    {
        return true;
    }

    else
    {
        return false;
    }
    return false;
}

// recursive function which iterates through each letter in a node, if not null letter then do it again on corrosponding node, and at
// end of iteration frees the node

void clear(node *ptr)
{
    for (int i = 0; i<27; i++)
    {
        if (ptr->children[i] != NULL)
        {
            clear(ptr->children[i]);
        }
    }
    free(ptr);
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    clear(root);
    return true;
}

