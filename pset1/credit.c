#include <cs50.h>
#include <stdio.h>
#include <math.h>
int check_length(long int n);
int check_digit(long int num, int length, int n);
bool luhn_alg(long int num, int length);

int main(void)
{
    // setup variables
    long int num = 0;
    int length = 0;
    string type = "";
    bool check = false;

    do
    {
        // get the number and setup variable to check if valid
        num = get_long("number:");
        length = check_length(num);
        int digit1 = check_digit(num, length, 1);
        int digit2 = check_digit(num, length, 2);
        bool luhn = luhn_alg(num, length);
        if (luhn == false)
        {
            printf("INVALID\n");
            break;
        }

        //checking all possible lengths, looking at beginning digits to determine card type if valid
        if (length == 13)
        {
            if (digit1 == 4)
            {
                type = "VISA";
                check = true;
            }
            else
            {
                printf("INVALID\n");
                break;
            }
        }

        else if (length == 15)
        {
            if (digit1 == 3 && (digit2 == 4 || digit2 == 7))
            {
                type = "AMEX";
                check = true;
            }
            else
            {
                printf("INVALID\n");
                break;
            }
        }
        else if (length == 16)
        {
            if (digit1 == 5 && digit2 > 0 && digit2 < 6)
            {
                type = "MASTERCARD";
                check = true;
            }


            else if (digit1 == 4)
            {
                type = "VISA";
                check = true;

            }
            else
            {
                printf("INVALID\n");
                break;
            }
        }
        else
        {
            printf("INVALID\n");
            break;
        }


    }
    while (check == false);
    printf("%s\n", type);

}

//function to check the length of card number given
int check_length(long int num)
{
    int count = 0;
    do
    {
        num = num / 10;
        count = count + 1;
    }
    while (num > 0);
    return count;
}


//function to check the nth digit of the card number given
int check_digit(long int num, int length, int n)
{

    long int digit = num / pow(10, length - n);
    digit = digit % 10;
    digit = (int)digit;
    return digit;

}

// function to check Luhn's algorithm
bool luhn_alg(long int num, int length)
{
    int sum = 0;
    int count = 0;

    do
    {
        // get the digit, multiply by 2, add up digits, add to sum for every other digit starting at 2nd to last
        int temp = check_digit(num, length, length - (count + 1));
        temp = temp * 2;
        int templength = check_length(temp);
        int tempdigit1 = check_digit(temp, templength, 1);
        int tempdigit2 = check_digit(temp, templength, 2);
        sum = sum + tempdigit1;
        sum = sum + tempdigit2;
        count = count + 2;
    }
    while (count < length);
    count = 0; //reset count
    do
    {
        int temp = check_digit(num, length, length - count);
        sum = sum + temp;
        count = count + 2;
    }
    while (count < length);

    if (sum % 10 == 0)
    {
        return (true);
    }
    else
    {
        return (false);
    }
}