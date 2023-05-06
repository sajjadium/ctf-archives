#include "Song.h"
#include <iostream>
#include <signal.h>
#include <unistd.h>

namespace android
{

    struct MetaData::typed_data
    {
    public:
        typed_data();
        ~typed_data();
        typed_data(const MetaData::typed_data &);
        typed_data &operator=(const MetaData::typed_data &);

        void clear();
        void setData(uint64_t type, const void *data, size_t size);
        void getData(uint64_t *type, const void **data, size_t *size) const;

    private:
        uint64_t mType;
        size_t mSize;

        union
        {
            void *data;
            float reservior;
        } u;

        void *allocateStorage(size_t size);
        void freeStorage();

        bool useReservior() const
        {
            return mSize <= sizeof(u.reservior);
        }

        void *storage()
        {
            return useReservior() ? &u.reservior : u.data;
        }

        const void *storage() const
        {
            return useReservior() ? &u.reservior : u.data;
        }
    };

    struct MetaData::MetaDataInternal
    {
        KeyedVector<uint64_t, MetaData::typed_data> mItems;
    };

    MetaData::typed_data::typed_data()
        : mSize(0),
          mType(0)
    {
    }

    MetaData::typed_data::~typed_data()
    {
        clear();
    }

    MetaData::typed_data::typed_data(const typed_data &from)
        : mType(from.mType),
          mSize(0)
    {

        void *dst = allocateStorage(from.mSize);
        if (dst)
        {
            memcpy(dst, from.storage(), mSize);
        }
    }

    MetaData::typed_data &MetaData::typed_data::operator=(
        const MetaData::typed_data &from)
    {
        if (this != &from)
        {
            clear();
            mType = from.mType;
            void *dst = allocateStorage(from.mSize);
            if (dst)
            {
                memcpy(dst, from.storage(), mSize);
            }
        }

        return *this;
    }

    void MetaData::typed_data::clear()
    {
        freeStorage();

        mType = 0;
    }

    bool MetaData::setData(uint64_t key, uint64_t type, const void *data, size_t size)
    {
        bool overwriting_existing = true;
        int64_t i = mInternalData->mItems.indexOfKey(key);
        if (i < 0)
        {
            typed_data item; // HMM??
            i = mInternalData->mItems.add(key, item);
            overwriting_existing = false;
        }

        typed_data &item = mInternalData->mItems.editValueAt(i);
        item.setData(type, data, size);

        return overwriting_existing;
    }

    bool MetaData::findData(uint64_t key, uint64_t *type, const void **data, size_t *size) const
    {
        ssize_t i = mInternalData->mItems.indexOfKey(key);

        if (i < 0)
            return false;

        const typed_data &item = mInternalData->mItems.valueAt(i);
        item.getData(type, data, size);

        return true;
    }

    bool MetaData::setCString(uint64_t key, const char *value)
    {
        return setData(key, TYPE_C_STRING, value, strlen(value) + 1);
    }

    bool MetaData::setInt32(uint64_t key, int32_t value)
    {
        return setData(key, TYPE_INT32, &value, sizeof(value));
    }

    bool MetaData::setInt64(uint64_t key, int64_t value)
    {
        return setData(key, TYPE_INT64, &value, sizeof(value));
    }

    bool MetaData::findCString(uint64_t key, const char **value) const
    {
        uint64_t type;
        const void *data;
        size_t size;
        if (!findData(key, &type, &data, &size) || type != TYPE_C_STRING)
        {
            return false;
        }

        *value = (const char *)data;
        return true;
    }

    bool MetaData::findInt64(uint64_t key, int64_t *value) const
    {
        uint64_t type;
        const void *data;
        size_t size;
        if (!findData(key, &type, &data, &size) || type != TYPE_INT64)
        {
            return false;
        }

        *value = *(int64_t *)data;
        return true;
    }

