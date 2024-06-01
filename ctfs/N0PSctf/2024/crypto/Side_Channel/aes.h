/*
 * Copyright (C) Telecom Paris
 * 
 * This file must be used under the terms of the CeCILL. This source
 * file is licensed as described in the file COPYING, which you should
 * have received as part of this distribution. The terms are also
 * available at:
 * https://cecill.info/licences/Licence_CeCILL_V2.1-en.html
*/

#ifndef __AES_H__

#define __AES_H__

#include <stdio.h>
#include <stdlib.h>
#include <inttypes.h>
#include <assert.h>

// 4 bytes array
typedef uint8_t word_t[4];
// encryption state: 4x4 bytes matrix; state[0] is the first (top) row;
// state[0][0] is the first (left) byte of the first row
typedef word_t state_t[4];
// key schedule: 44 (128 bits keys), 52 (192 bits keys) or 60 (256 bits keys) columns, 4 bytes each;
// round_key[0] is the w[0] of the AES standard
typedef word_t round_keys_t[60];

// AES functions
void addRoundKey(state_t s, const word_t rk[]);
uint8_t subByte(uint8_t b);
void subBytes(state_t s);
uint8_t invSubByte(uint8_t b);
void invSubBytes(state_t s);
void shiftRows(state_t s);
void invShiftRows(state_t s);
void mixColumns(state_t s);
void invMixColumns(state_t s);
void rotWord(word_t a);
void subWord(word_t a);
void keyExpansion(round_keys_t rk, const uint8_t key[16], const unsigned int len);
void cipher(uint8_t out[16], const uint8_t in[16], const unsigned int nr, const round_keys_t rk);
void invCipher(uint8_t out[16], const uint8_t in[16], const unsigned int nr, const round_keys_t rk);

// print n bytes array, bytes printed as 2 hex digits, separated by sep, with leading pre and trailing post strings
void printWord(const uint8_t w[], const unsigned int n, const char * const sep, const char * const pre, const char * const post);
// same as printWord but print in file f
void fprintWord(FILE *f, const uint8_t w[], const unsigned int n, const char * const sep, const char * const pre, const char * const post);
// print 16 bytes state as 4x4 matrix, 2 hex digits per cell
void printState(const state_t s);

#endif

// vim: set tabstop=4 softtabstop=4 shiftwidth=4 noexpandtab textwidth=0:
