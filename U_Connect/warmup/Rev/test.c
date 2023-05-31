#include <limits.h>
#include <stdio.h>
#include <stdlib.h>

// A structure to represent a stack
struct Stack {
    int top;
    unsigned capacity;
    int* array;
};

// function to create a stack of given capacity. It initializes size of
// stack as 0
struct Stack* createStack(unsigned capacity)
{
    struct Stack* stack = (struct Stack*)malloc(sizeof(struct Stack));
    stack->capacity = capacity;
    stack->top = -1;
    stack->array = (int*)malloc(stack->capacity * sizeof(int));
    return stack;
}

// Stack is full when top is equal to the last index
int isFull(struct Stack* stack)
{
    return stack->top == stack->capacity - 1;
}

// Stack is empty when top is equal to -1
int isEmpty(struct Stack* stack)
{
    return stack->top == -1;
}

// Function to add an item to stack.  It increases top by 1
void push(struct Stack* stack, int item)
{
    if (isFull(stack))
        return;
    stack->array[++stack->top] = item;
    printf("%d pushed to stack\n", item);
}

// Function to remove an item from stack.  It decreases top by 1
int pop(struct Stack* stack)
{
    if (isEmpty(stack))
        return INT_MIN;
    return stack->array[stack->top--];
}

// Function to return the top from stack without removing it
int peek(struct Stack* stack)
{
    if (isEmpty(stack))
        return INT_MIN;
    return stack->array[stack->top];
}

// Driver program to test above functions
int main() {
   
    struct Stack* stack = createStack(100);

    char *a, *b, *c, *d;
    char *value1 = "\x4d\x50\x09\x09";
    char *value2 = "\x93\x0a\xdc\x51";
    char *value3 = "\xf4\x43\x29\x77";
    char *value4 = "\x25\x85\x3b\xed";
    char *value5 = "\x6a\x4b\x21\x3c";
    char *value6 = "\x77\xb1\xbf\x4f";
    char *value7 = "\xeb\x9d\x96\xcb";

    push(stack, value1);
    push(stack, value2);
    a = pop(stack);
    push(stack, value3);
    push(stack, value4);
    b = pop(stack);
    push(stack, value5);
    push(stack, value6);
    c = pop(stack);
    push(stack, value7);
    d= pop(stack);

    printf("The flag is {");
    printf("%x%x%x%x", a,b,c,d);
    printf("}\r\n");

    return 0;
}
