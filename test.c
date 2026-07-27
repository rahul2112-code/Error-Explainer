// test.c - Sample C file with various errors for testing
#include <stdio.h>

int main() {
    int x = 5
    int y = 10;
    
    printf("Sum is: %d\n", add(x, y));
    
    return 0;
}

int add(int a, int b) {
    int sum = a + b;
    // Missing return statement
}