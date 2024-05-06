#include <stdio.h>
#include <cs50.h>
#include <math.h>

int rem, k, l, m, n;
float dollars;

int main(void)
{
    do
    {
        dollars = get_float("Change owed: ");
    }
    while (dollars < 0);
    
    int cents = round(dollars * 100);
    
    k = cents/25;
    rem = (cents - k * 25);
    l = rem/10;
    rem = rem - l * 10;
    m = rem/5;
    rem = rem - m * 5;
    n = k + l + m + rem;
    printf ("%i\n", n);
    
}
