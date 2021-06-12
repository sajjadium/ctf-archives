#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>

#define FILENAME "/var/notes"

int print_notes(int, int, char *);   // note printing function
int find_user_note(int, int);        // seek in file for a note for user
int search_note(char *, char *);     // search for keyword function
void fatal(char *);                  // fatal error handler

int main() {
	int userid, printing=1, fd; // file descriptor
	char searchstring[100];

	setbuf(stdout, NULL);
	setbuf(stdin, NULL);
	setbuf(stderr, NULL);

	printf("Search for: ");
	gets(searchstring);

	userid = getuid();
	fd = open(FILENAME, O_RDONLY);   // open the file for read-only access
	if(fd == -1)
		fatal("in main() while opening file for reading");

	printf("Searching for: \"");
	printf(searchstring);
	printf("\":\n");
    
	while(printing)
		printing = print_notes(fd, userid, searchstring);
	printf("-------[ end of note data ]-------\n");
	close(fd);
}

// A function to print the notes for a given uid that match
// an optional search string
// returns 0 at end of file, 1 if there are still more notes
int print_notes(int fd, int uid, char *searchstring) {
	int note_length;
	char byte=0, note_buffer[100];
	
	note_length = find_user_note(fd, uid);
	if(note_length == -1)  // if end of file reached
		return 0;           //   return 0

	read(fd, note_buffer, note_length); // read note data
	note_buffer[note_length] = 0;       // terminate the string
	
	if(search_note(note_buffer, searchstring)){ // if searchstring found
		printf("Found: \"");
		printf(searchstring);
		printf("\": ");
		printf(note_buffer);                    //   print the note
    }
	return 1;
}

// A function to find the next note for a given userID
// returns -1 if the end of the file is reached
// otherwise it returns the length of the found note
int find_user_note(int fd, int user_uid) {
	int note_uid=-1;
	unsigned char byte;
	int length;

	while(note_uid != user_uid) {  // loop until a note for user_uid is found
		if(read(fd, &note_uid, 4) != 4) // read the uid data
			return -1; // if 4 bytes aren't read, return end of file code
		if(read(fd, &byte, 1) != 1) // read the newline separator
         return -1;

		byte = length = 0;
		while(byte != '\n') {  // figure out how many bytes to the end of line
			if(read(fd, &byte, 1) != 1) // read a single byte
				return -1;     // if byte isn't read, return end of file code
			length++;  
		}
	}
	lseek(fd, length * -1, SEEK_CUR); // rewind file reading by length bytes

	printf("[DEBUG] found a %d byte note for user id %d\n", length, note_uid);
	return length;
}

// A function to search a note for a given keyword
// returns 1 if a match is found, 0 if there is no match
int search_note(char *note, char *keyword) {
	int i, keyword_length, match=0;

	keyword_length = strlen(keyword);
	if(keyword_length == 0)  // if there is no search string
		return 1;              // always "match"
	
	for(i=0; i < strlen(note); i++) { // iterate over bytes in note
		if(note[i] == keyword[match])  // if byte matches keyword
			match++;   // get ready to check the next byte
		else {        //   otherwise
			if(note[i] == keyword[0]) // if that byte matches first keyword byte
				match = 1;  // start the match count at 1
			else
				match = 0;  // otherwise it is zero
		}
		if(match == keyword_length) // if there is a full match
			return 1;   // return matched
	}
	return 0;  // return not matched
}

// A function to display an error message and then exit
void fatal(char *message) {
   char error_message[100];

   strcpy(error_message, "[!!] Fatal Error ");
   strncat(error_message, message, 83);
   perror(error_message);
   exit(-1);
}
