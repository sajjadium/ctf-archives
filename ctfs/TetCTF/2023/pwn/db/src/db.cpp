#include "db.h"
#include <memory>

using namespace std;

ZONE_REGISTER(SecretBuffer)
ZONE_REGISTER(DB);

// ----- SECRET_BUFFER ------

SecretBuffer::SecretBuffer(const char *key, size_t key_size, const char* buffer, size_t buffer_size)
{
	this->key = IOBytes(key, key_size);
	this->buffer = IOBytes(buffer, buffer_size);
	is_enc = false;
}

SecretBuffer::SecretBuffer(const IOBytes& key, const IOBytes& buffer)
{
	this->key = key;
	this->buffer = buffer;
	is_enc = false;
}

// copy operator
SecretBuffer& SecretBuffer::operator=(const SecretBuffer &that)
{
	key = that.key;
	buffer = that.buffer;
	is_enc = that.is_enc;
	return *this;
}

// append operator
SecretBuffer& SecretBuffer::operator+=(const SecretBuffer &that)
{
	// unable to concat one encrypted buffer to decrypted buffer
	if(is_enc != that.is_enc)
		return *this;

	buffer = buffer + that.buffer;
	return *this;
}

void SecretBuffer::set_key(const IOBytes &key)
{
	if(is_enc)
		return;

	this->key = key;
}

void SecretBuffer::attach_buffer(const IOBytes &buffer)
{
	if(is_enc)
		return;

	this->buffer += buffer;
}

void SecretBuffer::do_xor()
{
	for(size_t i = 0; i < this->buffer.get_size(); i++){
		this->buffer[i] = this->buffer[i] ^ this->key[i % this->key.get_size()];
	}
}

void SecretBuffer::encrypt()
{
	if(is_enc)
		return;

	do_xor();

	is_enc = true;
}

void SecretBuffer::decrypt(const IOBytes &key)
{
	if(!is_enc)
		return;

	if(this->key.compare(key)){
		// key are not equal
		return;
	}

	do_xor();

	is_enc = false;
}

optional<unique_ptr<IOBytes>> SecretBuffer::get_buffer()
{
	if(is_enc)
		return {};

	unique_ptr<IOBytes> copy_buffer = make_unique<IOBytes>();
	*copy_buffer += this->buffer;

	return {move(copy_buffer)};
}

bool SecretBuffer::is_encryped()
{
	return is_enc;
}

SecretBuffer::~SecretBuffer()
{
	key.clear();
	buffer.clear();
}

OPERATOR_NEW_DELETE_IMPLEMENTATION_DECL(SecretBuffer)

// DB
DB::DB()
{
	users.clear();
	secrets.clear();
}

DB::~DB()
{
	users.clear();
	secrets.clear();
}

bool DB::do_verify(shared_ptr<IOSymbol> user_name, shared_ptr<IOString> user_pass)
{
	auto dict_pass = users.get(user_name);

	if(!dict_pass.has_value()){
		return false;
	}

	shared_ptr<IOString> pass = dynamic_pointer_cast<IOString>(dict_pass.value());

	if((*pass) != (*user_pass)){
		return false;
	}

	return true;
}

size_t DB::db_size()
{
	return users.get_size();
}

bool DB::login(shared_ptr<IOSymbol> user_name, shared_ptr<IOString> user_pass)
{
	return do_verify(user_name, user_pass);
}

bool DB::create_user(shared_ptr<IOSymbol> user_name, shared_ptr<IOString> user_pass)
{
	if(users.has_key(user_name)){
		// user existed
		return false;
	}

	// create user
	users.add(user_name, user_pass);
	return true;
}

bool DB::create_secret_for(
		shared_ptr<IOSymbol> user_name,
		shared_ptr<IOString> user_pass,
		shared_ptr<SecretBuffer> secret)
{
	if(!do_verify(user_name, user_pass)){
		return false;
	}

	auto secret_value = secrets.get(user_name);
	if(secret_value.has_value()){
		shared_ptr<SecretBuffer> secret_buffer = dynamic_pointer_cast<SecretBuffer>(secret_value.value());
		if(secret_buffer->is_encryped())
			return false;
	}

	secrets.add(user_name, secret);
	return true;
}

optional<unique_ptr<IOBytes>> DB::read_secret_of(
		shared_ptr<IOSymbol> user_name,
		shared_ptr<IOString> user_pass,
		shared_ptr<IOBytes> key)
{
	if(!do_verify(user_name, user_pass))
		return {};

	auto secret_value = secrets.get(user_name);
	if(!secret_value.has_value()){
		// user didn't have secret
		return {};
	}

	shared_ptr<SecretBuffer> secret_buffer = dynamic_pointer_cast<SecretBuffer>(secret_value.value());
	if(!secret_buffer->is_encryped()){
		return {};
	}

	secret_buffer->decrypt(*key);
	auto op_raw_buffer = secret_buffer->get_buffer();

	if(op_raw_buffer.has_value()){
		secret_buffer->encrypt();
		return {move(op_raw_buffer.value())};
	}

	return {};
}

bool DB::has_user(std::shared_ptr<IOSymbol> user_name)
{
	return users.has_key(user_name);
}

unique_ptr<IOList> DB::get_all_users()
{
	return move(users.get_keys());
}

void DB::del_user(shared_ptr<IOSymbol> user_name)
{
	users.remove(user_name);
	secrets.remove(user_name);
}

OPERATOR_NEW_DELETE_IMPLEMENTATION_DECL(DB)
