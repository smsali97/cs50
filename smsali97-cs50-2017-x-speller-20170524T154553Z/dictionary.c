/**
 * Implements a dictionary's functionality.
 */
#include <stdio.h>
#include <cs50.h>
#include <stdlib.h>
#include <stdbool.h>
#include <strings.h>
#include <string.h>
#include <ctype.h>
#include "dictionary.h"

#define LENGTH 45
// variables
int ctr = 0;
int length = 45;
int SIZE = 100;
bool flag = false;



typedef struct node {
    char word[45 + 1];
    struct node* next;
}
node;

node *hash_table[100];

int hashstring(char *str);



/**
 * Generates a hashtring with a hash function
 * source: http://www.cse.yorku.ca/~oz/hash.html
 */
int hashstring(string str)
{
    /*int hash = 5381;
    int c;

    while ( (c = *str++) )
        hash = ((hash << 5) + hash) + c; 

    return (hash % SIZE);*/
    
    string newstr = str;
    
    int hash = 0;
    for (int i = 0, l = strlen(newstr); i < l; i++)
    {
        char c = tolower(newstr[i]);
    hash += c;
    }
    return hash % SIZE;
}

/**
 * Returns true if word is in dictionary else false.
 */
bool check(const char *word)
{
    int index = hashstring( (char*) word);
    
    
    
    node *cursor = hash_table[index];
    
    while (cursor != NULL)
    {
        int x = strcasecmp( (cursor->word), word);
        
        if ( x==0)
        {
            return true;
        }
        cursor = cursor->next;
    }
    
    return false;
}

/**
 * Loads dictionary into memory. Returns true if successful else false.
 */
bool load(const char *dictionary)
{
    // create a hash table of nodes

    
     // set each node pointer to null
    for (int i = 0; i < SIZE; i++)
    {
        hash_table[i] = NULL;
    } 
    
    // open dictionary
    FILE *fp;
    fp = fopen(dictionary, "r");
    if ( fp == NULL) 
    {
        return false;
    }
    
    char new_word[length];
    while( fscanf(fp, "%s", new_word) != EOF) 
    {
        
        // create a new node for word
        node *new_node = malloc( sizeof(node) );
            
        if ( new_node == NULL ) 
        {
            unload();
            fclose(fp);
            return false;
        }
        
        strcpy(new_node->word,new_word);
        
        
        ctr++;
        // find which 'bucket' should it go to
        int index = hashstring( (char*) new_word);
        // if the 'bucket' is null
        if (hash_table[index]==NULL) 
        {
            hash_table[index] = new_node;
            new_node->next = NULL;
        }
        else 
        {
            new_node->next = hash_table[index];
            hash_table[index] = new_node;
        }
    }
    fclose(fp);
    flag = true;
    return true;
}

/**
 * Returns number of words in dictionary if loaded else 0 if not yet loaded.
 */
unsigned int size(void)
{
  if (flag) 
    return ctr;
  else
    return 0;
}

/**
 * Unloads dictionary from memory. Returns true if successful else false.
 */
bool unload(void)
{
    for(int i = 0; i < SIZE; i++)
    {
        node* cursor = hash_table[i];
        while (cursor != NULL) 
        {
          node* temp = cursor;
          cursor = cursor->next;
          free(temp);
        }
    }
    return true;
}
