#include <stdlib.h>
#include <stdint.h>
#include <stdatomic.h>
#include <unistd.h>
#include <poll.h>
#include <fcntl.h>
#include <string.h>
#include <sys/wait.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <sodium.h>
#include <err.h>
#include <errno.h>
#include <sys/random.h>


#define ENC_BUF_LIMIT 256
#define ENC_BUF_OFFSET 6
#define CRYPT_LEN_LIMIT (ENC_BUF_LIMIT - 1 - ENC_BUF_OFFSET)/4*3
#define MESSAGE_LEN_LIMIT CRYPT_LEN_LIMIT - crypto_aead_xchacha20poly1305_ietf_NPUBBYTES - crypto_aead_xchacha20poly1305_ietf_ABYTES


static struct randombytes_implementation rimp;

volatile static atomic_uint_fast64_t rcount;
static uint8_t rkey[crypto_core_hchacha20_KEYBYTES];
static uint8_t aeadkey[crypto_aead_xchacha20poly1305_ietf_KEYBYTES];


size_t sat_sub(size_t a, size_t b) {
	size_t res;
	
	res = a - b;
	res &= -(res <= a);

	return res;
}


uint_fast64_t increment_rcount() {
	return atomic_fetch_add(&rcount, 1);
}

const char* rimplementation_name() {
	return "SecFast (SF) Military Grade 256-bit Random";
}

static inline void fill_rsmall(uint8_t out[crypto_core_hchacha20_OUTPUTBYTES]) {
	uint8_t in[crypto_core_hchacha20_INPUTBYTES] = {0x00};
	
	*((uint_fast64_t*)in) = increment_rcount();
	crypto_core_hchacha20((unsigned char*)out, (const unsigned char*)in, (const unsigned char*)rkey, NULL);
}

uint32_t rrandom() {
	uint32_t* out_converted;
	uint8_t out[crypto_core_hchacha20_OUTPUTBYTES];
	
	fill_rsmall(out);
	out_converted = (uint32_t*)out;
	return *out_converted;
}

void rstir() {
	int collected, needed, stored;
	
	needed = crypto_core_hchacha20_KEYBYTES;
	stored = collected = 0;
	
	while (needed) {
		if ((collected = getrandom((void*)(rkey + stored), needed, GRND_RANDOM)) == -1) err(1, "Error collecting random data");
		needed -= collected;
		stored += collected;
	}
}

void rbuf(void * const buf, const size_t size) {
	uint8_t small_out[crypto_core_hchacha20_OUTPUTBYTES];
	uint8_t *buf_out, *limit;
	size_t leftover, i;
	
	buf_out = (uint8_t*)buf;
	leftover = size % crypto_core_hchacha20_OUTPUTBYTES;
	limit = buf_out + sat_sub(size, leftover);
	while(buf_out < limit) {
		fill_rsmall(buf_out);
		buf_out += crypto_core_hchacha20_OUTPUTBYTES;
	}
	if (leftover) {
		fill_rsmall(small_out);
		for(i = 0; i < leftover; i += 1) {
			buf_out[i] = small_out[i];
		}
	}
}

int init() {
	atomic_store(&rcount, 0);
	rstir();
	
	rimp.implementation_name = rimplementation_name;
	rimp.random = rrandom;
	rimp.stir = rstir;
	rimp.uniform = NULL;
	rimp.buf = rbuf;
	rimp.close = NULL;
	
	if (randombytes_set_implementation(&rimp)) errx(1, "Failed to set custom random implementation in libsodium.");
	if (sodium_init() == -1) errx(1, "Failed to initalize libsodium.");
	
	crypto_aead_xchacha20poly1305_ietf_keygen(aeadkey);
	
	return 0;
}

char* get_flag() {
	char* out;
	
	if(!(out = getenv("FLAG"))) {
		warnx("Using default flag.");
		out = "flag{TESTING_ONLY}";
	}
	
	return out;
}

uint16_t get_port() {
	long port;
	char* port_var_val;
	char* endchr;
	
	port_var_val = getenv("PORT");
	if (port_var_val) {
		errno = 0;
		port = strtol(port_var_val, &endchr, 10);
		if (errno) err(1, "Error interpreting PORT");
		if (errno || *endchr || port != (port & 0xFFFF) || !port) {
			errx(1, "The provided port was not a number greater than 0 and less than 65536.");
			return 0;
		}
	} else {
		warnx("Using default port.");
		return 3000;
	}
	
	return (uint16_t)port;
}

