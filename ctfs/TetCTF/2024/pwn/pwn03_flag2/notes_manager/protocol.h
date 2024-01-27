/*
 * protocol.h
 * Author: peternguyen93
 * Struct definations to communicate between interface and backend
 */

#ifndef PROTOCOL_H
#define PROTOCOL_H

#include <stdint.h>
#include "utlist.h"

enum Status {
	Empty = 0,
	OK = 1,
	Error = 2,
	Timeout = 3,
	Exit = 4
};
typedef enum Status Status;

typedef enum Action {
	NONE = 0,
	COMMIT = 1,
	FETCH = 2,
	DELETE = 3,
	AUTH = 4,
	TRUNCATED = 5 // use for reply_msg is larger than SHM_MEM_MAX_SIZE
} Action;

struct msg_hdr {
	Action action;
	uint32_t msg_size;
	char msg_content[];
};
typedef struct msg_hdr * msg_hdr_t;

#define MAX_LEN 64

struct NoteCommon {
	char title[MAX_LEN];
	char author[32];
	uint32_t content_len;
	uint32_t flags;
	uint32_t encrypt:1;
	uint32_t synced:1; // unsed in backend
};

#define note_title common.title
#define note_author common.author
#define note_content_len common.content_len
#define note_is_encrypt common.encrypt
//#define note_content common.content
#define note_synced common.synced

// interface
struct Note {
	struct NoteCommon common;
	char *note_content;
	struct Note *prev;
	struct Note *next;
};
typedef struct Note * Note_t;

// backend site
struct NoteBackend {
	struct NoteCommon common;
	uint8_t passwd[32]; // SHA256_DIGEST_LENGTH
	char *note_content;
	struct NoteBackend *prev;
	struct NoteBackend *next;
};
typedef struct NoteBackend* NoteBackend_t;

struct NoteSerialize {
	struct NoteCommon common;
	char content[];
};
typedef struct NoteSerialize * NoteSerialize_t;

#endif
