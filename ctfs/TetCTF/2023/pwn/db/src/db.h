
#ifndef DB_H
#define DB_H

#include "IOObjects.h"
#include <memory>
#include <optional>

#define SECRET_BUFFER 10

class SecretBuffer: public IOObject
{
private:
	IOBytes key;
	IOBytes buffer;
	bool is_enc;

	void do_xor(void);

public:
	SecretBuffer(): IOObject(SECRET_BUFFER) {}
	SecretBuffer(const char *key, size_t key_size, const char *buffer, size_t buffer_size);
	SecretBuffer(const IOBytes& key, const IOBytes& buffer);
	~SecretBuffer();

	SecretBuffer& operator=(const SecretBuffer& that);
	SecretBuffer& operator+=(const SecretBuffer& that);

	void set_key(const IOBytes& key);
	void attach_buffer(const IOBytes& buffer);

	void encrypt(void);
	void decrypt(const IOBytes& key);

	std::optional<std::unique_ptr<IOBytes>> get_buffer();
	bool is_encryped(void);

	OPERATOR_NEW_DELETE_DELC
};

class DB
{
private:
	IODict users;
	IODict secrets;

	bool do_verify(std::shared_ptr<IOSymbol> user_name, std::shared_ptr<IOString> user_pass);

public:
	DB();
	~DB();

	size_t db_size();
	bool has_user(std::shared_ptr<IOSymbol> user_name);
	bool create_user(std::shared_ptr<IOSymbol> user_name, std::shared_ptr<IOString> user_pass);
	bool login(std::shared_ptr<IOSymbol> user_name, std::shared_ptr<IOString> user_pass);
	bool create_secret_for(std::shared_ptr<IOSymbol> user_name, std::shared_ptr<IOString> user_pass, std::shared_ptr<SecretBuffer> secret);
	std::optional<std::unique_ptr<IOBytes>> read_secret_of(
								std::shared_ptr<IOSymbol> user_name,
								std::shared_ptr<IOString> user_pass,
								std::shared_ptr<IOBytes> key);
	std::unique_ptr<IOList> get_all_users(void);
	void del_user(std::shared_ptr<IOSymbol> user_name);

	OPERATOR_NEW_DELETE_DELC
};


#endif
