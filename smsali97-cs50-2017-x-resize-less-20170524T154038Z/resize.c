/**
 * copy.c
 *
 * Computer Science 50
 * Problem Set 4
 *
 * Resizes a BMP piece by piece, just 'cause.
 */
       
#include <stdio.h>
#include <stdlib.h>

#include "bmp.h"

int main(int argc, char* argv[])
{
    // ensure proper usage
    if (argc != 4)
    {
        printf("Usage: ./resize size infile outfile\n");
        return 1;
    }
    
    int size = atoi(argv[1]);
    if ( size < 1 || size > 100) {
        return 5;
        printf(" 1 < size range <= 100 ");
    }

    // remember filenames
    char* infile = argv[2];
    char* outfile = argv[3];

    // open input file 
    FILE* inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        printf("Could not open %s.\n", infile);
        return 2;
    }

    // open output file
    FILE* outptr = fopen(outfile, "w");
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
    
    
    // outfile's BITMAPINFOHEADER and BITMAPOUTFILEHEADER
    BITMAPINFOHEADER boi = bi;
    BITMAPFILEHEADER bof = bf;
     
    boi.biWidth = bi.biWidth * size;
    boi.biHeight = bi.biHeight * size;
    
    // determine padding for scanlines
    int padding =  (4 - (bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;
    int newpadding = (4 - (boi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;
    
    bi.biSizeImage = ( (sizeof(RGBTRIPLE) * bi.biWidth ) + padding ) * abs(bi.biHeight);
    boi.biSizeImage = ( ( sizeof(RGBTRIPLE) * boi.biWidth ) + newpadding ) * abs(boi.biHeight);
    //boi.biSizeImage = ( (sizeof(RGBTRIPLE) * boi.biWidth ) + newpadding ) * abs(boi.biHeight);
    //boi.biSizeImage = ((boi.biWidth * abs(boi.biHeight) * 3) + newpadding )*abs(boi.biHeight);
    
    bof.bfSize =  boi.biSizeImage + bof.bfOffBits;
    
    // write outfile's BITMAPFILEHEADER
    fwrite(&bof, sizeof(BITMAPFILEHEADER), 1, outptr);

    // write outfile's BITMAPINFOHEADER
    fwrite(&boi, sizeof(BITMAPINFOHEADER), 1, outptr);

   // iterate over infile's scanlines n times
   for (int i = 0, biHeight = abs(bi.biHeight); i < biHeight; i++) 
   {
       for (int s = 0; s < size ; s++)
       {
           //Reset cursor
           fseek(inptr, bof.bfOffBits + i * (padding + (bi.biWidth * 3)), SEEK_SET);
       
           // iterate over pixels in scanlines
           for (int j = 0; j < bi.biWidth; j++)
           {
            // temporary storage
            RGBTRIPLE triple;
            
            // read RGB triple from infile
            fread(&triple, sizeof(RGBTRIPLE), 1, inptr);
            
            // iterate the pixels n times!
                for (int x = 0; x < size; x++)
                {
                // write RGB triple to outfile
                fwrite(&triple, sizeof(RGBTRIPLE),1,outptr);
                }

            }
           // skip over orignal padding, if any
           fseek(inptr, padding, SEEK_CUR);
       
           // then add it back!
           for (int k = 0; k < newpadding; k++)
            fputc(0x00, outptr);
       }
   }
    // close infile
    fclose(inptr);
    // close outfile
    fclose(outptr);
    // that's all folks
    return 0;
}
