#include "String8.h"
#include "KeyedVector.h"
#include <byteswap.h>
#include <sys/types.h>

#define DATA_LENGTH 0x10000

enum
{
    TYPE_TITLE = 'tlte',
    TYPE_DATE = 'date',
    TYPE_TIME = 'time',
    TYPE_SINGER = 'sgnr',
    TYPE_ALBUM = 'abum',
    TYPE_FEATURING = 'feat'
} tagTypes;

namespace android
{

    class DataIterator
    {
    public:
        DataIterator();
        ~DataIterator();

        bool startTag(uint8_t *data);
        bool endTag(uint8_t *data);
        bool getTitleTag(uint8_t *data, String8 *name);
        bool getAlbumTag(uint8_t *data, String8 *album);
        bool getTimeTag(uint8_t *data, int64_t *time);
        bool getDateTag(uint8_t *data, int64_t *date);
        bool getSingerTag(uint8_t *data, String8 *singer);
        bool getFeaturingTag(uint8_t *data, String8 *featuring);
        void skipDateTag();
        void skipTimeTag();
        virtual void next();

    private:
        uint64_t mOffset;
        uint64_t mFrameSize;
        bool dateAvailable;
        bool timeAvailable;
    };

    class DataPrinter
    {
    public:
        DataPrinter();
        ~DataPrinter();
        virtual void printTag(const char *token, const char *data);
        virtual void printTag(const char *token, int64_t data);
    };

    class MetaData
    {
    public:
        enum Type
        {
            TYPE_C_STRING = 'cstr',
            TYPE_INT32 = 'in32',
            TYPE_INT64 = 'in64'
        };

        MetaData();
        ~MetaData();

        void clear();
        bool remove(uint64_t key);

        bool setCString(uint64_t key, const char *value);
        bool setInt32(uint64_t key, int32_t value);
        bool setInt64(uint64_t key, int64_t value);
        bool findCString(uint64_t key, const char **value) const;
        bool findInt32(uint64_t key, int32_t *value) const;
        bool findInt64(uint64_t key, int64_t *value) const;
        bool setData(uint64_t key, uint64_t type, const void *data, size_t size);
        bool findData(uint64_t key, uint64_t *type, const void **data, size_t *size) const;

    private:
        struct MetaDataInternal;
        struct typed_data;
        MetaDataInternal *mInternalData;
    };

}