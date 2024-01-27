/*
 * Secure Note Manager
 * Author: peternguyen93
 */
#include "ipc.h"
#include "dbg.h"
#include "protocol.h"
#include "utlist.h"
#include <openssl/sha.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <sys/capability.h>
#include <sys/types.h>

struct IPC ipc;
#define MAX_CONTENT_LEN 0x1000
#define MAX_NOTE 0x100

Note_t notes;
uint32_t notes_size;

int Note_cmp(Note_t note1, Note_t note2)
{
	int res = strncmp(note1->note_title, note2->note_title, sizeof(note1->note_title) - 1) == 0 && \
			strncmp(note2->note_author, note1->note_author, sizeof(note1->note_author) - 1) == 0;
	return !res;
}

Note_t Note_init(
	char *title,
	char *author,
	uint32_t content_len,
	uint32_t encrypt)
{
	Note_t new_note = (Note_t)malloc(sizeof(struct Note));
	bzero(new_note, sizeof(struct Note));
	strncpy(new_note->note_title, title, sizeof(new_note->note_title) - 1);
	strncpy(new_note->note_author, author, sizeof(new_note->note_author) - 1);

	new_note->note_content_len = content_len;
	new_note->note_is_encrypt = encrypt;
	return new_note;
}

void Note_destroy(Note_t note)
{
	assert_fail_f(note, "note could not be null\n");
	if(note->note_content){
		free(note->note_content);
		note->note_content = NULL;
	}
	bzero((void *)note, sizeof(struct Note));
	free(note);
}

void read_line(char *buf, size_t max_size)
{
	uint32_t i = 0;

	while(i < max_size){
		char c = fgetc(stdin);
		if(c == '\n'){
			buf[i] = '\0';
			break;
		}
		buf[i++] = c;
	}
}

int read_int()
{
	char buf[32] = {0};
	read_line(buf, sizeof(buf));
	return atoi(buf);
}

void add_new_note()
{
	char title[32];
	char author[32];
	char buf[64];
	char passwd_hash[SHA256_DIGEST_LENGTH];
	int is_encrypt;
	uint32_t content_len;

	if(notes_size > MAX_NOTE){
		printf("Unable to add new note\n");
		return;
	}

	printf("Title: ");
	read_line(title, sizeof(title) - 1);
	printf("Author: ");
	read_line(author, sizeof(author) - 1);

	do{
		printf("Wanna encrypt this notes? (y/n) ");
		read_line(buf, sizeof(buf));
	}while(buf[0] != 'y' && buf[0] != 'n');

	is_encrypt = buf[0] == 'y' ? 1 : 0;

	Note_t new_note = Note_init(title, author, 0, is_encrypt);
	if(is_encrypt){
		printf("What is your passwd? ");
		bzero(buf, sizeof(buf));

		read_line(buf, sizeof(buf) - 1);
		SHA256((const unsigned char *)buf, strlen(buf), (unsigned char *)passwd_hash);
	}

	printf("How many bytes for content? ");
	content_len = read_int();
	if(content_len > MAX_CONTENT_LEN){
		content_len = MAX_CONTENT_LEN;
	}

	printf("Content: \n");
	new_note->note_content = malloc(content_len);
	new_note->note_content_len = content_len;
	fgets(new_note->note_content, content_len, stdin);

	if(is_encrypt){
		// sync this note to backend
		size_t send_size = sizeof(struct msg_hdr) + sizeof(struct NoteSerialize) + sizeof(passwd_hash) + content_len;
		msg_hdr_t send_msg = malloc(send_size);
		send_msg->action = COMMIT;
		send_msg->msg_size = send_size - sizeof(struct msg_hdr);
		NoteSerialize_t serialize_p = (NoteSerialize_t)send_msg->msg_content;
		memcpy(&(serialize_p->common), &(new_note->common), sizeof(struct NoteCommon));
		serialize_p->note_content_len = sizeof(passwd_hash) + content_len;
		memcpy(serialize_p->content, passwd_hash, sizeof(passwd_hash));
		memcpy(&(serialize_p->content[sizeof(passwd_hash)]), new_note->note_content, new_note->note_content_len);

		send_data(&ipc, RECEIVER, send_msg, send_size);
		free(send_msg);

		uint64_t status = 0;
		int rc = recv_data_timeout(&ipc, SENDER, NULL, (uint64_t *)&status, 60);
		
		if(IS_ERR(rc) || status != OK){
			printf("Unable to sync this note to server :(, destroying this note\n");
			Note_destroy(new_note);
			return;
		}

		free(new_note->note_content);
		new_note->note_content = NULL;
		new_note->note_synced = 1;
	}

	DL_APPEND(notes, new_note);
	notes_size++;
	puts("Added");
}

