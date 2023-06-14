//gcc -g -Wl,-z,relro,-z,now -fno-stack-protector -no-pie chall.c -o chall
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>

char *name_list[20];

int readint(){
    char buf[0x10];
    return atoi(fgets(buf,0x10,stdin));
}

void note(){
    char buff[32];
    printf("note : ");
    read(0, buff, 88);
}

void init(){
    setvbuf(stdin, 0, 2, 0);
    setvbuf(stdout, 0, 2, 0);
    setvbuf(stderr, 0, 2, 0);
    alarm(120);
}

int menu(){
    printf("Blacklist Name\n");
    printf("Menu:\n");
    printf("1. Add Name.\n");
    printf("2. Delete Name.\n");
    printf("3. Write note.\n");
    printf("> ");
    return readint();
}

int main(){
    init();
    int number=0;
    int idx_chs=0;
    int last=0;
    int idx=0;
    char temp[16];
    memset(&name_list, 0, 8*20);
    memset(&temp, 0, 16);
    while(1){
        number = menu();
        if (number == 1){
            if (idx<20){
                printf("Name : ");
                name_list[idx] = (char*)malloc(sizeof(char) * 15);
                temp[read(0, temp, 16)-1]=0;
                strncpy(name_list[idx],temp,strlen(temp));
                printf("Idx %i is added\n",idx);
                idx++;
            }else{
                printf("Full\n");
            }
        }else if(number == 2){
            printf("Index : ");
            idx_chs = readint();
            if (0 <= idx_chs ){
                free(name_list[idx_chs]);
                idx--;
                printf("Free idx %i",idx_chs);
            }else{
                printf("invalid index\n");
            }
        }else if(number == 3){
            note();
            break;
        }else{
            printf("invalid number\n");
            exit(1);
        }
    }
    return 0;
}