char* ee_buf(unsigned char* enc_buf, const unsigned char* in_buf, size_t buf_len) {
	uint8_t crypt_buf[CRYPT_LEN_LIMIT];
	
	randombytes_buf((void* const)(crypt_buf + buf_len), crypto_aead_xchacha20poly1305_ietf_NPUBBYTES);
	crypto_aead_xchacha20poly1305_ietf_encrypt_detached((unsigned char*)crypt_buf, (unsigned char*)crypt_buf + buf_len + crypto_aead_xchacha20poly1305_ietf_NPUBBYTES, NULL, (const unsigned char*)in_buf, (unsigned long long)buf_len, NULL, 0, NULL, (const unsigned char*)crypt_buf + buf_len, (const unsigned char*)aeadkey);
	return sodium_bin2base64((char* const) enc_buf, sodium_base64_ENCODED_LEN(buf_len + crypto_aead_xchacha20poly1305_ietf_NPUBBYTES + crypto_aead_xchacha20poly1305_ietf_ABYTES, sodium_base64_VARIANT_URLSAFE_NO_PADDING), (const unsigned char* const)crypt_buf, buf_len + crypto_aead_xchacha20poly1305_ietf_NPUBBYTES + crypto_aead_xchacha20poly1305_ietf_ABYTES, sodium_base64_VARIANT_URLSAFE_NO_PADDING);
}

int child_process(int rsock, uint8_t* enc_buf) {
	size_t buf_len, transferred;
	uint8_t* enc_buf_transfer;
	
	buf_len = strlen(enc_buf) + 1;
	enc_buf[buf_len - 1] = '\n';
	enc_buf_transfer = enc_buf;
	while (buf_len) {
		if ((transferred = send(rsock, enc_buf_transfer, buf_len, 0)) == -1) err(1, "Sending failed");
		buf_len -= transferred;
		enc_buf_transfer += transferred;
	}
	
	enc_buf[0] = 0x6f;
	enc_buf[1] = 0x75;
	enc_buf[2] = 0x74;
	enc_buf[3] = 0x3a;
	enc_buf[4] = 0x20;
	enc_buf[5] = 0x20;
	buf_len = MESSAGE_LEN_LIMIT;
	enc_buf_transfer = enc_buf + ENC_BUF_OFFSET;
	while (buf_len) {
		if ((transferred = recv(rsock, enc_buf_transfer, buf_len, 0)) == -1) err(1, "Receiving failed");
		buf_len -= transferred;
		enc_buf_transfer += transferred;
	}
	
	ee_buf(enc_buf + ENC_BUF_OFFSET, enc_buf + ENC_BUF_OFFSET, MESSAGE_LEN_LIMIT);
	
	buf_len = strlen(enc_buf) + 1;
	enc_buf[buf_len - 1] = '\n';
	enc_buf_transfer = enc_buf;
	while (buf_len) {
		if ((transferred = send(rsock, enc_buf, buf_len, 0)) == -1) err(1, "Sending failed");
		buf_len -= transferred;
		enc_buf_transfer += transferred;
	}
	
	return 0;
}

int main() {
	int lsock, rsock;
	struct sockaddr_in addr;
	struct pollfd pfd;
	uint16_t port;
	pid_t pid;
	char* flag;
	size_t flag_len;
	uint8_t enc_buf[ENC_BUF_LIMIT] = {0x66, 0x6c, 0x61, 0x67, 0x3a, 0x20};
	
	init();
	
	port = get_port();
	if (!port) return 1;
	
	flag = get_flag();
	flag_len = strlen((const char*)flag);
	if (flag_len > MESSAGE_LEN_LIMIT) errx(1, "Flag is too long.");
	
	lsock = socket(AF_INET, SOCK_STREAM, 0);
	
	if (lsock == -1) err(1, "Error while creating socket");
	
	addr.sin_addr.s_addr = inet_addr("0.0.0.0");
	addr.sin_family = AF_INET;
	addr.sin_port = htons(port);
	
	if (bind(lsock, (struct sockaddr *)&addr, sizeof(addr)) == -1) err(1, "Error while binding to address");
	
	if (listen(lsock, 5) == -1) err(1, "Error while setting listen on address");
	
	if (fcntl(lsock, F_SETFL, O_NONBLOCK) == -1) err(1, "Error while setting the socket to non blocking");
	pfd.fd = lsock;
	pfd.events = POLLIN;
	
	while (1) {
		if (poll(&pfd, 1, 250) == -1) 	warn("Error polling socket");
		rsock = accept(lsock, NULL, NULL);
		if (rsock == -1) if (errno != EAGAIN && errno != EWOULDBLOCK)	warn("Error accepting connection");
		
		while((pid = waitpid(-1, NULL, WNOHANG)) > 0);
		if (pid == -1) if (errno != ECHILD) warn("Error waiting on child");
		
		if (rsock == -1) continue;
		
		
		ee_buf(enc_buf + ENC_BUF_OFFSET, flag, flag_len);
		
		
		pid = fork();
		if (pid == -1) {
			warn("Error forking");
			if (close(rsock) == -1) warn("Error closing fd");
		} else if (!pid) {
			if (close(lsock) == -1) warn("Error closing fd");
			if (child_process(rsock, enc_buf)) return 1;
			if (close(rsock) == -1) warn("Error closing fd");
			break;
		} else {
			if (close(rsock) == -1) warn("Error closing fd");
		}
	}
	
	return 0;
}

