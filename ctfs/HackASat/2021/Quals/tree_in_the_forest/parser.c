/*
 * Parser for telecommand protocol
 * 
 * Logs how many times each command has been hit. Has a simple security feature that hides data from the user.
 * 
 */

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <string>
#include <iostream>
#include <sstream>
#include <sys/types.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <netinet/in.h>
#include <sys/time.h>
#include <signal.h>

#define COMMAND_LIST_LENGTH 10
typedef enum command_id_type {
	COMMAND_ADCS_ON = 		0,
	COMMAND_ADCS_OFF =		1,
	COMMAND_CNDH_ON =		2,
	COMMAND_CNDH_OFF =		3,
	COMMAND_SPM =			4,
	COMMAND_EPM =			5,
	COMMAND_RCM =			6,
	COMMAND_DCM =			7,
	COMMAND_TTEST =			8,
	COMMAND_GETKEYS =		9, // only allowed in unlocked state
} command_id_type;

typedef enum lock_states {
	UNLOCKED = 			0,
	LOCKED = 			1,
} lock_states;

typedef struct command_header{
	short version : 16;
	short type : 16;
	command_id_type id : 32;
} command_header;

// Globals used in this program, used to store command log and locked/unlocked state
unsigned int lock_state;
char command_log[COMMAND_LIST_LENGTH];

void catch_alarm (int sig) {
  fprintf(stderr, "timeout\n");
  exit(0);
}

unsigned int timeout (unsigned int seconds)
{
  struct itimerval old_timer;
  struct itimerval new_timer;

  new_timer.it_interval.tv_usec = 0;
  new_timer.it_interval.tv_sec = 0;
  new_timer.it_value.tv_usec = 0;
  new_timer.it_value.tv_sec = (long int) seconds;
  if (setitimer (ITIMER_REAL, &new_timer, &old_timer) < 0)
    return 0;
  else
    return old_timer.it_value.tv_sec;
}

const char* handle_message(command_header* header){
	command_id_type id = header->id;
	// Based on the current state, do something for each command
	switch(lock_state){
		case UNLOCKED:
			if (id == COMMAND_GETKEYS)
				return std::getenv("FLAG");
			else
				return "Command Success: UNLOCKED";
		default:
			if (id == COMMAND_GETKEYS)
				return "Command Failed: LOCKED";
			else
				return "Command Success: LOCKED";
	}

	// Forward command to antenna
}

void server_loop(){
	int sockfd;
	char buffer[sizeof(command_header)];
	struct sockaddr_in servaddr, cliaddr;

	if ((sockfd = socket(AF_INET, SOCK_DGRAM, 0)) < 0 ) {
		perror("socket creation failed");
		exit(EXIT_FAILURE);
	}

	memset(&servaddr, 0, sizeof(servaddr));
	memset(&cliaddr, 0, sizeof(cliaddr));
	servaddr.sin_family    = AF_INET; // IPv4
	servaddr.sin_addr.s_addr = inet_addr("0.0.0.0");
	// servaddr.sin_port = htons(std::atoi(std::getenv("CHAL_PORT")));
	servaddr.sin_port = htons(54321);

	fprintf(stderr, "Trying to bind to socket.\n");
	if (bind(sockfd, (const struct sockaddr *)&servaddr, sizeof(servaddr)) < 0)
	{
		perror("bind failed");
		exit(EXIT_FAILURE);
	}
	fprintf(stderr, "Bound to socket.\n");

	do{
		std::stringstream response;
		socklen_t len;
		int n;
		len = sizeof(cliaddr);

		n = recvfrom(sockfd, (char *)buffer, sizeof(command_header), MSG_WAITALL, (struct sockaddr *)&cliaddr, &len);

		if (n != sizeof(command_header)){ // this should never happen, due to UDP
			response << "Invalid length of command header, expected "<<sizeof(command_header)<<" but got "<<n<<std::endl;
		} else { 
			command_header* header = (command_header*)buffer;
			response<<"Command header acknowledge: version:"<<header->version<<" type:"<<header->type<<" id:"<<header->id<<std::endl;

			if (header->id >= COMMAND_LIST_LENGTH){
				response<<"Invalid id:"<<header->id<<std::endl;
			} else {

				// Log the message in the command log
				command_log[header->id]++;

				// Handle the message, return the response
				response<<handle_message(header)<<std::endl;

			}
		}

		sendto(sockfd, response.str().c_str(), response.str().length(), MSG_CONFIRM, (const struct sockaddr *) &cliaddr, len);
	} while(1);
}

int main() {

	lock_state = LOCKED;

//	const char *service_host = std::getenv("SERVICE_HOST");
//	const char *service_port = std::getenv("SERVICE_PORT");
	const char *timeout_value = std::getenv("TIMEOUT");

//    fprintf(stdout, "Starting up on udp:%s:%s\n", service_host, service_port);
//	fflush(stdout);

//	fprintf(stderr, "Address of lock_state:       %p\n", &lock_state);
//	fprintf(stderr, "Address of command_log: %p\n", &command_log);
	// fprintf(stderr, "Port: %d\n", std::atoi(std::getenv("CHAL_PORT")));


	// Zero out the command log
	for (int i=0; i < COMMAND_LIST_LENGTH; i++)
		command_log[i] = 0;

	// set a timer

	if (timeout_value)
		timeout(atoi(timeout_value));
	else
		timeout(60);

	// catch the alarm from the timer and exit the challenge
  	signal (SIGALRM, catch_alarm);

	server_loop();

	return 1;
}
