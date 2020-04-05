//Modificado por Luis Antonio Costa (2016/2) para o Laboratorio 3 de Redes de Computadores

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#define _WIN32 1 // 1 ou zero dependendo do SO utilizado

#ifdef _WIN32
	#include <winsock2.h>
	#include <WS2tcpip.h>
#else
	#include <sys/types.h>
	#include <sys/socket.h>
	#include <netinet/in.h>
	#include <arpa/inet.h>
	#define	SOCKET	int
	#define INVALID_SOCKET  ((SOCKET)~0)
#endif


#define MAX_PACKET 1250

enum erros {WSTARTUP, ABRESOCK, BIND, ACCEPT, LISTEN,RECEIVE};

void TrataErro(SOCKET, int);

int main(int argc, char* argv[])
{
    int porta=0;
    SOCKET s=0, s_cli;
    struct sockaddr_in  addr_serv, addr_cli;
    socklen_t addr_cli_len=sizeof(addr_cli);

#ifdef _WIN32
    WSADATA wsaData;

	if (WSAStartup(MAKEWORD(2,2), &wsaData) != 0) {
		TrataErro(s, WSTARTUP);
		exit(1);
		}
#endif

    if(argc < 2) {
		  printf("Utilizar:\n");
		  printf("testesrv -p <porta>\n");
		  exit(1);
	 }

	 for(int i=1; i < argc; i++) {
		  if(argv[i][0]=='-'){
				switch(argv[i][1]){
					 case 'p':
						  i++;
						  porta = atoi(argv[i]);
						  if(porta < 1024) {
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

  char recvbuf[MAX_PACKET];

  // Cria o socket na familia AF_INET (Internet) e do tipo TCP (SOCK_STREAM)
  if ((s = socket(AF_INET, SOCK_STREAM, 0))==INVALID_SOCKET)
	  TrataErro(s, ABRESOCK);

  // Define domínio, IP e porta a receber dados
  addr_serv.sin_family = AF_INET;
  addr_serv.sin_addr.s_addr = htonl(INADDR_ANY); // recebe de qualquer IP
  addr_serv.sin_port = htons(porta);

  // Associa socket com estrutura addr_serv
  if ((bind(s, (struct sockaddr *)&addr_serv, sizeof(addr_serv))) != 0)
	  TrataErro(s, BIND);

  // Coloca socket em estado de escuta para as conexoes na porta especificada
  if((listen(s, 8)) != 0) // permite ateh 8 conexoes simultaneas
	  TrataErro(s, LISTEN);

  // permite conexoes entrantes utilizarem o socket
  if((s_cli=accept(s, (struct sockaddr *)&addr_cli, (socklen_t *)&addr_cli_len)) < 0)
	  TrataErro(s, ACCEPT);

  // Laço principal: fica esperando chegar mensagem
    while(1)
    {
        if ((recv(s_cli, recvbuf, MAX_PACKET,0)) < 0)
        {
            close(s_cli);
            TrataErro(s, RECEIVE);
        }
    }

  // fecha socket e termina programa
    printf("Fim da conexao\n");
    close(s);
    close(s_cli);
    exit(1);
}

void TrataErro(SOCKET s, int tipoerro)
{
	char tipo[20];

	switch(tipoerro) {
		case WSTARTUP:
			strcpy(tipo, "Windows Startup");
			break;
		case ABRESOCK:
			strcpy(tipo, "Open Socket");
			break;
		case BIND:
			strcpy(tipo, "Bind");
			break;
		case ACCEPT:
			strcpy(tipo, "Accept");
			break;
		case LISTEN:
			strcpy(tipo, "Listen");
			break;
		case RECEIVE:
			strcpy(tipo, "Receive");
			break;
		default:
			strcpy(tipo, "Indefinido. Verificar");
			break;
	}
    printf("erro no %s", tipo);
    close(s);
    exit(1);
}