    void MetaData::typed_data::setData(uint64_t type, const void *data, size_t size)
    {
        clear();
        mType = type;

        void *dst = allocateStorage(size);
        if (dst)
        {
            memcpy(dst, data, size);
        }
    }

    void MetaData::typed_data::getData(uint64_t *type, const void **data, size_t *size) const
    {
        *type = mType;
        *size = mSize;
        *data = storage();
    }

    void *MetaData::typed_data::allocateStorage(size_t size)
    {
        mSize = size;

        if (useReservior())
        {
            return &u.reservior;
        }

        u.data = malloc(mSize);
        if (!u.data)
            exit(0);

        return u.data;
    }

    void MetaData::typed_data::freeStorage()
    {
        if (!useReservior())
        {
            if (u.data)
            {
                free(u.data);
                u.data = NULL;
            }
        }

        mSize = 0;
    }

    MetaData::MetaData()
        : mInternalData(new MetaDataInternal())
    {
    }

    MetaData::~MetaData()
    {
        clear();
        delete mInternalData;
    }

    void MetaData::clear()
    {
        mInternalData->mItems.clear();
    }

    DataIterator::DataIterator()
        : mOffset(0),
          mFrameSize(0),
          dateAvailable(false),
          timeAvailable(false)
    {
    }

    bool DataIterator::startTag(uint8_t *data)
    {
        mFrameSize = 5;
        if (memcmp(&data[mOffset], "<TAG>", mFrameSize))
            return false;
        next();
        return true;
    }

    bool DataIterator::endTag(uint8_t *data)
    {
        if (memcmp(&data[mOffset], "</TAG>", 6))
            return false;

        mOffset = 0;
        mFrameSize = 0;
        return true;
    }

    bool DataIterator::getTitleTag(uint8_t *data, String8 *name)
    {
        size_t n = 0;
        mFrameSize = 7;
        if (memcmp(&data[mOffset], "<TITLE>", mFrameSize))
            return false;
        next();

        n = (data[mOffset + 1] << 8) + data[mOffset];
        mFrameSize = 2;
        next();

        uint8_t encoding = data[mOffset];
        const uint8_t *frameData = &data[mOffset];
        if (encoding == 0x00)
        {
            name->setTo((const char *)frameData + 1, n);
        }
        else if (encoding == 0x03)
        {
            name->setTo((const char *)(frameData + 1), n);
        }
        else if (encoding == 0x02)
        {
            int len = n / 2;
            const char16_t *framedata = (const char16_t *)(frameData + 1);
            char16_t *framedatacopy = NULL;
            if (len > 0)
            {
                framedatacopy = new (std::nothrow) char16_t[len];
                if (framedatacopy == NULL)
                {
                    return false;
                }
                for (int i = 0; i < len; i++)
                {
                    framedatacopy[i] = bswap_16(framedata[i]);
                }
                framedata = framedatacopy;
            }
            name->setTo(framedata, len);
            if (framedatacopy != NULL)
            {
                delete[] framedatacopy;
            }
        }
        else
            false;

        mFrameSize = 1 + n;
        next();

        mFrameSize = 8;
        if (memcmp(&data[mOffset], "</TITLE>", mFrameSize))
            return false;
        next();

        return true;
    }

    bool DataIterator::getTimeTag(uint8_t *data, int64_t *time)
    {
        timeAvailable = true;
        mFrameSize = 6;
        if (memcmp(&data[mOffset], "<TIME>", mFrameSize))
            return false;
        next();

        *time = data[mOffset];
        mFrameSize = 1;
        next();

        mFrameSize = 7;
        if (memcmp(&data[mOffset], "</TIME>", mFrameSize))
            return false;
        next();

        return true;
    }

    bool DataIterator::getDateTag(uint8_t *data, int64_t *date)
    {
        dateAvailable = true;
        mFrameSize = 6;
        if (memcmp(&data[mOffset], "<DATE>", mFrameSize))
            return false;
        next();

        *date = (data[mOffset + 1] << 8) + data[mOffset];
        mFrameSize = 2;
        next();

        mFrameSize = 7;
        if (memcmp(&data[mOffset], "</DATE>", mFrameSize))
            return false;
        next();

        return true;
    }