void delete_note(void)
{
	struct Note s_note;
	Note_t tmp;
	char buf[64];
	char passwd_hash[SHA256_DIGEST_LENGTH];

	bzero(&s_note, sizeof(struct Note));
	printf("Title: ");
	read_line(s_note.note_title, sizeof(s_note.note_title) - 1);
	printf("Author: ");
	read_line(s_note.note_author, sizeof(s_note.note_author) - 1);

	DL_SEARCH(notes, tmp, &s_note, Note_cmp);
	if(!tmp){
		printf("Unable to find your note\n");
		return;
	}


	size_t send_size = sizeof(struct msg_hdr) + sizeof(struct NoteSerialize);
	msg_hdr_t send_msg;

	// sync with server
	if(tmp->note_is_encrypt || tmp->note_synced){
		if(tmp->note_is_encrypt){
			send_size += SHA256_DIGEST_LENGTH;
			printf("Your password? ");
			bzero(buf, sizeof(buf));
			read_line(buf, sizeof(buf) - 1);

			// sha256
			SHA256((const unsigned char *)buf, strlen(buf), (unsigned char *)passwd_hash);
		}

		send_msg = malloc(send_size);
		send_msg->action = DELETE;
		send_msg->msg_size = send_size - sizeof(struct msg_hdr);
		NoteSerialize_t serialize_p = (NoteSerialize_t)send_msg->msg_content;
		memcpy(&(serialize_p->common), &(tmp->common), sizeof(struct NoteCommon));

		serialize_p->note_content_len = 0;
		if(tmp->note_is_encrypt){
			serialize_p->note_content_len = sizeof(passwd_hash);
			memcpy(serialize_p->content, passwd_hash, sizeof(passwd_hash));
		}

		send_data(&ipc, RECEIVER, send_msg, send_size);
		free(send_msg);

		uint64_t status = 0;
		int rc = recv_data_timeout(&ipc, SENDER, NULL, &status, 60);

		if(IS_ERR(rc) || (Status)status != OK){
			printf("Unable to delete note\n");
			return;
		}
	}

	DL_DELETE(notes, tmp);
	notes_size--;
	printf("Deleted\n");
}

void list_note()
{
	Note_t tnote;
	DL_FOREACH(notes, tnote){
		printf("Title: %s\n", tnote->note_title);
		printf("Author: %s\n", tnote->note_author);
		if(tnote->note_is_encrypt){
			printf("Content: (Encrypted)\n");
		} else {
			printf("Content: %s\n", tnote->note_content);
		}
	}
}

