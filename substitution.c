#include <stdio.h>
#include <cs50.h>
#include <ctype.h>
#include <string.h>

int dif[26];
bool isValid(string input);

int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./substitution key \n");
        return 1;
    }
    string input = argv[1];
    if (isValid(input))
    {
        string txt = get_string("plaintext: ");
        for(int i = 0; i < strlen(txt); i++)
        {
            int chara = txt[i];
            txt[i] = isupper(chara) ? chara + dif[chara - 'A'] : chara + dif[chara - 'a'];
        }
    printf("ciphertext: %s\n", txt);
    }
    else 
    {
        return 1;
    }
}

bool isValid(string input)
{
    int len = strlen(input);
    if(len != 26)
    {
        printf("Key must contain 26 characters. \n");
        return false;
    }
    for (int i = 0, l = 'A'; i < len; i++, l++)
    {
        if(!isalpha(input[i])) {
            printf("Usage: ./substitution key \n"); 
            return false;
        }
        dif[i] = (int) toupper(input[i]) - l;
        for (int j = 0; j < i; j++)
        {
            return dif[i] == dif[j];
        }
    }
    return true;
}