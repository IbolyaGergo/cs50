#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int height;
    int k;
    int l;
    int m;
    
    do
    {
        height = get_int("Height: ");
    }
    while (height < 1 ^ height > 8);
        
    for (k = 0; k < height; k++)
    {
        for (m = k+1; m < height; m++)
        {
            printf (" ");
        }
        
        for (l = 0; l < k+1; l++)
        {
            printf ("#");
            }
        
        printf ("  ");
        
        for (l = 0; l < k+1; l++)
        {
            printf ("#");
            }
 
        printf ("\n");
        }
    }
    
    
