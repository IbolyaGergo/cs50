#include <stdio.h>
#include <cs50.h>

    
int sum=0;
int counter=1;
int dig, sec, dignum, i;

int main(void)
{
    long card=get_long("Number: ");
    long number=card;
 
    while(counter<19)
    {
        if((number%10)>0)
        {
            dig=number%10;                 /*non-zero digit counted from right to left*/
        
            if(counter%2==0&&dig>0)        /*every 2nd digit multiplied by 2*/
            {
                sec=dig*2;
                sec=sec/10+(sec%10);
                sum=sum+sec;               /*sum of digits is added to the sum*/
            }
            else
            {
                sum=sum+dig;
            }
        }
        
        number/=10;                        /*reducing the number of digits from the right*/
        
        counter++;
        
        if(number>0)
        {
            dignum=counter;
        }
        
    }
   
    if(sum%10==0)                          /*control of the validity of the card number
                                            * if valid, check if it's VISA, MasterCard or AmericanExpress*/
    {
        if(dig==4)
        {
            if(dignum==13||dignum==16)
            {
                printf("VISA\n");
            }
        }
    
        if(dignum==15)
        {
            for(i=0;i<13;i++)
            {
                card/=10;
            }

            if(card==34||card==37)
            {
                printf("AMEX\n");
            }
        }

        if(dignum==16&&dig==5)
        {
            for(i=0;i<15;i++)
            {
                card/=10;
            }
            
            if(card==1||card==2||card==3||card==4||card==5)
            {
                printf("MASTERCARD\n");
            }
        }
    }
            
    else
    {
        printf("INVALID\n");
    }
}
