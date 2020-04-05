// testecli.cpp : Defines the entry point for the console application.
//

//Modificado por Luis Antonio Costa (2016/2) para o Laboratorio 3 de Redes de Computadores

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <time.h>
#include <unistd.h>

#ifdef _WIN32
	#include <winsock2.h>
#else
	#include <sys/types.h>
	#include <sys/socket.h>
	#include <netinet/in.h>
	#include <arpa/inet.h>
	#define	SOCKET	int
	#define INVALID_SOCKET  ((SOCKET)~0)
#endif


#define PORTA_CLI 2345 // porta TCP do cliente

int main(int argc, char* argv[])
{
  SOCKET s;
  struct sockaddr_in  s_cli, s_serv;
  char ip_srv[16];
  int porta_srv = 0;

#ifdef _WIN32
	 WSADATA wsaData;

	if (WSAStartup(MAKEWORD(2,2), &wsaData) != 0) {
		printf("Erro no startup do socket\n");
		exit(1);
	}
#endif

    if(argc < 5) {
		  printf("Utilizar:\n");
		  printf("testecli -h <ip> -p <porta>\n");
		  exit(1);
	 }

	 for(int i=1; i < argc; i++) {
		  if(argv[i][0]=='-'){
				switch(argv[i][1]){
					 case 'h':
						  i++;
						  strcpy(ip_srv, argv[i]);
						  break;
					 case 'p':
						  i++;
						  porta_srv = atoi(argv[i]);
						  if(porta_srv < 1024) {
								printf("Porta invalida\n");
								exit(1);
						  }
						  break;
					 default:
						  printf("Parametro %d: %s invalido\n",i,argv[i]);
						  exit(1);
				}
		  }else{
				printf("Parametro %d: %s invalido\n",i,argv[i]);
				exit(1);
		  }
	 }

  // abre socket TCP
  if ((s = socket(AF_INET, SOCK_STREAM, 0))==INVALID_SOCKET)
  {
    printf("Erro iniciando socket\n");
    return(0);
  }

  // seta informacoes IP/Porta locais
  s_cli.sin_family = AF_INET;
  s_cli.sin_addr.s_addr = htonl(INADDR_ANY);
  s_cli.sin_port = htons(PORTA_CLI);

  // associa configuracoes locais com socket
  if ((bind(s, (struct sockaddr *)&s_cli, sizeof(s_cli))) != 0)
  {
    printf("erro no bind\n");
    close(s);
    return(0);
  }

  // seta informacoes IP/Porta do servidor remoto
  s_serv.sin_family = AF_INET;
  s_serv.sin_addr.s_addr = inet_addr(ip_srv);
  s_serv.sin_port = htons(porta_srv);

  // connecta socket aberto no cliente com o servidor
    if(connect(s, (struct sockaddr*)&s_serv, sizeof(s_serv)) != 0)
    {
    //printf("erro na conexao - %d\n", WSAGetLastError());
        printf("erro na conexao");
        close(s);
        exit(1);
    }

#if 0
  // envia mensagem de conexao - aprimorar para dar IP e porta
  if ((send(s, "Conectado\n", 11,0)) == SOCKET_ERROR);
  {
    printf("erro na transmissão - %d\n", WSAGetLastError());
    closesocket(s);
    return 0;
  }
#endif

    char str[1250] = "mensagem";
    int j=0;
    time_t inicio, fim;
    double tempo=0, total_tempo=0, veloc=0;

    while(1)
    {
        time(&inicio);

        if ((send(s, (const char *)&str, sizeof(str),0)) < 0)
        {
            printf("erro na transmissão\n");
            close(s);
            return 0;
        }

        time(&fim);

        j++;
        // incrementa o total do tempo com o da última mensagem enviada
        tempo = difftime(fim, inicio);
        total_tempo += tempo;

        // ao chegar em 1 segundo exibe
        if(total_tempo>=1)
        {
            veloc = (j*sizeof(str)*8/total_tempo)/1000000;
            printf("%f Mbps\n", veloc);
            total_tempo=0;
            j=0;
        }
    }

        // fecha socket e termina programa
        printf("Fim da conexao\n");
        close(s);
        return 0;
}
