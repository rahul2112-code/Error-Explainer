#include <stdio.h>

int main() {
    char str[100];
    int alphabets = 0, digits = 0, specialChars = 0, i = 0;

    printf("Enter a string: ")
    gets(str); 
    while (str[i] != '\0') {
        if ((str[i] >= 'a' && str[i] <= 'z') || (str[i] >= 'A' && str[i] <= 'Z')) {
            alphabets++;
        } else if (str[i] >= '0' && str[i] <= '9') {
            digits++;
        } else {
            specialChars++;
        }
        i++;
    }

    printf("Alphabets: %d\n", alphabet);
    printf("Digits: %d\n", digits);
    printf("Special Characters: %d\n", specialChars);

    return 0;
}
