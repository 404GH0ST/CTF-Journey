#include<stdio.h>
#include<string.h>
#include <stdlib.h>
#include <unistd.h>
//gcc -g -Wl,-z,relro,-z,now chall.c -o chall
void init(){
	setvbuf(stdin, 0LL, 2, 0LL);
  	setvbuf(stdout, 0LL, 2, 0LL);
  	setvbuf(stderr, 0LL, 2, 0LL);
  	alarm(30);
}

void win(){
	FILE* file;
    int c = 0;

    file = fopen("flag.txt", "r");

    if (NULL == file) {
        fprintf(stderr, "Cannot open flag.txt");
        exit(EXIT_FAILURE);
    } else {
        while (1) {
            c = fgetc(file);
            if (c == EOF)
                break;
            putchar(c);
        }
        fclose(file);
    }	
}

void main(){
	init();
	char nama[80];
	char nama_staff[100]="Felix Alexander";
	printf("---Ticket---\n");
	printf("Nama : ");
	fgets(nama,120,stdin);
	if ( strncmp(nama_staff,"Administrator",13) == 0 ){
		printf("Selamat Datang %s\n",nama);
		win();
	}else{
		printf("Selamat Datang %s\n",nama);
		printf("Nama Staff yang membuat ticket kamu : %s\n",nama_staff);
	}

}