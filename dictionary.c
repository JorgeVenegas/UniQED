// Implements a dictionary's functionality
#include <stdio.h>
#include <stdbool.h>
#include <cs50.h>
#include <string.h>
#include <strings.h>
#include <ctype.h>
#include <stdlib.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Number of buckets in hash table
const unsigned int N = 10000;

// Number of words in dictionary.
int words = 0;

// Hash table
node *table[N];

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    node *trav = table[hash(word)];
    while (trav != NULL)
    {
        if(strcasecmp(word, trav->word) == 0)
        {
            return true;
        }
        else
        {
            trav = trav->next;
        }
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word) {
    long sum = 0, mul = 1;
    for (int i = 0; i < strlen(word); i++) {
        mul = (i % 4 == 0) ? 1 : mul * 256;
        sum += tolower(word[i]) * mul;
    }
    return (int)(labs(sum) % N);
}

// Hashes word to a number
/*
unsigned int hash(const char *word)
{
    int hash = 0;
    for (int i = 0, b = 1; i < 3; i++, b *= 100)
    {
        hash += (tolower(word[i]) - 'a') * b;
    }
    return hash;
}
*/

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        printf("Could not open file\n");
        return false;
    }

    char word[LENGTH];

    while (fscanf(file, "%s", word) != EOF)
    {
        words++;
        node *new_node = malloc(sizeof(node)); // Create new node for word.
        strcpy(new_node->word, word); // Copy the value of the word to the node.
        int index = hash(word); // Hash word to get hash code.
        if (table[index] == NULL) // In case the table index has not any linked list.
        {
            table[index] = new_node; // Table index now points to new node.
            new_node->next = NULL; // Set new node pinting to NULL.
        }
        else // In case it already has a linked list.
        {
            new_node->next = table[index]; // Set new node pointing to the first element in linked list.
            table[index] = new_node; // Set the table index pointer to the new node we have just created.
        }
    }
    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    return words;
}

// Free al memory allocated.
void destroy(node *node)
{
    if (node->next == NULL)
    {
        return;
    }
    destroy(node->next);
    free(node);
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    for (int i = 0; i < N; i++)
    {
        if(table[i] != NULL)
        {
            destroy(table[i]);
        }
    }
    return true;
}
