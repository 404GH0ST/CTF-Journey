#include<stdio.h>
#include<string.h>
#include <stdlib.h>
#include <unistd.h>
//gcc -g -Wl,-z,relro,-z,now -no-pie -fno-stack-protector chall.c -o chall
void init(){
	setvbuf(stdin, 0LL, 2, 0LL);
  	setvbuf(stdout, 0LL, 2, 0LL);
  	setvbuf(stderr, 0LL, 2, 0LL);
  	alarm(10);
}

void printf_something_wrong(long int pass1){
	if (pass1 == 0x19b6da8f2bdcb1ee){
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
	}else{
		printf("Coba lagi\n");
	}
}

void flag(){
	printf("FLAG{this is flag}\n");
}

void main(){
	init();
	char buff[40];
	int choose;
	long long int temp_money;
	unsigned long long int money=100000;
	while(1){
		printf("Selamat Datang di TokoPedie\n");
		printf("Uang : %llu$\n",money);
		printf("Menu Barang:\n");
		printf("1. Flag\n");
		printf("2. Laptop ROG\n");
		printf("3. Handphone\n");
		printf("4. Top-Up Money\n");
		printf("5. Keluar\n");
		printf("> ");
		scanf("%i",&choose);
		switch(choose) {
		  case 1:
		  	if ( 48038396025285290 < money){
				printf("Maaf Flag lagi kosong, apakah kamu ingin pre-order ? ");
				money -= 48038396025285290 ;
				read(0,buff,120);
			}else{
				printf("Uang kamu tidak cukup, karena harga flag 48038396025285290$\n");
			}
		    break;
		  case 2:
		    if ( 100 <= money){
				printf("Selamat kamu berhail membeli Laptop ROG");
				money -= 100 ;
			}else{
				printf("Uang kamu tidak cukup, karena harga laptop ROG 100$\n");
			}
		    break;
		  case 3:
		    if ( 200 <= money){
				printf("Selamat kamu berhail membeli Laptop ROG");
				money -= 200 ;
			}else{
				printf("Uang kamu tidak cukup, karena harga laptop ROG 200$\n");
			}
		    break;
		  case 4:
		  	printf("Masukin Jumlahnya: ");
		  	scanf("%lli",&temp_money);
		    if ( temp_money <= 1000){
		    	money += temp_money ;
				printf("Selamat kamu berhail Top-Up\n");	
			}else{
				printf("Kamu melebihi tidak bisa Top-Up lebih dari 1000$\n");
			}
		    break;
		  case 5:
		   	printf("Selamat tinggal\n");
		   	return ;
		  default:
		  	printf(":(\n");
		    // code block
		}
	}

}


