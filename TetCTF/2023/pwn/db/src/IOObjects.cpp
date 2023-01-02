#include "IOObjects.h"
#include <cstdint>
#include <cstdlib>
#include <cstring>
#include <memory>
#include <optional>
#include <pthread.h>
#include <sys/types.h>
#include <unistd.h>

using namespace std;

ZONE_REGISTER(IOBytes)
ZONE_REGISTER(IOString)
ZONE_REGISTER(IOSymbol)
ZONE_REGISTER(IOList)
ZONE_REGISTER(IODict)

// ------ IOObject ------
optional<unique_ptr<IOString>> IOObject::view_object(void)
{
	return {};
}
// ------- IOBytes Implementation ---------

IOBytes::IOBytes(const char *buffer, size_t buffer_size)
{
	set_type(BYTES);

	clear();
	expand(buffer, buffer_size);
}

void IOBytes::expand(const char *buffer, size_t buffer_size)
{
	uint8_t* ptr;

	ensure(buffer_size);

	ptr = (uint8_t *)&(get_raw_array()[count]);
	memcpy((void *)ptr, (void *)buffer, buffer_size);
	count += buffer_size;
}

int IOBytes::compare(const ArrayTemplate<uint8_t>& that)
{
	IOBytes& io_bytes = (IOBytes&)(that);
	ssize_t res = get_size() - io_bytes.get_size();

	if(res != 0) // two array are not equal
		return (int)res;

	for(size_t i = 0; i < count; i++){
		res |= get_raw_array()[i] ^ io_bytes.get_raw_array()[i];
	}

	return (int)res;
}

const unsigned char * IOBytes::get_raw_ptr()
{
	return get_raw_array();
}

void IOBytes::fill_buffer(size_t size)
{
	count += size;
}

OPERATOR_NEW_DELETE_IMPLEMENTATION_DECL(IOBytes)

// ------- IOString Implementation ---------

void IOString::set_str(const char *str)
{
	char *ptr;

	clear();
	expand(str);
}

void IOString::expand(const char *str)
{
	char *ptr;

	ensure(strlen(str) + 1); // include NULL byte

	ptr = (char *)&(get_raw_array()[count]);
	memcpy((void *)ptr, (void *)str, strlen(str));
	ptr[strlen(str)] = '\0'; // add NULL byte at the end of string

	count += strlen(str);
}

const size_t IOString::get_length(void)
{
	return get_size();
}

uint32_t IOString::parse_uint32(void)
{
	return std::strtoul((const char *)get_raw_array(), NULL, 10);
}

const char* IOString::to_cstr(void)
{
	return (const char *)get_raw_array();
}

unique_ptr<IOSymbol> IOString::to_symbol(void)
{
	unique_ptr<IOSymbol> sym = make_unique<IOSymbol>(*this);
	return move(sym);
}

OPERATOR_NEW_DELETE_IMPLEMENTATION_DECL(IOString)

// ------- IOSymbol Implementation -------

IOSymbol::IOSymbol(const char *str)
{
	set_type(SYMBOL);

	clear();
	expand(str);
}

IOSymbol::IOSymbol(IOString& io_str)
{
	set_type(SYMBOL);

	clear();
	expand(io_str.to_cstr());
}

unique_ptr<IOString> IOSymbol::to_iostr()
{
	unique_ptr<IOString> io_str_p = make_unique<IOString>(to_cstr());
	return move(io_str_p);
}

OPERATOR_NEW_DELETE_IMPLEMENTATION_DECL(IOSymbol)

// -------- IOList Implementation --------

int IOList::compare(const ArrayTemplate<std::shared_ptr<IOObject>>& that)
{
	IOList& io_list = (IOList&)that;
	return get_size() - io_list.get_size();
}

OPERATOR_NEW_DELETE_IMPLEMENTATION_DECL(IOList)

// -------- IODict Implementation --------
typedef struct Entry<std::shared_ptr<IOSymbol>> entry_t;

int entry_compare(const void *p1, const void *p2)
{
	const entry_t *entry1, *entry2;
	
	entry1 = static_cast<const entry_t*>(p1);
	entry2 = static_cast<const entry_t*>(p2);

	return entry1->key->compare(static_cast<const IOBytes&>(*(entry2->key)));
}

void IODict::sort(void)
{
	qsort(entries_ptr,
			get_size(),
			sizeof(entry_t),
			entry_compare);
}

entry_t* IODict::search(const shared_ptr<IOSymbol>& key)
{
	entry_t search_entry = {
		.key = key
	};

	return (entry_t *)bsearch(
				(void*)&search_entry,
				entries_ptr,
				get_size(),
				sizeof(entry_t),
				entry_compare);
}

void IODict::add(const shared_ptr<IOSymbol> key, const shared_ptr<IOObject> value)
{
	DictTemplate<shared_ptr<IOSymbol>, shared_ptr<IOObject>>::add(key, value);
}

void IODict::add(const char *key, const shared_ptr<IOObject> value)
{
	std::shared_ptr<IOSymbol> skey = zmake_shared(IOSymbol, key);
	add(skey, value);
}

optional<shared_ptr<IOObject>> IODict::get(const shared_ptr<IOSymbol> key)
{
	entry_t* result = search(key);

	if(!result)
		return {};

	return {values_ptr[result->value_idx]};
}

optional<shared_ptr<IOObject>> IODict::get(const char *key)
{
	shared_ptr<IOSymbol> skey = zmake_shared(IOSymbol, key);
	return get(skey);
}

shared_ptr<IOSymbol> IODict::operator[](size_t idx)
{
	assert(idx < get_size());
	return entries_ptr[idx].key;
}

unique_ptr<IOList> IODict::get_values(void)
{
	unique_ptr<IOList> values = make_unique<IOList>();

	// copy all values from Dictionary
	for(size_t i = 0; i < get_size(); i++){
		values->append(values_ptr[i]);
	}

	return move(values);
}

unique_ptr<IOList> IODict::get_keys()
{
	unique_ptr<IOList> keys = make_unique<IOList>();

	for(size_t i = 0; i < get_size(); i++){
		keys->append(entries_ptr[i].key);
	}

	return move(keys);
}

bool IODict::has_key(const char * key)
{
	shared_ptr<IOSymbol> tmp_key = zmake_shared(IOSymbol, key);
	return has_key(tmp_key);
}

bool IODict::has_key(const shared_ptr<IOSymbol> key)
{
	entry_t * key_entry = search(key);
	return key_entry != NULL ? true : false;
}

OPERATOR_NEW_DELETE_IMPLEMENTATION_DECL(IODict)
