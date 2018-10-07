/**
 * recover.c
 *
 * Computer Science 50
 * Problem Set 4
 *
 * Recovers JPEGs from a forensic image.
 */
 
#include <stdio.h> 
#include <stdbool.h>
#include <stdlib.h>

int main(int argc, char* argv[])
{
    // track counter of jpegs opened
    int count = 0;
    
    
    // start of a series of jpegs
    bool start = false;
    bool found = false;
    
    // open memory card file
    char* infile = argv[1];
    FILE* inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        fprintf(stderr,"Could not open file");
        return 1;
    }
    
    if ( argc != 2) {
        fprintf(stderr,"Usage ./recover card.raw");
    return 1;
        
    }
    
    FILE* img = NULL;
    
    unsigned char a[512];
    fread(a, sizeof(unsigned char) , 512 , inptr);
    
    // repeat until end of card
    do {
        // start of a new jpeg?
        if ( a[0] == 0xff &&  a[1] == 0xd8 && a[2] == 0xff &&  (a[3] & 0xf0) == 0xe0 ) 
            start = true;
        else
            start = false;
        
        // has a jpeg been found before?    

        
        // start of the very first jpeg
        if (!found && start ) {
            char* title = malloc(8 * sizeof(char) );
            sprintf(title,"%03i.jpg",count++);
            img = fopen(title,"w");

            if (img == NULL)
            {
            printf("Could not create %s.\n",title);
            return 2;
            }
            
            fwrite(a, sizeof(unsigned char), 512, img);
            found = true;
        
            free(title);
        }
        
        // continuing on the same jpeg
        else if (found && !start) {
            fwrite(a, sizeof(unsigned char), 512, img);
        }
        
        else if (found && start ) {
            // close previously open jpeg
            fclose(img);
            
            char* title = malloc(8 * sizeof(char));
            sprintf(title,"%03i.jpg",count++);
            img = fopen(title,"w");

            if (img == NULL)
            {
            printf("Could not create %s.\n",title);
            return 3;
            }
            fwrite(a, sizeof(unsigned char), 512, img);
        
            free(title);
        }
        
    
    } while ( ( fread(a, sizeof(unsigned char) , 512 , inptr) ) == 512);
    
    if (count == 0) {
        fprintf(inptr,"lack of image");
        return 1;
    }
    fclose(img);
    fclose(inptr);
}    