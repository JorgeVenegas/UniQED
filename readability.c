#include <stdio.h>
#include <cs50.h>
#include <ctype.h>
#include <string.h>
#include <math.h>

int main(void)
{
    float l = 0, w = 1, s = 0;
    string input = get_string("Text: ");
    int len = strlen(input);
    for (int i = 0; i < len; i++)
    {
        char x = input[i];
        char prevx = input[i-1];
        if(isalpha(x))
        {
            l++;
        }
        else if (isspace(x) && !isspace(prevx))
        {
            w++;
        }
        else if(x == '.' || x == '!' || x == '?')
        {
            s++;
        }
    }
    l *= (100 / w);
    s *= (100 / w);
    float output = round(0.0588 * l - 0.296 * s - 15.8);
    if(output < 1) 
    {
        printf("Before Grade 1\n");
    }
    else if(output > 16)
    {
        printf("Grade 16+\n");
    }
    else 
    {
        printf("Grade %i\n", (int) output);
    }
}