    bool DataIterator::getSingerTag(uint8_t *data, String8 *singer)
    {
        size_t n = 0;
        mFrameSize = 8;
        if (memcmp(&data[mOffset], "<SINGER>", mFrameSize))
            return false;
        next();

        n = (data[mOffset + 1] << 8) + data[mOffset];
        mFrameSize = 2;
        next();

        uint8_t encoding = data[mOffset];
        const uint8_t *frameData = &data[mOffset];
        if (encoding == 0x00)
        {
            singer->setTo((const char *)frameData + 1, n);
        }
        else if (encoding == 0x03)
        {
            singer->setTo((const char *)(frameData + 1), n);
        }
        else if (encoding == 0x02)
        {
            int len = n / 2;
            const char16_t *framedata = (const char16_t *)(frameData + 1);
            char16_t *framedatacopy = NULL;
            if (len > 0)
            {
                framedatacopy = new (std::nothrow) char16_t[len];
                if (framedatacopy == NULL)
                {
                    return false;
                }
                for (int i = 0; i < len; i++)
                {
                    framedatacopy[i] = bswap_16(framedata[i]);
                }
                framedata = framedatacopy;
            }
            singer->setTo(framedata, len);
            if (framedatacopy != NULL)
            {
                delete[] framedatacopy;
            }
        }
        else
            false;

        mFrameSize = 1 + n;
        next();

        mFrameSize = 9;
        if (memcmp(&data[mOffset], "</SINGER>", mFrameSize))
            return false;
        next();

        return true;
    }

    bool DataIterator::getAlbumTag(uint8_t *data, String8 *album)
    {
        size_t n = 0;
        mFrameSize = 7;
        if (memcmp(&data[mOffset], "<ALBUM>", mFrameSize))
            return false;
        next();

        n = (data[mOffset + 1] << 8) + data[mOffset];
        mFrameSize = 2;
        next();

        uint8_t encoding = data[mOffset];
        const uint8_t *frameData = &data[mOffset];
        if (encoding == 0x00)
        {
            album->setTo((const char *)frameData + 1, n);
        }
        else if (encoding == 0x03)
        {
            album->setTo((const char *)(frameData + 1), n);
        }
        else if (encoding == 0x02)
        {
            int len = n / 2;
            const char16_t *framedata = (const char16_t *)(frameData + 1);
            char16_t *framedatacopy = NULL;
            if (len > 0)
            {
                framedatacopy = new (std::nothrow) char16_t[len];
                if (framedatacopy == NULL)
                {
                    return false;
                }
                for (int i = 0; i < len; i++)
                {
                    framedatacopy[i] = bswap_16(framedata[i]);
                }
                framedata = framedatacopy;
            }
            album->setTo(framedata, len);
            if (framedatacopy != NULL)
            {
                delete[] framedatacopy;
            }
        }
        else
            false;

        mFrameSize = 1 + n;
        next();

        mFrameSize = 8;
        if (memcmp(&data[mOffset], "</ALBUM>", mFrameSize))
            return false;
        next();

        return true;
    }

