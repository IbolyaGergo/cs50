#include <cs50.h>
#include <stdio.h>
#include <string.h>

bool isnum(string str);
int strtoint(string s);
void cipher(string plaintext, int key);

int main(int argc, string argv[])
{
    // There must be 2 args(./caesar key), the 2nd arg must be a positive integer
    if (argc == 2 && isnum(argv[1]))
    {
        string ptext = get_string("plaintext: ");
        int k = strtoint(argv[1]);
        cipher (ptext, k);
    }
    else
    {
        printf ("Usage: ./caesar key\n");
    }
}

//Function that returns false, if one of the chars is not a number, otherwise returns true
bool isnum(string str)
{
    for (int i = 0; i < strlen(str); i++)
    {
        if (str[i] < 48 || str[i] > 57)
        {
            return false;
        }
    }
    return true;
}

//Making an int from a string
int strtoint(string s)
{
    int len = strlen(s);
    int num = 0;
    
    for (int i = 0, t = 1; i < len; i++)
    {
        num = (s[len - 1 - i] - 48)*t + num;

        t *= 10;
    }
    return num;
}

//Ciphering a plaintext
void cipher(string plaintext, int key)
{
    int ciphertext[strlen(plaintext)];
    
    for(int i = 0; i < strlen(plaintext); i++)
    {
        if (plaintext[i] >= 'a' && plaintext[i] <= 'z')
        {
            ciphertext[i] = (int) 'a' + ((int) plaintext[i] + key - (int) 'a') % 26;
        }
        else if (plaintext[i] >= 'A' && plaintext[i] <= 'Z')
        {
            ciphertext[i] = (int) 'A' + ((int) plaintext[i] + key - (int) 'A') % 26;
        }
        else
        {
            ciphertext[i] = plaintext[i];
        }
    }
    printf("ciphertext: ");
    for (int i = 0; i < strlen(plaintext); i++)
    {
        printf("%c", ciphertext[i]);
    }
    printf("\n");
}
