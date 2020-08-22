#include <stdio.h>
#include <cs50.h>

bool checkIfValid(long input);
int getLength(long input);
bool checkSum(long input);
void checkforBrandAndPrint(long input);

int main(void) 
{
    long input = 0;
    do 
    {
        input = get_long("Number: \n");
    }
    while (input < 0);
    
    if (checkIfValid(input))
    {
        checkforBrandAndPrint(input);
    }
    else 
    {
        printf("INVALID\n");
    }
}

bool checkIfValid(long input)
{
    int len = getLength(input);
    return (len == 13 || len == 15 || len == 16) && checkSum(input);
}

int getLength(long input)
{
    int l;
    for (l = 0; input != 0; input /= 10, l++);
    return l;
}

bool checkSum(long input)
{
    int sum = 0;
    for (int p = 0; input != 0; input /= 10, p++)
    {
        if (p % 2 == 0)
        {
            sum += input % 10;
        }
        else
        {
            int digit = 2 * (input % 10);
            sum += (digit / 10) + (digit % 10);
        }
    }
    return (sum % 10) == 0;
}

void checkforBrandAndPrint(long input)
{
    string print; 
    if ((input >= 34e13 && input < 35e13) || (input >= 37e13 && input < 38e13))
    {
        print = "AMEX\n";
    }
    else if (input >= 51e14 && input < 56e14)
    {
        print = "MASTERCARD\n";
    }
    else if ((input >= 4e12 && input < 5e12) || (input >= 4e15 && input < 5e15))
    {
        print = "VISA\n";
    }
    else
    {
        print = "INVALID\n";
    }
    printf("%s", print);
}