#include <cs50.h>
#include <stdio.h>
#include <string.h>

bool ischar(string str);
void cipher(string plaintext, string keyword);
int shift(char c);

int main(int argc, string argv[])
{
    if (argc == 2 && ischar(argv[1]))
    {
        string ptext = get_string("plaintext: ");
        cipher(ptext, argv[1]);
    }
    else
    {
        printf("Usage: ./vigenere keyword\n");
    }
}

//Function that returns false, if one of the chars is not a number, otherwise returns true
bool ischar(string str)
{
    for (int i = 0; i < strlen(str); i++)
    {
        if ((str[i] >= 'a' && str[i] <= 'z') || (str[i] >= 'A' && str[i] <= 'Z'))
        {
            return true;
        }
    }
    return false;
}

//Ciphering a plaintext
void cipher(string plaintext, string keyword)
{
    char ciphertext[strlen(plaintext)];
    int keylen = strlen(keyword);
    int charnum = 0;
    for(int i = 0, key; i < strlen(plaintext); i++)
    {
        key = shift(keyword[charnum]);
        
        if (plaintext[i] >= 'a' && plaintext[i] <= 'z')
        {
            ciphertext[i] = 'a' + (plaintext[i] + key - 'a') % 26;
        }
        else if (plaintext[i] >= 'A' && plaintext[i] <= 'Z')
        {
            ciphertext[i] = 'A' + ( plaintext[i] + key - 'A') % 26;
        }
        else
        {
            ciphertext[i] = plaintext[i];
        }
        if ((i + 1) % keylen == 0)
        {
            charnum = 0;
        }
        else
        {
            charnum++;
        }
    }
    printf("ciphertext: ");
    for (int i = 0; i < strlen(plaintext); i++)
    {
        printf("%c", ciphertext[i]);
    }
    printf("\n");
}

//Function takes a char as input, the output is the char's corresponding shift value
int shift(char c)
{
    if (c <= 'Z')
    {
        return c % 'A';
    }
    else
    {
        return c % 'a';
    }
}
