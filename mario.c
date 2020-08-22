#include <stdio.h>
#include <cs50.h>

int main(void) 
{
    do 
    {
     int height = get_int("Height: \n");    
    } while(height >= 1 && height <= 8) 
    for (int i = 1; i <= height; i++)
    {
        for(int j = 0; j < (height - i); j++) 
        {
        printf(" ");    
        }
        for(int k = 0; k < i; k++) 
        {
        printf("#");    
        }
        printf("  ");    
        for(int k = 0; k < i; k++) 
        {
        printf("#");    
        }
        printf("\n");    
    }
}