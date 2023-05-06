/*
 * Implementation Basic of Array, Dictionary String
 */

#ifndef IOOBJECTS_H
#include <cstdint>
#include <cstdlib>
#include <sys/types.h>
#include "libzone.h"
#include <memory>
#include <optional>
#include <cstring>
#include <assert.h>

#define zmake_shared(Type, ...) shared_ptr<Type>(new Type(__VA_ARGS__))

#define ZONE_REGISTER(object_name) \
	struct zone_init ## object_name { \
		const char *zone_name;\
		zone_init ## object_name() { \
			zone_name = #object_name; \
			zone_create(zone_name, sizeof(object_name)); \
		} \
	}; \
	static zone_init ## object_name init_ ## object_name; \

// IO Object Types
#define OBJECT 			0
#define STRING 			1
#define BYTES  			2
#define LIST   			3
#define DICT   			4
#define SYMBOL 			5
#define SERVICE 		6
#define EVENT 			7
#define SERVICE_MANAGER 8
// ---------------

#define OPERATOR_NEW_DELETE_DELC \
	void* operator new(size_t size);\
	void operator delete(void *ptr);

#define OPERATOR_NEW_DELETE_IMPLEMENTATION_DECL(CPP_OBJECT_NAME) \
	void* CPP_OBJECT_NAME::operator new(size_t size) {\
		return zone_alloc(init_ ## CPP_OBJECT_NAME.zone_name); \
	} \
	void CPP_OBJECT_NAME::operator delete(void *ptr) {\
		zone_free(init_ ## CPP_OBJECT_NAME.zone_name, ptr);\
	}

#define ARRAY_TEMPLATE_COPY_INDEX_DELC(BaseClass, Class, Type) \
	Class& operator=(const Class& that) { \
		BaseClass<Type>::operator=(that); \
		return *this; \
	}\
	Class& operator+(const Class& that) { \
		BaseClass<Type>::operator+(that); \
		return *this; \
	}\
	Class& operator+=(const Class& that) { \
		BaseClass<Type>::operator+=(that); \
		return *this; \
	}\
	Type& operator[](size_t idx) {\
		return BaseClass<Type>::operator[](idx);\
	}

#define ARRAY_TEMPLATE_OPERATOR_COMPARES_DELC(BaseClass) \
	bool operator==(BaseClass& other) { \
		return compare(other) == 0;\
	} \
	bool operator!=(BaseClass& other){\
		return compare(other) != 0;\
	}\
	bool operator>(BaseClass& other){\
		return compare(other) > 0;\
	}\
	bool operator<(BaseClass& other){\
		return compare(other) < 0;\
	}\
	bool operator>=(BaseClass& other){\
		return compare(other) >= 0;\
	}\
	bool operator<=(BaseClass& other){\
		return compare(other) <= 0;\
	}

class IOBytes;
class IOString;
class IOSymbol;
class IOList;
class IODict;

class IOObject {
private:
	int type;
	// IOObject interface
protected:
	virtual void set_type(int type) {
		this->type = type;
	}

public:
	IOObject(int obj_type): type(obj_type) {};
	IOObject(): type(OBJECT) {};

	IOObject& operator=(IOObject& other) {
		type = other.type;
		return *this;
	}

	virtual int get_type(void){
		return type;
	};

	virtual std::optional<std::unique_ptr<IOString>> view_object(void);
};

#define DEFAULT_SIZE 64

static inline size_t round_up(size_t size, size_t base)
{
	return size % base == 0 ? size : base + (size / base) * base;
}

template <typename T>
class ArrayTemplate {
private:
	T  inlinearray[DEFAULT_SIZE];
	T* array;
	size_t size;

protected:
	size_t count;

	const T* get_raw_array(void) {
		return (const T*)array;
	}

	void ensure(size_t needed_size) {
		size_t realloc_size = 0;
		T* new_array = NULL;
		// automatically realloc buffer if count > size
		if(count + needed_size > size){
			realloc_size = round_up(count + needed_size, size);

			new_array = (T *)zcalloc(realloc_size, sizeof(T));
			assert(new_array != NULL); // make sure new array is not NULL
			// copy old array to new array
			memcpy((void *)new_array, (void *)array, sizeof(T) * count);

			if((size_t)array != (size_t)inlinearray){
				zfree(array, size * sizeof(T));
			}

			size = realloc_size;
			array = new_array;
		}
	}

public:
	ArrayTemplate() {
		array = (T *)&inlinearray;
		count = 0;
		size = DEFAULT_SIZE;
	}

	ArrayTemplate(size_t init_size) {
		if (init_size > DEFAULT_SIZE) {
			size = round_up(init_size, DEFAULT_SIZE);
			array = (T *)zcalloc(size, sizeof(T));
		} else {
			size = DEFAULT_SIZE;
			array = (T *)&inlinearray;
		}
		count = 0;
	};

	ArrayTemplate& operator=(const ArrayTemplate& other) {
		if(!other.count)
			return *this;
		// copy all array in other to this.array
		ensure(other.count);

		for(size_t i = 0; i < other.count; i++) {
			array[i] = other.array[i];
		}

		size = other.size;
		count = other.count;
		return *this;
	};

	T& operator[](uint32_t idx) {
		assert(idx < count);
		return array[idx];
	}

	T& get_at(uint32_t idx) {
		assert(idx < count);
		return array[idx];
	}

	ArrayTemplate& operator+(const ArrayTemplate& t_other) {
		expand(t_other);
		return *this;
	}

	ArrayTemplate& operator+=(const ArrayTemplate& that) {
		expand(that);
		return *this;
	}

	virtual int compare(const ArrayTemplate<T>& that) = 0;

	ARRAY_TEMPLATE_OPERATOR_COMPARES_DELC(ArrayTemplate)

	virtual void expand(const ArrayTemplate& t_other){
		ensure(t_other.count);

		for(size_t i = count; i < t_other.count; i++){
			array[i] = t_other.array[i];
		}

		count += t_other.count;
	}

	virtual void append(const T& t_object) {
		// append to end of list
		ensure(1);
		array[count++] = t_object;
	}

	const size_t get_max_size(void) {
		return size;
	}

	const size_t get_size(void) {
		return count;
	}

	void remove_at(size_t idx) {
		assert(idx < count);
		array[idx] = 0; // release this item

		for(size_t i = idx; i < count - 1; i++) {
			array[i] = array[i + 1];
		}

		count--;
	}

	std::optional<T&> pop() {
		if(get_size() == 0)
			return {};

		// pop last item from this list
		T last_item = array[count - 1];
		array[count - 1] = 0;
		count--;
		return {last_item};
	}

	void clear(void) {
		// clear the array
		for(size_t i = 0 ; i < count; i++){
			array[i] = 0;
		}

		if((size_t)array != (size_t)inlinearray){
			// free dynamic buffer
			zfree(array, size * sizeof(T));
		}

		// reset all attributes
		array = (T *)&inlinearray;
		count = 0;
		size = DEFAULT_SIZE;
	}

	~ArrayTemplate() {
		clear();
	}
};

class IOBytes: public ArrayTemplate<uint8_t>, public IOObject {
public:
	IOBytes(): ArrayTemplate(), IOObject(BYTES) {};
	IOBytes(const char *buffer, size_t buffer_size);
	IOBytes(size_t alloc_size): ArrayTemplate(alloc_size) { set_type(BYTES); };

	virtual void expand(const char* buffer, size_t buffer_size);

	// overwrite compare method
	int compare(const ArrayTemplate<uint8_t>& that) override;
	virtual int compare(const IOBytes& that) {
		// overload ArrayTemplate to use IOBytes
		return compare(static_cast<const ArrayTemplate<uint8_t>&>(that));
	}

	const unsigned char *get_raw_ptr(void);
	void fill_buffer(size_t size);

	// automatically override operator=/operator+ of ArrayTemplate
	ARRAY_TEMPLATE_COPY_INDEX_DELC(ArrayTemplate, IOBytes, uint8_t)

	ARRAY_TEMPLATE_OPERATOR_COMPARES_DELC(IOBytes)

	OPERATOR_NEW_DELETE_DELC
};

class IOString: public IOBytes {
public:
	IOString(): IOBytes() {set_type(STRING);};
	IOString(const char *str): IOString() { set_str(str); };

	void expand(const char *str);
	void set_str(const char *str);

	std::unique_ptr<IOSymbol> to_symbol(void);
	const char* to_cstr();

	const size_t get_length(void);
	uint32_t parse_uint32(void);

	ARRAY_TEMPLATE_COPY_INDEX_DELC(ArrayTemplate, IOString, uint8_t)
	OPERATOR_NEW_DELETE_DELC

};

class IOSymbol: public IOString {
public:
	IOSymbol(): IOString() {set_type(SYMBOL);};
	IOSymbol(const char *str);
	IOSymbol(IOString& iostr);

	std::unique_ptr<IOString> to_iostr(void);

	ARRAY_TEMPLATE_OPERATOR_COMPARES_DELC(IOSymbol)
	ARRAY_TEMPLATE_COPY_INDEX_DELC(ArrayTemplate, IOSymbol, uint8_t)

	OPERATOR_NEW_DELETE_DELC
};

class IOList: public ArrayTemplate<std::shared_ptr<IOObject>>, public IOObject {
public:
	IOList(): ArrayTemplate(), IOObject(LIST) {};

	int compare(const ArrayTemplate<std::shared_ptr<IOObject>>& that) override;

	ARRAY_TEMPLATE_COPY_INDEX_DELC(ArrayTemplate, IOList, std::shared_ptr<IOObject>)
	OPERATOR_NEW_DELETE_DELC
};

#define DEFAULT_TABLE_SIZE 128

template <typename K>
struct Entry {
	K key;
	size_t value_idx;
};

template <typename K, typename V>
class DictTemplate {
private:
#define ENTRY_DEAD (~0)
	struct Entry<K> inline_entries[DEFAULT_TABLE_SIZE];
	V inline_values[DEFAULT_TABLE_SIZE];
	size_t count;
	size_t table_size;

#define IS_INLINE_PTR(ptr, inline_buffer) ((size_t)ptr == (size_t)&inline_buffer ? true : false)

protected:
	// make these pointers accessible from child class
	struct Entry<K>* entries_ptr;
	V* values_ptr;

	void ensure(size_t needed_size) {
		V *new_values;
		struct Entry<K> *new_entries;
		size_t realloc_size = 0;

		if(count + needed_size > table_size) {
			realloc_size = round_up(count + needed_size, table_size);

			new_values = (V *)zcalloc(realloc_size, sizeof(V));
			assert(new_values != NULL);
			new_entries = (struct Entry<K> *)zcalloc(realloc_size, sizeof(struct Entry<K>));
			assert(new_entries != NULL);

			memcpy((void *)new_values, (void *)values_ptr, count * sizeof(std::shared_ptr<V>));
			memcpy((void *)new_entries, (void *)entries_ptr, count * sizeof(struct Entry<K>));

			if(!IS_INLINE_PTR(values_ptr, inline_values)){
				zfree(values_ptr, table_size * sizeof(std::shared_ptr<V>));
				zfree(entries_ptr, table_size * sizeof(struct Entry<K>));
			}

			values_ptr = new_values;
			entries_ptr = new_entries;
			count += needed_size;
			table_size = realloc_size;
		}
	}

	// interface method  need to be implmented in derived class
	virtual void sort(void) = 0;
	virtual struct Entry<K>* search(const K& key) = 0;

public:
	DictTemplate() {
		count = 0;
		table_size = DEFAULT_TABLE_SIZE;
		values_ptr = (V *)&inline_values;
		entries_ptr = (struct Entry<K> *)&inline_entries;
	}

	~DictTemplate() {
		clear();
	}

	void update(const DictTemplate& other) {
		//expand this dictionary
		ensure(other.count);

		for(size_t i = count; i < other.count; i++){
			values_ptr[i] = other.values_ptr[i - count];
			entries_ptr[i] = other.entries_ptr[i - count];
			// update new value_idx
			entries_ptr[i].value_idx += count;
		}

		count+= other.count;

	}

	void add(const K& key, const V& value) {
		struct Entry<K> *exist_key;

		exist_key = search(key);
		if(exist_key){
			// update value only
			assert(exist_key->value_idx != ENTRY_DEAD);
			values_ptr[exist_key->value_idx] = value;
		} else {
			// add new key/value to dictionary
			ensure(1);

			values_ptr[count] = value;
			entries_ptr[count].key = key;
			entries_ptr[count].value_idx = count;
			count++;

			if(count > 1)
				sort(); // sort the entries list if size of this array larger than 1
		}
	}

	void remove(const K& key){
		struct Entry<K> *entryp;
		size_t value_idx;

		entryp = search(key);
		if(!entryp)
			return; // item does not found

		// found item with key, delete it
		size_t entry_idx = ((size_t)entryp - (size_t)entries_ptr) / sizeof(struct Entry<K>);
		value_idx = entryp->value_idx;

		assert(value_idx != ENTRY_DEAD);

		// delete value first
		values_ptr[value_idx] = 0; // clear value in Dictionary
		for(size_t i = value_idx; i < count - 1; i++){
			values_ptr[i] = values_ptr[i + 1];
		}

		// delete key
		entryp->key = 0; // clear key in Dictionary
		entryp->value_idx = ENTRY_DEAD;
		for(size_t i = entry_idx; i < count - 1; i++){
			entries_ptr[i] = entries_ptr[i + 1];
		}

		count--;
	}

	void clear(void){
		// delete all keys/ values in Dictionary
		for(size_t i = 0; i < count; i++){
			entries_ptr[i].key = 0;
			entries_ptr[i].value_idx = ENTRY_DEAD;
			values_ptr[i] = 0;
		}

		if(!IS_INLINE_PTR(entries_ptr, inline_entries)){
			zfree(entries_ptr, sizeof(struct Entry<K>) * table_size);
			zfree(values_ptr, sizeof(V) * table_size);
		}

		entries_ptr = (struct Entry<K> *)&inline_entries;
		values_ptr = (V *)&inline_values;
		count = 0;
		table_size = DEFAULT_TABLE_SIZE;
	}

	const size_t get_size() {
		return count;
	};

	const size_t get_max_size() {
		return table_size;
	};

};

class IODict: public DictTemplate<std::shared_ptr<IOSymbol>, std::shared_ptr<IOObject>>, public IOObject
{
protected:
	struct Entry<std::shared_ptr<IOSymbol>>* search(const std::shared_ptr<IOSymbol>& key) override; // override DictTemplate::search
	void sort(void) override; //override DictTemplate::sort

public:
	IODict(): DictTemplate(), IOObject(DICT) {}

	IODict& operator=(const IODict& that){
		clear(); // clear exist entries
		update(that); // copy entries from that dictionary
		return *this;
	}

	IODict& operator+(const IODict& that){
		// extend Dictionary
		update(that);
		return *this;
	}

	std::shared_ptr<IOSymbol> operator[](size_t idx);

	void add(const std::shared_ptr<IOSymbol> key, const std::shared_ptr<IOObject> value);
	void add(const char* key, const std::shared_ptr<IOObject> value);
	std::optional<std::shared_ptr<IOObject>> get(const char* key);
	std::optional<std::shared_ptr<IOObject>> get(const std::shared_ptr<IOSymbol> key);

	bool has_key(const char * key);
	bool has_key(const std::shared_ptr<IOSymbol> key);

	std::unique_ptr<IOList> get_keys(void);
	std::unique_ptr<IOList> get_values(void);

	OPERATOR_NEW_DELETE_DELC
};

#endif
