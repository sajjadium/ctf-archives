#include "Bitmap.h"
#include "kprintf.h"
#include "assert.h"
#include "kstring.h"

uint8 const Bitmap::bits_per_bitmap_atom_ = 8;

static const uint8 BIT_COUNT[] =
{
0, 1, 1, 2, 1, 2, 2, 3, 1, 2, 2, 3, 2, 3, 3, 4, 1, 2, 2, 3, 2, 3, 3, 4, 2, 3, 3, 4, 3, 4, 4, 5, 1, 2, 2, 3, 2, 3, 3, 4,
2, 3, 3, 4, 3, 4, 4, 5, 2, 3, 3, 4, 3, 4, 4, 5, 3, 4, 4, 5, 4, 5, 5, 6, 1, 2, 2, 3, 2, 3, 3, 4, 2, 3, 3, 4, 3, 4, 4, 5,
2, 3, 3, 4, 3, 4, 4, 5, 3, 4, 4, 5, 4, 5, 5, 6, 2, 3, 3, 4, 3, 4, 4, 5, 3, 4, 4, 5, 4, 5, 5, 6, 3, 4, 4, 5, 4, 5, 5, 6,
4, 5, 5, 6, 5, 6, 6, 7, 1, 2, 2, 3, 2, 3, 3, 4, 2, 3, 3, 4, 3, 4, 4, 5, 2, 3, 3, 4, 3, 4, 4, 5, 3, 4, 4, 5, 4, 5, 5, 6,
2, 3, 3, 4, 3, 4, 4, 5, 3, 4, 4, 5, 4, 5, 5, 6, 3, 4, 4, 5, 4, 5, 5, 6, 4, 5, 5, 6, 5, 6, 6, 7, 2, 3, 3, 4, 3, 4, 4, 5,
3, 4, 4, 5, 4, 5, 5, 6, 3, 4, 4, 5, 4, 5, 5, 6, 4, 5, 5, 6, 5, 6, 6, 7, 3, 4, 4, 5, 4, 5, 5, 6, 4, 5, 5, 6, 5, 6, 6, 7,
4, 5, 5, 6, 5, 6, 6, 7, 5, 6, 6, 7, 6, 7, 7, 8
};

Bitmap::Bitmap(size_t number_of_bits) :
        size_(number_of_bits),
        num_bits_set_(0)
{
  bitmap_ = new uint8[BITMAP_BYTE_COUNT(number_of_bits)]{};
}

Bitmap::Bitmap(const Bitmap &bm)
  : size_(bm.size_)
  , num_bits_set_(bm.num_bits_set_)
{
  const size_t bytes = BITMAP_BYTE_COUNT(size_);
  bitmap_ = new uint8[bytes]{};
  memcpy(bitmap_, bm.bitmap_, bytes);
}

Bitmap::~Bitmap()
{
  delete[] bitmap_;
}

#define BYTE (b[bit_number / bits_per_bitmap_atom_])
#define MASK (1 << (bit_number % bits_per_bitmap_atom_))

bool Bitmap::setBit(size_t bit_number)
{
  assert(bit_number < size_);
  return setBit(bitmap_, num_bits_set_, bit_number);
}

bool Bitmap::setBit(uint8* b, size_t& num_bits_set, size_t bit_number)
{
  //kprintfd("bitmap %p, %zu, %zu\n",b,num_bits_set, bit_number);
  if (!(BYTE & MASK))
  {
    BYTE |= MASK;
    ++num_bits_set;
    return true;
  }
  return false;
}

bool Bitmap::getBit(size_t bit_number)
{
  assert(bit_number < size_);
  return getBit(bitmap_, bit_number);
}

bool Bitmap::getBit(uint8* b, size_t bit_number)
{
  return BYTE & MASK;
}

bool Bitmap::unsetBit(size_t bit_number)
{
  assert(bit_number < size_);
  return unsetBit(bitmap_, num_bits_set_, bit_number);
}

bool Bitmap::unsetBit(uint8* b, size_t& num_bits_set, size_t bit_number)
{
  if (BYTE & MASK)
  {
    BYTE &= ~MASK;
    --num_bits_set;
    return true;
  }
  return false;
}

void Bitmap::setByte(size_t byte_number, uint8 byte)
{
  assert(byte_number * bits_per_bitmap_atom_ < size_);
  uint8& b = bitmap_[byte_number];

  num_bits_set_ -= BIT_COUNT[b];
  num_bits_set_ += BIT_COUNT[byte];
  b = byte;
}

uint8 Bitmap::getByte(size_t byte_number)
{
  assert(byte_number * bits_per_bitmap_atom_ < size_);
  return bitmap_[byte_number];
}

void Bitmap::bmprint()
{
  bmprint(bitmap_, size_, num_bits_set_);
}

void Bitmap::bmprint(uint8* b, size_t n, size_t num_bits_set)
{
  kprintfd("\n---------------------Bitmap: size=%zd, num_bits_set=%zd---------------------\n"
      "       0x0      0x8      0x10     0x18     0x20     0x28     0x30     0x38\n", n, num_bits_set);
  for (size_t i = 0; i < n; i++)
  {
    if (i % 64 == 0)
      kprintfd("%05zx| ",i);
    kprintfd("%d", getBit(b, i));
    if (i % 8 == 7)
      kprintfd(" ");
    if (i % 64 == 63)
      kprintfd("\n");
  }
  kprintfd("\n----------------------------------Bitmap:end----------------------------------\n");
}

size_t Bitmap::getSize()
{
  return size_;
}

size_t Bitmap::getNumBitsSet()
{
  return num_bits_set_;
}

size_t Bitmap::getNumFreeBits()
{
  return size_ - num_bits_set_;
}