    bool DataIterator::getFeaturingTag(uint8_t *data, String8 *featuring)
    {
        size_t n = 0;
        mFrameSize = 11;
        if (memcmp(&data[mOffset], "<FEATURING>", mFrameSize))
            return false;
        next();

        n = (data[mOffset + 1] << 8) + data[mOffset];
        mFrameSize = 2;
        next();

        uint8_t encoding = data[mOffset];
        const uint8_t *frameData = &data[mOffset];
        if (encoding == 0x00)
        {
            featuring->setTo((const char *)frameData + 1, n);
        }
        else if (encoding == 0x03)
        {
            featuring->setTo((const char *)(frameData + 1), n);
        }
        else if (encoding == 0x02)
        {
            int len = n / 2;
            const char16_t *framedata = (const char16_t *)(frameData + 1);
            char16_t *framedatacopy = NULL;
            if (len > 0)
            {
                framedatacopy = new (std::nothrow) char16_t[len];
                if (framedatacopy == NULL)
                {
                    return false;
                }
                for (int i = 0; i < len; i++)
                {
                    framedatacopy[i] = bswap_16(framedata[i]);
                }
                framedata = framedatacopy;
            }
            featuring->setTo(framedata, len);
            if (framedatacopy != NULL)
            {
                delete[] framedatacopy;
            }
        }
        else
            false;

        mFrameSize = 1 + n;
        next();

        mFrameSize = 12;
        if (memcmp(&data[mOffset], "</FEATURING>", mFrameSize))
            return false;
        next();

        return true;
    }

    void DataIterator::next()
    {
        mOffset += mFrameSize;
    }

    void DataIterator::skipDateTag()
    {
        dateAvailable = false;
    }

    void DataIterator::skipTimeTag()
    {
        timeAvailable = false;
    }

    DataPrinter::DataPrinter() {}

    DataPrinter::~DataPrinter() {}

    void DataPrinter::printTag(const char *token, const char *data)
    {
        std::cout << token << data << std::endl;
    }

    void DataPrinter::printTag(const char *token, int64_t data)
    {
        std::cout << token << data << std::endl;
    }

}

using namespace android;

void myalarm(int signo)
{
    exit(0);
}

int main()
{
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    signal(SIGALRM, myalarm);
    alarm(30);

    uint8_t data[DATA_LENGTH + 1];
    DataIterator *it = new DataIterator();
    DataPrinter *dp;
    const char *title_data;
    const char *singer_data;
    const char *album_data;
    const char *featuring_data;

    int64_t date, time;
    int64_t date_data, time_data;
    MetaData *meta = new MetaData();
    String8 title;
    String8 album;
    String8 singer;
    String8 featuring;

    std::cout << "[ Add your favorite song ]" << std::endl;

    while (1)
    {
        memset(data, 0, DATA_LENGTH);
        std::cin.read(reinterpret_cast<char *>(data), DATA_LENGTH);

        if (!it->startTag(data))
            return 0;

        while (1)
        {
            if (!it->getTitleTag(data, &title))
                return 0;
            meta->setCString(TYPE_TITLE, title.string());

            if (!it->getSingerTag(data, &singer))
                return 0;
            meta->setCString(TYPE_SINGER, singer.string());

            if (!it->getAlbumTag(data, &album))
                return 0;
            meta->setCString(TYPE_ALBUM, album.string());

            if (!it->getDateTag(data, &date))
                it->skipDateTag();
            else
                meta->setInt64(TYPE_DATE, date);

            if (!it->getTimeTag(data, &time))
                it->skipTimeTag();
            else
                meta->setInt64(TYPE_TIME, time);

            if (!it->getFeaturingTag(data, &featuring))
                return 0;
            meta->setCString(TYPE_FEATURING, featuring.string());

            if (!dp)
                dp = new DataPrinter();

            if (meta->findCString(TYPE_TITLE, &title_data))
                dp->printTag("title: ", title_data);

            if (meta->findCString(TYPE_SINGER, &singer_data))
                dp->printTag("singer: ", singer_data);

            if (meta->findCString(TYPE_ALBUM, &album_data))
                dp->printTag("album: ", album_data);

            if (meta->findInt64(TYPE_DATE, &date_data))
                dp->printTag("date: ", date_data);

            if (meta->findInt64(TYPE_TIME, &time_data))
                dp->printTag("time: ", time_data);

            if (meta->findCString(TYPE_FEATURING, &featuring_data))
                dp->printTag("featuring: ", featuring_data);

            if (it->endTag(data))
                break;
            else
                return 0;
        }
    }

    return 0;
}