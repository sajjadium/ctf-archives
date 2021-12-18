#ifndef TRUSTY_USER_DIARY_H
#define TRUSTY_USER_DIARY_H

#define MAX_MESSAGES 32U
#define MESSAGE_SIZE 0x4000

enum message_type {
	SLOW,
	ZERO_COPY,
};

#define ADD_MESSAGE 0x11U
#define ADD_MESSAGE_ZERO_COPY 0x22U
struct add_message_request {
	unsigned long id;
	union {
		void *message;
		unsigned long va_page;
	};
};

#define REMOVE_MESSAGE 0x33U
struct remove_message_request {
	unsigned long id;
};

#define UPDATE_MESSAGE 0x44U
struct update_message_request {
	unsigned long id;
	void *new_message;
};

#define READ_MESSAGE 0x55U
struct read_message_request {
	unsigned long id;
	void *dest_message;
};

#endif
