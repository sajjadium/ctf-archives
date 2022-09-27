#include "encoder.h"

static const char* const hex_chars = "0123456789abcdef";

void hex_to_bytes(std::string buf, char* out, size_t len)
{
    char tmp[1000];

    for (size_t i = 0; i < len; i++) {
        tmp[i] = tolower(buf[i]);
    }

    for (size_t i = 0; i < len; i += 2) {
        char x = strchr(hex_chars, tmp[i]) - hex_chars;
        char y = strchr(hex_chars, tmp[i+1]) - hex_chars;
        tmp[i/2] = (x << 4 | y);
    }

    snprintf(out, len/2 + 1, tmp);
}

std::string bytes_to_hex(char* buf, size_t len)
{
    std::string ret;
    char tmp[500];
    memcpy(tmp, buf, len);
    
    for (size_t i = 0; i < len; i++) {
        ret += hex_chars[(tmp[i] & 0xf0) >> 4];
        ret += hex_chars[(tmp[i] & 0x0f)];
    }

	return ret;
}

static const std::string base64_chars =
             "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
             "abcdefghijklmnopqrstuvwxyz"
             "0123456789+/";


static inline bool is_base64(unsigned char c) {
    return (isalnum(c) || (c == '+') || (c == '/'));
}

std::string bytes_to_base64(char* buf, size_t len) {
  	unsigned char char_array_3[3], char_array_4[4];
	std::string ret;

	int i = 0;
  	while (len--) {
    	char_array_3[i++] = *(buf++);

    	if (i == 3) {
      		char_array_4[0] = (char_array_3[0] & 0xfc) >> 2;
      		char_array_4[1] = ((char_array_3[0] & 0x03) << 4) + ((char_array_3[1] & 0xf0) >> 4);
      		char_array_4[2] = ((char_array_3[1] & 0x0f) << 2) + ((char_array_3[2] & 0xc0) >> 6);
      		char_array_4[3] = char_array_3[2] & 0x3f;

      		for (i = 0; i < 4; i++) {
        		ret += base64_chars[char_array_4[i]];
			}

      		i = 0;
    	}
  	}

  	if (i) {
    	for (int j = i; j < 3; j++) {
      		char_array_3[j] = 0;
		}

    	char_array_4[0] = (char_array_3[0] & 0xfc) >> 2;
    	char_array_4[1] = ((char_array_3[0] & 0x03) << 4) + ((char_array_3[1] & 0xf0) >> 4);
    	char_array_4[2] = ((char_array_3[1] & 0x0f) << 2) + ((char_array_3[2] & 0xc0) >> 6);
    	char_array_4[3] = char_array_3[2] & 0x3f;

    	for (int j = 0; j < i + 1; j++) {
      		ret += base64_chars[char_array_4[j]];
		}

		while (i++ < 3) {
      		ret += '=';
		}
  	}

  	return ret;
}

size_t base64_to_bytes(std::string buf, char* out) {
    int len = buf.size();
    unsigned char char_array_4[4], char_array_3[3];

    int i = 0;
    int j = 0;
    int k = 0;
    size_t l = 0;

    while (len-- && (buf[k] != '=') && is_base64(buf[k])) {
        char_array_4[i++] = buf[k];
        k++;
        
        if (i == 4) {
            for (i = 0; i < 4; i++) {
                char_array_4[i] = base64_chars.find(char_array_4[i]);
            }

            char_array_3[0] = (char_array_4[0] << 2) + ((char_array_4[1] & 0x30) >> 4);
            char_array_3[1] = ((char_array_4[1] & 0xf) << 4) + ((char_array_4[2] & 0x3c) >> 2);
            char_array_3[2] = ((char_array_4[2] & 0x3) << 6) + char_array_4[3];

            for (i = 0; (i < 3); i++) {
                out[l++] = char_array_3[i];
            }

            i = 0;
        }
    }

    if (i) {
        for (j = i; j <4; j++) {
            char_array_4[j] = 0;
        }

        for (j = 0; j <4; j++) {
            char_array_4[j] = base64_chars.find(char_array_4[j]);
        }

        char_array_3[0] = (char_array_4[0] << 2) + ((char_array_4[1] & 0x30) >> 4);
        char_array_3[1] = ((char_array_4[1] & 0xf) << 4) + ((char_array_4[2] & 0x3c) >> 2);
        char_array_3[2] = ((char_array_4[2] & 0x3) << 6) + char_array_4[3];

        for (j = 0; (j < i - 1); j++) {
            out[l++] = char_array_3[j];
        }
    }
   
    return l;
}

std::string hex_to_base64_impl(std::string buf)
{
    char bytes[1000];
    size_t len = buf.size();
    hex_to_bytes(buf, bytes, len);
    return bytes_to_base64(bytes, len / 2);
}

std::string base64_to_hex_impl(std::string buf)
{
    char bytes[1000];
    size_t len = base64_to_bytes(buf, bytes);
    return bytes_to_hex(bytes, len);
}
