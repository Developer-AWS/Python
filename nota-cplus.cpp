#include <stdio.h>
#include<stdlib.h>

int main(){
    float nota1, nota2, media;
          puts ("Digite a primeira nota\n");
          scanf ("%f", &nota1);
    
          puts("Digite a segunda nota\n");
          scanf("%f", &nota2);
              media = (nota1 + nota2) / 2;
              printf("A media do aluno foi %f\n", &media); // altere aquiii
         
    system("pause");
    }