/*
 * This process store secret data submited from user
 * Author: peternguyen
 */
#include "ipc.h"
#include "dbg.h"
#include "protocol.h"
#include "utlist.h"
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <openssl/sha.h>
#include <openssl/evp.h>

struct IPC ipc;
#define MAX_CONTENT_LEN 0x1000
#define MAX_NOTE 0x100

NoteBackend_t notes;
uint32_t notes_size = 0;

unsigned char IV[] = "\x0A\x91\x72\x71\x6A\xE6\x42\x84\x09\x88\x5B\x8B\x82\x9C\xCB\x05";

typedef enum CryptMode {
	Encrypt = 1,
	Decrypt = 0
} CryptMode;

static inline size_t roundup(size_t value, size_t base)
{
	if(value % base == 0)
		return value;
	return (value / base) * base + base;
}

int Note_Crypt(const char *key,
		const char *inbuf, const size_t inbuf_size,
		char **out_buf, size_t *out_size, CryptMode mode)
{
	EVP_CIPHER *cipher = EVP_aes_256_cbc();//_CTX ctx;
	EVP_CIPHER_CTX *ctx;
	size_t block_size, out_buf_size = 0;
	int outlen = 0;

	*out_size = 0;
	//assert_fail_f(*out_buf, "NULL out_buf pointer\n");
	if(!(ctx = EVP_CIPHER_CTX_new())){
		return 0;
	}

	if(!EVP_CipherInit_ex(ctx, cipher, NULL, (const unsigned char *)key, (const unsigned char *)IV, mode)){
		return 0;
	}

	block_size = EVP_CIPHER_CTX_get_block_size(ctx);
	out_buf_size = roundup(inbuf_size, block_size);
	*out_buf = malloc(out_buf_size);

	if(!EVP_CipherUpdate(ctx, (unsigned char *)*out_buf, &outlen, (unsigned char*)inbuf, inbuf_size)){
		free(*out_buf);
		*out_buf = NULL;
		return 0;
	}

	if(!EVP_CipherFinal(ctx, (unsigned char *)((*out_buf) + outlen), &outlen)){
		free(*out_buf);
		*out_buf = NULL;
		return 0;
	}

	*out_size = out_buf_size;
	EVP_CIPHER_CTX_free(ctx);
	return 1;
}

int NoteBackend_cmp(NoteBackend_t note1, NoteBackend_t note2)
{
	int res = strncmp(note1->note_title, note2->note_title, sizeof(note1->note_title) - 1) == 0 && \
			strncmp(note2->note_author, note1->note_author, sizeof(note1->note_author) - 1) == 0;
	return !res;
}

NoteBackend_t NoteBackend_init(
	char *title,
	char *author,
	uint32_t content_len,
	uint32_t encrypt)
{
	NoteBackend_t new_note = (NoteBackend_t)malloc(sizeof(struct NoteBackend));
	bzero(new_note, sizeof(struct NoteBackend));
	strncpy(new_note->note_title, title, sizeof(new_note->note_title) - 1);
	strncpy(new_note->note_author, author, sizeof(new_note->note_author) - 1);

	new_note->note_content_len = content_len;
	new_note->note_is_encrypt = encrypt;
	return new_note;
}

void NoteBackend_destroy(NoteBackend_t note)
{
	assert_fail_f(note, "note could not be null\n");
	if(note->note_content){
		free(note->note_content);
		note->note_content = NULL;
	}
	bzero((void *)note, sizeof(struct NoteBackend));
	free(note);
}