void edit_note()
{
	struct Note s_note;
	Note_t tmp;
	char buf[64];
	char passwd_hash[SHA256_DIGEST_LENGTH];
	msg_hdr_t send_msg;
	size_t send_size = 0;
	NoteSerialize_t serialize_p;
	uint64_t status;
	int rc;

	bzero(&s_note, sizeof(struct Note));
	printf("Title: ");
	read_line(s_note.note_title, sizeof(s_note.note_title) - 1);
	printf("Author: ");
	read_line(s_note.note_author, sizeof(s_note.note_author) - 1);

	DL_SEARCH(notes, tmp, &s_note, Note_cmp);
	if(!tmp){
		printf("Unable to find your note\n");
		return;
	}
	
	if(tmp->note_is_encrypt){
		printf("Password ?");
		read_line(buf, sizeof(buf) - 1);
		// sha256
		SHA256((const unsigned char *)buf, strlen(buf), (unsigned char *)passwd_hash);

		// sync with server
		send_size = sizeof(struct msg_hdr) + sizeof(struct NoteSerialize) + sizeof(passwd_hash);
		send_msg = malloc(send_size);
		send_msg->action = AUTH;
		send_msg->msg_size = send_size - sizeof(struct msg_hdr);
		serialize_p = (NoteSerialize_t)send_msg->msg_content;
		memcpy(&(serialize_p->common), &(tmp->common), sizeof(struct NoteCommon));
		serialize_p->note_content_len = sizeof(passwd_hash);
		memcpy(serialize_p->content, passwd_hash, sizeof(passwd_hash));

		send_data(&ipc, RECEIVER, send_msg, send_size);
		free(send_msg);

		rc = recv_data_timeout(&ipc, SENDER, NULL, &status, 60);
		if(IS_ERR(rc) || status != OK){
			printf("Authenticate was failed\n");
			return;
		}
		printf("Access granted\n");
	}

	printf("New content len?");
	uint32_t content_len = read_int();
	content_len = content_len < MAX_CONTENT_LEN ? content_len: MAX_CONTENT_LEN;

	printf("New content:\n");
	if(tmp->note_is_encrypt){
		tmp->note_content = malloc(content_len);
		tmp->note_content_len = content_len;
		fgets(tmp->note_content, content_len, stdin);
		// sync with server
		send_size = sizeof(struct msg_hdr) + sizeof(struct NoteSerialize) + sizeof(passwd_hash) + content_len;
		send_msg = malloc(send_size);
		send_msg->action = COMMIT;
		send_msg->msg_size = send_size - sizeof(struct msg_hdr);
		serialize_p = (NoteSerialize_t)send_msg->msg_content;
		memcpy(&(serialize_p->common), &(tmp->common), sizeof(struct NoteCommon));

		serialize_p->note_content_len += sizeof(passwd_hash);
		memcpy(serialize_p->content, passwd_hash, sizeof(passwd_hash));
		memcpy(serialize_p->content + sizeof(passwd_hash), tmp->note_content, tmp->note_content_len);

		free(tmp->note_content);
		tmp->note_content = NULL;

		send_data(&ipc, RECEIVER, send_msg, send_size);
		free(send_msg);

		rc = recv_data_timeout(&ipc, SENDER, NULL, (uint64_t *)&status, 60);
		if(IS_ERR(rc) || status != OK){
			printf("Unable to update your content\n");
			return;
		}
		tmp->note_synced = 1;
	} else {
		if(tmp->note_content){
			free(tmp->note_content);
		}
		tmp->note_content = malloc(content_len);
		tmp->note_content_len = content_len;
		fgets(tmp->note_content, content_len, stdin);
		tmp->note_synced = 0;
	}
}

void read_note()
{
	struct Note s_note;
	Note_t tmp;
	char buf[64];
	char passwd_hash[SHA256_DIGEST_LENGTH];
	msg_hdr_t send_msg;
	msg_hdr_t recv_msg;
	size_t recv_size = 0;
	size_t send_size = 0;
	NoteSerialize_t serialize_p;
	Status status;
	int rc;

	bzero(&s_note, sizeof(struct Note));
	printf("Title: ");
	read_line(s_note.note_title, sizeof(s_note.note_title) - 1);
	printf("Author: ");
	read_line(s_note.note_author, sizeof(s_note.note_author) - 1);

	DL_SEARCH(notes, tmp, &s_note, Note_cmp);
	if(!tmp){
		printf("Unable to find your note\n");
		return;
	}

	if(tmp->note_is_encrypt){
		printf("Password? ");
		read_line(buf, sizeof(buf) - 1);
		// sha1 here
		SHA256((const unsigned char *)buf, strlen(buf), (unsigned char *)passwd_hash);

		// read from backend
		send_size = sizeof(struct msg_hdr) + sizeof(struct NoteSerialize) + SHA256_DIGEST_LENGTH;
		send_msg = malloc(send_size);
		send_msg->action = FETCH;
		send_msg->msg_size = send_size - sizeof(struct msg_hdr);
		serialize_p = (NoteSerialize_t)send_msg->msg_content;

		memcpy(&(serialize_p->common), &(tmp->common), sizeof(struct NoteCommon));
		memcpy(serialize_p->content, passwd_hash, sizeof(passwd_hash));

		send_data(&ipc, RECEIVER, send_msg, send_size);
		free(send_msg);

		rc = recv_data_timeout(&ipc, SENDER, (void **)&recv_msg, &recv_size, 60);
		if(IS_ERR(rc) || recv_size < sizeof(struct msg_hdr)){
			printf("Unable to read content\n");
			return;
		}

		serialize_p = (NoteSerialize_t)recv_msg->msg_content;
		printf("Content: %s\n", serialize_p->content);

	} else {
		printf("Content: %s\n", tmp->note_content);
	}
}

