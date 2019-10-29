#include <cs50.h>
#include <stdio.h>

int get_int_range(string prompt); // making a prototype for our get int function
void print_lots(string character,int n); // prototype for printing repeated characters in a line


int main(void)
{
    int height = get_int_range("Height between 1 and 8:");
    
    for (int k=0; k<height; k++)
    {
        // print characters in proper order
        print_lots(" ",height - k - 1);
        print_lots("#",k+1);
        printf("  ");
        print_lots("#",k+1);
        printf("\n");
    }

}

int get_int_range(string prompt) // define function to get an int in a range
{
    int n;
    do
    {
        n = get_int("%s", prompt);
    }
    while (n < 1 || n>8);
    return n;
}

void print_lots(string character,int n) // define a function to print the same character a bunch
{
    for(int i=0; i<n;i++)
    {
            printf("%s", character);
    }
}
