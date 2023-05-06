#include "com_thekidofarcrania_heap_JHeap.h"
#include <err.h>
#include <iconv.h>
#include <stdio.h>
#include <stdlib.h>
#include <wchar.h>
#include <unistd.h>

#ifdef DEBUG
#define debugf(...) printf(__VA_ARGS__)
#else
#define debugf(...)
#endif

size_t from_utf(char *in, size_t inlen, jchar *out, size_t outlen) {
  size_t outleft = outlen;

  iconv_t cd = iconv_open("unicodelittle", "utf-8");
  if (iconv(cd, &in, &inlen, (char**)&out, &outleft) == (size_t) -1)
    err(1, "iconv() failed");

  return outlen - outleft;
}


JNIEXPORT jlong JNICALL Java_com_thekidofarcrania_heap_JHeap_addrOf
  (JNIEnv *env, jclass cls, jobject target) {
#ifdef DEBUG
    return *(jlong*)target;
#else
    return 0;
#endif
}

// Must have env and cls defined!
#define GetID(type, out, cls, name, signature) _GetID(Get ## type ## ID, out, cls, name, signature)
#define _GetID(fn, out, cls, name, signature) do { \
  (out) = (*env)->fn(env, (cls), (name), (signature)); \
  if (!(out)) errx(1, #fn "() failed!"); \
} while(0)
JNIEXPORT void JNICALL Java_com_thekidofarcrania_heap_JHeap_editThis
  (JNIEnv * env, jobject obj, jint x) {
  jclass cls = (*env)->GetObjectClass(env, obj);
  jmethodID mth_utf8len;
  jfieldID fld_data;
  jint datalen, readlen, offset;
  jchar *data;
  char *tmp;
  char numbuff[10];
  jboolean copied;
  jstring tmp2;

  GetID(Field, fld_data, cls, "data", "[C");
  GetID(Method, mth_utf8len, cls, "utf8Length", "()I");

  jarray arr_data = (jarray)(*env)->GetObjectField(env, obj, fld_data);
  if (!arr_data) errx(1, "Null array!");

  datalen = (*env)->CallIntMethod(env, obj, mth_utf8len);
  if (datalen < 0)
    errx(1, "negative size");

  // Read offset
  printf("Offset: ");
  fflush(stdout);
  readlen = read(0, numbuff, sizeof(numbuff) - 1);
  if (readlen <= 0)
    err(1, "read() failed");
  numbuff[readlen - 1] = 0;
  offset = atoi(numbuff);
  if (offset >= datalen || offset < 0)
    errx(1, "invalid offset");
  datalen -= offset; 
  
  tmp = malloc(datalen);
  if (!tmp)
    errx(1, "malloc() failed");


  printf("Content: ");
  fflush(stdout);
  readlen = read(0, tmp, datalen);
  if (readlen <= 0)
    err(1, "read() failed");

  data = (*env)->GetPrimitiveArrayCritical(env, arr_data, &copied);

  if (copied) errx(1, "Error! This was copied!");
  from_utf(tmp, readlen, data + offset * 2, readlen * 2 + 2);
  free(tmp);
  (*env)->ReleasePrimitiveArrayCritical(env, arr_data, data, 0);
}