void backend_listener()
{
	uint64_t status = 0;
	uint64_t msg_size = 0;
	msg_hdr_t msg;
	int rc;
	uint32_t action;

	status = OK;
	rc = send_data(&ipc, SENDER, NULL, status);
	if(IS_ERR(rc)){
		perror("send_data error");
		return;
	}

	DBG("Waiting for interface send signal...\n");
	status = 0;
	rc = recv_data_timeout(&ipc, RECEIVER, NULL, (uint64_t *)&status, 60);
	if(IS_ERR(rc)){
		perror("recv_data_timeout");
		return;
	}

	assert_fail_f((Status)status == OK, "[backend] Receive error from SENDER %d\n", (Status)status);
	DBG("[backend] interface process is up, let waiting for request\n");

	while(1){
		// handle request from interface
		msg_size = 0;
		rc = recv_data_timeout(&ipc, RECEIVER, (void **)&msg, &msg_size, 60 * 4);
		DBG("[Backend] rc: %d\n", rc);
		if(IS_ERR(rc) || IS_TIMEOUT(rc)){
			continue;
		}

		if(msg_size == Exit){
			DBG("[Backend] receive signal exit\n");
			break;
		}

		DBG("[Backend] Receive %d data from RECEIVER\n", msg_size);
		if(msg_size < sizeof(struct msg_hdr)){
			DBG("[Backend] msg_size is too small\n");
			continue;
		}

		action = msg->action;
		uint32_t msg_size = msg->msg_size;
		uint32_t parsed_count = 0;
		NoteBackend_t tmp1, etmp;
		struct NoteBackend inline_tmp;
		int parsed_error = OK;
		NoteSerialize_t serialize_note = NULL;
		msg_hdr_t reply_msg = NULL;
		uint32_t reply_size = 0;
		uint32_t written_count = 0;
		char *encrypt_buf = NULL;
		size_t encrypt_size = 0;

		switch(action){
			case COMMIT: {
				if(msg_size < sizeof(struct NoteSerialize)){
					DBG("[backend] msg content size is too small\n");
					send_data(&ipc, SENDER, NULL, Error);
					break;
				}
				parsed_count = 0;
				while(parsed_count + sizeof(struct NoteSerialize) < msg_size){
					serialize_note = (NoteSerialize_t)((size_t)msg->msg_content + parsed_count);

					if(serialize_note->note_content_len + parsed_count + sizeof(struct NoteSerialize) > msg_size){
						DBG("[backend] serialize_note->note_content_len is too big: %d\n", serialize_note->note_content_len);
						parsed_error = Error;
						break;
					}

					if(serialize_note->note_is_encrypt && serialize_note->note_content_len < SHA256_DIGEST_LENGTH){
						DBG("[backend] encrypted note note_content_len is too small\n");
						parsed_error = Error;
						break;
					}

					NoteBackend_t new_note = NoteBackend_init(serialize_note->note_title,
															serialize_note->note_author,
															serialize_note->note_content_len,
															serialize_note->note_is_encrypt);
					uint32_t content_len = serialize_note->note_content_len;
					if(serialize_note->note_is_encrypt){
						content_len = serialize_note->note_content_len - SHA256_DIGEST_LENGTH;
					}

					DL_SEARCH(notes, tmp1, new_note, NoteBackend_cmp);
					parsed_error = OK;
					if(tmp1){
						// update content only;
						DBG("[backend] COMMIT: update content for %s - %s\n", tmp1->note_title, tmp1->note_author);
						if(tmp1->note_is_encrypt && memcmp(tmp1->passwd, serialize_note->content, SHA256_DIGEST_LENGTH) == 0){
							// access granted
							DBG("[backend] COMMIT: access granted for encrypted note - update new content\n");
							Note_Crypt((const char *)tmp1->passwd,
											(const char *)&(serialize_note->content[SHA256_DIGEST_LENGTH]),
											(const size_t)content_len,
											&encrypt_buf,
											&encrypt_size,
											Encrypt);
							if(tmp1->note_content){
								free(tmp1->note_content);
							}
							tmp1->note_content = encrypt_buf;
							tmp1->note_content_len = encrypt_size;
						} else if(!tmp1->note_is_encrypt){
							DBG("[backend] COMMIT: update new content_len: %d\n", content_len);

							if(tmp1->note_content){
								free(tmp1->note_content);
							}

							tmp1->note_content = malloc(content_len);
							tmp1->note_content_len = content_len;
							memcpy(tmp1->note_content, serialize_note->content, serialize_note->note_content_len);
						}
						NoteBackend_destroy(new_note);
					} else {
						if(notes_size + 1 > MAX_NOTE){
							send_data(&ipc, SENDER, NULL, Error);
							break;
						}

						if(new_note->note_is_encrypt){
							memcpy(new_note->passwd, serialize_note->content, SHA256_DIGEST_LENGTH);
						}
						
						if(new_note->note_is_encrypt){
							// aes encrypt content
							Note_Crypt((const char *)new_note->passwd,
										(const char *)serialize_note->content + SHA256_DIGEST_LENGTH,
										(const size_t)content_len,
										&(new_note->note_content),
										(size_t *)&(new_note->note_content_len),
										Encrypt);
						} else {
							new_note->note_content = malloc(content_len);
							memcpy(new_note->note_content, serialize_note->content, content_len);
						}
						DBG("[backend] Addded new_note %s(%s) - encrypt: %d\n",
															new_note->note_title,
															new_note->note_author, new_note->note_is_encrypt);
						DL_APPEND(notes, new_note);
						notes_size++;
					}
					parsed_count += sizeof(struct NoteSerialize) + serialize_note->note_content_len;
				}
				DBG("parsed_error: 0x%x\n", parsed_error);
				send_data(&ipc, SENDER, NULL, parsed_error);
				break;
			}
			case DELETE: {
				parsed_error = Error;
				if(msg_size >= sizeof(struct NoteSerialize)){
					tmp1 = NULL;
					serialize_note = (NoteSerialize_t)msg->msg_content;
					uint32_t content_len = serialize_note->note_content_len;
					etmp = NoteBackend_init(serialize_note->note_title,
											serialize_note->note_author,
											serialize_note->note_content_len,
											serialize_note->note_is_encrypt);

					DL_SEARCH(notes, tmp1, etmp, NoteBackend_cmp);
					if(tmp1){
						DBG("[backend] DELETE: found delete note: %s(%s) - encrypt: %d\n",
											tmp1->note_title, tmp1->note_author, tmp1->note_is_encrypt);
						// found note
						if((tmp1->note_is_encrypt &&
								memcmp(tmp1->passwd, serialize_note->content, SHA256_DIGEST_LENGTH) == 0) ||
							!tmp1->note_is_encrypt){
							// verify password before destroy
							goto delete_note;
						} else if(!tmp1->note_is_encrypt) {
delete_note:
							parsed_error = OK;
							DL_DELETE(notes, tmp1);
							NoteBackend_destroy(tmp1);
							notes_size--;
							DBG("[backend] DELETE: successfully delete this note\n");
						}
					} else {
						DBG("[backend] DELETE: unable to find note: %s(%s)\n", tmp1->note_title, tmp1->note_author);
					}
					NoteBackend_destroy(etmp);
				} else {
					DBG("[backend] DELETE: msg_content_len is too small %d - %d\n", msg_size, sizeof(struct NoteSerialize));
				}
				send_data(&ipc, SENDER, NULL, parsed_error);
				break;
			}
			case AUTH: {
				parsed_error = Error;
				if(msg_size >= sizeof(struct NoteSerialize)){
					tmp1 = NULL;
					serialize_note = (NoteSerialize_t)msg->msg_content;
					if(serialize_note->note_is_encrypt && serialize_note->note_content_len == SHA256_DIGEST_LENGTH) {
						etmp = NoteBackend_init(serialize_note->note_title,
											serialize_note->note_author,
											serialize_note->note_content_len,
											serialize_note->note_is_encrypt);

						DL_SEARCH(notes, tmp1, etmp, NoteBackend_cmp);
						NoteBackend_destroy(etmp);

						DBG("[backend] Authenticate with note: %s - %s\n", tmp1->note_title, tmp1->note_author);
						if(tmp1 && tmp1->note_is_encrypt && memcmp(tmp1->passwd, serialize_note->content, SHA256_DIGEST_LENGTH) == 0){
							parsed_error = OK;
							DBG("[backend] Access granted\n");
						}
					} else {
						DBG("[backend] AUTH messge conent len is too small: %d\n", serialize_note->note_content_len);
					}
				} else {
					DBG("[backend] AUTH message content is too small: %d\n", msg_size);
				}
				send_data(&ipc, SENDER, NULL, parsed_error);
				break;
			}
			case FETCH: {
				if(msg_size != 0xFFFFFFFF){
					DBG("[backend] Fetch encrypt note\n");
					//fetch single encrypted note
					if(msg_size < sizeof(struct NoteSerialize) + SHA256_DIGEST_LENGTH){
						DBG("[backend] FETCH - msg content size is too small: %d\n", msg_size);
						send_data(&ipc, SENDER, NULL, Error);
						break;
					}

					serialize_note = (NoteSerialize_t)msg->msg_content;
					
					memcpy(&(inline_tmp.common), &(serialize_note->common), sizeof(struct NoteCommon));
					DL_SEARCH(notes, tmp1, &inline_tmp, NoteBackend_cmp);
					if(!tmp1){
						DBG("[backend] Unable to find note %s - %s\n", inline_tmp.note_title, inline_tmp.note_author);
						send_data(&ipc, SENDER, NULL, Error);
						break;
					}

					if(!tmp1->note_is_encrypt){
						DBG("[backend] This note was not encrypted\n");
						send_data(&ipc, SENDER, NULL, Error);
						break;
					}

					if(memcmp(tmp1->passwd, serialize_note->content, SHA256_DIGEST_LENGTH)){
						DBG("[backend] Password incorrect\n");
						send_data(&ipc, SENDER, NULL, Error);
						break;
					}

					// aes decrypt here
					char *decrypt_buffer = NULL;
					size_t decrypt_len = 0;
					Note_Crypt((const char *)tmp1->passwd, (const char *)tmp1->note_content,
											(const size_t)tmp1->note_content_len,
											&decrypt_buffer, (size_t *)&decrypt_len,
											Decrypt);

					// everything is ok
					// send it back
					reply_size = sizeof(struct msg_hdr) + sizeof(struct NoteSerialize) + decrypt_len;
					reply_msg = malloc(reply_size);
					reply_msg->msg_size = reply_size - sizeof(struct msg_hdr);
					serialize_note = (NoteSerialize_t)reply_msg->msg_content;

					memcpy(&(serialize_note->common), &(tmp1->common), sizeof(struct NoteCommon));
					serialize_note->note_content_len = decrypt_len;
					memcpy(serialize_note->content, decrypt_buffer, decrypt_len);
					free(decrypt_buffer);

					send_data(&ipc, SENDER, reply_msg, reply_size);
					free(reply_msg);

					break;
				}

				DBG("[backend] FETCH all notes except encrypted notes\n");
				NoteSerialize_t serialize_p = NULL;
				NoteBackend_t cur_note = notes;
				NoteBackend_t tmp_note2 = NULL;
				int truncated = 0;
				uint32_t tmp_size = 0;

				// fetch all
				do {
					truncated = 0;
					reply_size = sizeof(struct msg_hdr);
					DL_FOREACH_SAFE(cur_note, tmp1, etmp){
						tmp_size = sizeof(struct NoteSerialize);
						if(!tmp1->note_is_encrypt){
							tmp_size += tmp1->note_content_len;
						}
						if(reply_size + tmp_size > SHM_MEM_MAX_SIZE){
							DBG("[backend] reply_size(%d) is larger than SHM_MEM_MAX_SIZE, enable truncated mode\n", reply_size + tmp_size);
							truncated = 1;
							tmp_note2 = tmp1;
							break;
						}
						reply_size += tmp_size;
					}

					if(reply_size == sizeof(struct msg_hdr)){
						DBG("[backend] nodes is empty\n");
						// notes is empty just return OK
						send_data(&ipc, SENDER, NULL, OK);
						break;
					}

					DBG("[backend] FETCH: msg truncated: %d\n", truncated);

					reply_msg = malloc(reply_size);
					reply_msg->action = truncated ? TRUNCATED : NONE;
					reply_msg->msg_size = reply_size - sizeof(struct msg_hdr);

					written_count = 0;
					DL_FOREACH_SAFE(cur_note, tmp1, etmp){
						serialize_p = (NoteSerialize_t)((size_t)reply_msg->msg_content + written_count);
						
						memcpy(&(serialize_p->common), &(tmp1->common), sizeof(struct NoteCommon));
						written_count+= sizeof(struct NoteSerialize);
						DBG("[backend] FETCH: serialize note %s(%s)\n", serialize_p->note_title, serialize_p->note_author);
						if(!tmp1->note_is_encrypt){
							written_count += tmp1->note_content_len;
							memcpy(serialize_p->content, tmp1->note_content, tmp1->note_content_len);
						}
					}

					send_data(&ipc, SENDER, reply_msg, reply_size);
					free(reply_msg);

					if(truncated){
						uint64_t status = 0;
						rc = recv_data_timeout(&ipc, RECEIVER, NULL, &status, 60);
						if(IS_ERR(rc) || (Status)status != OK){
							DBG("[backend] Send truncated message error\n");
							break;
						}

						if(tmp_note2){
							cur_note = tmp_note2;
						}
					}

				}while(truncated);
				break;
			}
			default:
				DBG("[Backend] Unsupported action %d\n", action);
				break;
		}
	}
}

int main(int argc, char **argv)
{
	if(argc < 2){
		ERROR("Usage %s <EVFD_String>\n", argv[0]);
		return 1;
	}
	char *ipc_env = argv[1];

#ifdef DEBUG
	int uid = getuid();
	int gid = getgid();
	DBG("[backend] uid = %d - gid = %d\n", uid, gid);
#endif

	if(!ipc_env){
		printf("ipc_env is NULL\n");
		return 1;
	}

	notes = NULL;
	//assert_fail_f(ipc_env != NULL, "Unable to get IPC_ENV environment variable");
	IPC_create(&ipc, 0, EFD_NONBLOCK, 0);
	parse_ev_fds(&ipc, ipc_env);

	backend_listener();
	return 0;
}
