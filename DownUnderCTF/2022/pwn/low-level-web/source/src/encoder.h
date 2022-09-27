#ifndef __ENCODER_H_
#define __ENCODER_H_

#include <string>
#include <cstring>

std::string hex_to_base64_impl(std::string buf);
std::string base64_to_hex_impl(std::string buf);

#endif // __ENCODER_H_