int note_sync(int flag)
{
	msg_hdr_t msg_hdr = NULL;
	uint32_t send_size, recv_size;
	struct msg_hdr inline_msg_hdr;
	Note_t cur_note, next_note, next_note2;
	NoteSerialize_t serialize_p;
	uint64_t status;
	uint32_t read_count = 0;
	int rc;

	if(flag == 1){
		send_size = sizeof(struct msg_hdr);

		next_note = notes;
		next_note2 = notes;

		// commit un-synced note to backend
		DL_FOREACH(next_note, cur_note){
			if(cur_note->note_synced)
				continue;
			send_size += sizeof(struct NoteSerialize) + cur_note->note_content_len;
			if(send_size > SHM_MEM_MAX_SIZE){
				next_note = cur_note;
				break;
			}
		}

		if(send_size == sizeof(struct msg_hdr)){
			printf("All notes was synced\n");
			return 0;
		}

		msg_hdr = malloc(send_size);
		msg_hdr->action = COMMIT;
		msg_hdr->msg_size = send_size - sizeof(struct msg_hdr);
		serialize_p = (NoteSerialize_t)msg_hdr->msg_content;

		DL_FOREACH(next_note2, cur_note) {
			if(cur_note->note_synced)
				continue;
			memcpy(&(serialize_p->common), &(cur_note->common), sizeof(struct NoteCommon));
			memcpy(serialize_p->content, cur_note->note_content, cur_note->note_content_len);
			serialize_p = (NoteSerialize_t)((size_t)serialize_p + sizeof(struct NoteSerialize) + cur_note->note_content_len);
			cur_note->note_synced = 1;
		}

		send_data(&ipc, RECEIVER, msg_hdr, send_size);
		free(msg_hdr);

		rc = recv_data_timeout(&ipc, SENDER, NULL, (uint64_t *)&status, 60);
		if(IS_ERR(rc) || status != OK){
			printf("Unable to commit data to backend\n");
			return 1;
		}

	} else {
		// fetch from backend
		inline_msg_hdr.action = FETCH;
		inline_msg_hdr.msg_size = 0xFFFFFFFF; // fetch all except encrypted note content
		send_data(&ipc, RECEIVER, &inline_msg_hdr, sizeof(inline_msg_hdr));

		int truncated = 0;
		do{
			truncated = 0;
			rc = recv_data_timeout(&ipc, SENDER, (void **)&msg_hdr, (uint64_t *)&recv_size, 60);
			if(IS_ERR(rc) || recv_size < sizeof(struct msg_hdr)){
				if((Status)recv_size == OK){
					return 0;
				} else {
					printf("Unable to fetch data from backend\n");
					return 1;
				}
			}

			if(msg_hdr->action == TRUNCATED)
				truncated = 1;

			Note_t search_note;
			// parse from backend
			while(read_count < msg_hdr->msg_size){
				serialize_p = (NoteSerialize_t)((size_t)msg_hdr->msg_content + read_count);
				Note_t new_note = Note_init(serialize_p->note_title,
											serialize_p->note_author,
											serialize_p->note_content_len,
											serialize_p->note_is_encrypt);

				read_count += sizeof(struct NoteSerialize);
				Note_t p_note;
				DL_SEARCH(notes, search_note, new_note, Note_cmp);
				p_note = search_note;
				if(!search_note){
					p_note = new_note;
				}

				// update new content
				if(!p_note->note_is_encrypt){
					memcpy(p_note->note_content, serialize_p->content, serialize_p->note_content_len);
					read_count += new_note->note_content_len;
				}

				if(p_note->note_is_encrypt) {
					p_note->note_synced = 1;
					if(p_note->note_content){
						free(p_note->note_content);
						p_note->note_content = NULL;
					}
				}

				if(!search_note){
					DL_APPEND(notes, new_note);
				} else {
					Note_destroy(new_note);
				}
			}

			if(truncated){
				// signal backend send next data
				send_data(&ipc, RECEIVER, NULL, OK);
			}
		} while(truncated);
	}
	return 0;
}

