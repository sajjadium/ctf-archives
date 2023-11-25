#pragma once

#include "types.h"

#define BITMAP_BYTE_COUNT(number_of_bits) (number_of_bits / Bitmap::bits_per_bitmap_atom_ + ((number_of_bits % Bitmap::bits_per_bitmap_atom_ > 0) ? 1 : 0))

class Bitmap
{
  public:

    static uint8 const bits_per_bitmap_atom_;

    Bitmap(size_t number_of_bits);
    Bitmap(const Bitmap &bm);
    ~Bitmap();

    bool setBit(size_t bit_number);
    static bool setBit(uint8* b, size_t& num_bits_set, size_t bit_number);

    bool getBit(size_t bit_number);
    static bool getBit(uint8* b, size_t bit_number);

    bool unsetBit(size_t bit_number);
    static bool unsetBit(uint8* b, size_t& num_bits_set, size_t bit_number);

    size_t getSize();

    /**
     * returns the number of bits set
     * @return the number of bits set
     */
    size_t getNumBitsSet();

    /**
     * returns the number of unset bits
     * @return the number of unset bits
     */
    size_t getNumFreeBits();

    /**
     * prints the bitmap using kprintfd
     */
    void bmprint();
    static void bmprint(uint8* b, size_t n, size_t num_bits_set);

    /**
     * sets a whole byte in the bitmap
     * only use if you know what you are doing
     * @param byte_number the number of the byte to set
     * @param byte the byte to set
     */
    void setByte(size_t byte_number, uint8 byte);

    /**
     * returns a whole byte of a given number
     * only use if you know what you are doing
     * @param byte_number the number of the byte to return
     * @return the byte
     */
    uint8 getByte(size_t byte_number);

  private:
    size_t size_;
    size_t num_bits_set_;
    uint8 *bitmap_;
};

