// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <strings.h>
#include <string.h>
#include <cs50.h>

#include "dictionary.h"

// Represents number of buckets in a hash table
#define N 378

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Represents a hash table
node *hashtable[N];

// Hashes word to a number between 0 and 25, inclusive, based on its first letter
unsigned int hash(const char *word)
{
    int len = strlen(word);
    unsigned int index = 0;
    int charcopy;
    for (int i = 0; i < len; i++)
    {
        charcopy = word[i];
        if (!islower(charcopy))
        {
            charcopy = tolower(charcopy);
        }
        index += charcopy;
    }
    index = index % N;
    return index;
}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    // Initialize hash table
    for (int i = 0; i < N; i++)
    {
        hashtable[i] = NULL;
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
    int ind;

    // Insert words into hash table
    while (fscanf(file, "%s", word) != EOF)
    {
        // TODO
        node *new_node = malloc(sizeof(node));
        if (!new_node)
        {
            unload();
            return false;
        }
        // copy word from file to (*new_node).word
        strcpy(new_node->word, word);

        // getting the index of the word in hashtable
        ind = hash(new_node->word);

        // Inserting the word to hashtable
        if (!hashtable[ind])
        {
            new_node->next = NULL;
        }
        else
        {
            new_node->next = hashtable[ind];
        }
        hashtable[ind] = new_node;
    }

    // Close dictionary
    fclose(file);

    // Indicate success
    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    unsigned int number = 0;

    for (int i = 0; i < N; i++)
    {
        node *cursor = hashtable[i];

        while (cursor != NULL)
        {
            number ++;
            cursor = cursor->next;
        }
    }
    return number;
}

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    // TODO
    int index = hash(word);
    node *cursor = hashtable[index];
    int comparison;

    while (cursor != NULL)
    {
        comparison = strcasecmp(cursor->word, word);
        if (comparison == 0)
        {
            return true;
        }
        else
        {
            cursor = cursor->next;
        }
    }
    return false;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    // TODO
    for (int i = 0; i < N; i++)
    {
        node *cursor = hashtable[i];
        while (cursor != NULL)
        {
            node *tmp = cursor;
            cursor = cursor->next;
            free(tmp);
        }
    }
    return true;
}