int note_main()
{
	int rc;
	uint64_t status = Empty;
	char buf[64];

	DBG("Waiting for backend is up....\n");
	rc = recv_data_timeout(&ipc, SENDER, NULL, (uint64_t *)&status, 60); // wait for 1 min
	if(!IS_OK(rc)){
		ERROR("Unable to receive signal from backend process\n");
		return -1;
	}

	if(status != OK){
		ERROR("receive error status from backend\n");
		return -1;
	}

	// tell backend we are ok to work now
	status = OK;
	rc = send_data(&ipc, RECEIVER, NULL, OK);

	int op;
	int exit = 0;

	//sleep(1);
	while(!exit){
		printf("==== Secure Note Manager ====\n");
		printf("1. Add New Note\n");
		printf("2. List Note\n");
		printf("3. Read Note\n");
		printf("4. Edit Note\n");
		printf("5. Delete Note\n");
		printf("6. Sync Notes\n");
		printf("7. Exit\n");
		printf("Choice: ");
		op = read_int();
		switch(op){
			case 1:
				add_new_note();
				break;
			case 2:
				list_note();
				break;
			case 3:
				read_note();
				break;
			case 4:
				edit_note();
				break;
			case 5:
				delete_note();
				break;
			case 6:
				do{
					printf("You you want to [s]ync or [c]ommit note? (s/c)");
					bzero(buf, sizeof(buf));
					read_line(buf, sizeof(buf) - 1);
				}while(buf[0] != 's' && buf[0] != 'c');
				if(buf[0] == 'c'){
					note_sync(1);
				}else {
					note_sync(0);
				}
				break;
			case 7:
				note_sync(1);
				exit=1;
				break;
			default:
				printf("Invalid input\n");
				break;
		}
	}

	send_data(&ipc, RECEIVER, NULL, Exit);
	return 0;
}

int main(int argc, char **argv)
{
	pid_t pid;
	char ev_fds_str[64] = {0};

	if(argc < 2){
		ERROR("Missing backend binary path\n");
		return 1;
	}

	IPC_create(&ipc, 1, 0, 1);

	setvbuf(stdin, NULL, _IONBF, 0);
	setvbuf(stdout, NULL, _IONBF, 0);
	serialize_ev_fd(&ipc, ev_fds_str, sizeof(ev_fds_str));

	const char *child_argv[32] = {
		argv[1],
		ev_fds_str,
		NULL
	};

	pid = fork();
	if(pid == 0){
		// child Process
		if(setgid(1001) == -1){
			DBG("Unable to drop privilege setgid\n");
		}
		cap_t proc = cap_get_proc();
		cap_clear(proc);
		if(cap_set_proc(proc)){
			DBG("cap_set_proc was failed\n");
		}

		execv(argv[1], child_argv);
	} else if(pid > 0){
		// parent process
		note_main();
		int waitStatus;
		waitpid(pid, &waitStatus, 0);

	} else {
		perror("fork");
	}

	return 0;
}
