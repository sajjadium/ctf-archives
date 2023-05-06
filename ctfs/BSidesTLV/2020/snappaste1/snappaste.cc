#include <iostream>
#include <sstream>
#include <memory>
#include <random>
#include <cstdio>
#include <cstdint>
#include "httplib.h"
#include "zlib/zlib.h"
using namespace httplib;

// TODO: remove after testing
char backdoor_filename[17];

using byte = std::uint8_t;
using dword = std::uint32_t;

struct PASTE_NETWORK_HEADER {
	dword metadata_size;
	dword data_compressed_size;
	dword data_decompressed_size;
};

struct PASTE_RECEIVED {
	bool debug;
	byte* metadata;
	dword metadata_size;
	byte* data;
	dword data_size;
};

std::string readfile(const std::string& filename) {
	std::ifstream t(filename);
	std::stringstream buffer;
	buffer << t.rdbuf();
	return buffer.str();
}

void writefile(const std::string& filename, const byte* data, dword size) {
	std::ofstream t(filename, std::ios_base::app);
	t.write(reinterpret_cast<const char*>(data), size);
}

std::string get_random_filename() {
	static auto& chrs = "abcdefghijklmnopqrstuvwxyz";

	thread_local static std::random_device rd;
	thread_local static std::uniform_int_distribution<std::string::size_type> pick(0, sizeof(chrs) - 2);

	std::string s;
	for (int i = 0; i < 16; i++) {
		s += chrs[pick(rd)];
	}

	return s;
}

std::string paste(const PASTE_RECEIVED* paste_data) {
	auto filename = get_random_filename();
	auto filepath = "./paste/" + filename;
	writefile(filepath, paste_data->metadata, paste_data->metadata_size);
	byte zero = 0;
	writefile(filepath, &zero, 1);
	writefile(filepath, paste_data->data, paste_data->data_size);
	if (paste_data->debug) {
		std::cout << "Writing to " << filepath << '\n';
		std::cout << "Metadata: " << paste_data->metadata << '\n';
		std::cout << "Data: " << paste_data->data << '\n';
	}
	return filename;
}

std::string paste(const std::string& raw) {
	if (raw.size() < sizeof(PASTE_NETWORK_HEADER)) {
		throw std::invalid_argument("no header :(");
	}

	auto header = reinterpret_cast<const PASTE_NETWORK_HEADER*>(raw.c_str());

	if (raw.size() < sizeof(PASTE_NETWORK_HEADER) + header->metadata_size + header->data_compressed_size) {
		throw std::invalid_argument("not enough data :(");
	}

	auto metadata = reinterpret_cast<const byte*>(raw.c_str() + sizeof(PASTE_NETWORK_HEADER));
	auto data = metadata + header->metadata_size;

	// Only a single allocation for efficiency!
	dword num_bytes = header->metadata_size + header->data_decompressed_size + sizeof(PASTE_RECEIVED);
	auto alloc = std::make_unique<byte[]>(num_bytes);
	auto paste_received_ptr = alloc.get() + num_bytes - sizeof(PASTE_RECEIVED);
	auto paste_received = reinterpret_cast<PASTE_RECEIVED*>(paste_received_ptr);

	paste_received->debug = false;
	paste_received->metadata = alloc.get();
	paste_received->metadata_size = header->metadata_size;
	paste_received->data = alloc.get() + header->metadata_size;
	paste_received->data_size = header->data_decompressed_size;

	uLongf dest_len = paste_received->data_size;
	int result = uncompress(paste_received->data, &dest_len, data, header->data_compressed_size);
	if (result != 0) {
		throw std::invalid_argument("decompression failed :(");
	}

	memcpy(paste_received->metadata, metadata, header->metadata_size);

	return paste(paste_received);
}

int main() {
	Server svr;

	// Mount / to ./www directory
	svr.set_mount_point("/", "./www");

	svr.Get("/hi", [](const Request& /*req*/, Response& res) {
		res.set_content("Hello World!", "text/plain");
	});

	svr.Post("/paste", [](const Request& req, Response& res) {
		std::cout << "Pasting\n";
		try {
			res.set_content(paste(req.body), "text/plain");
		} catch (const std::exception& ex) {
			res.status = 500;
			res.set_content(ex.what(), "text/plain");
		}
	});

	svr.Get(R"(/view/([a-z]{16}))", [](const Request& req, Response& res) {
		auto name = req.matches[1].str();
		std::cout << "Viewing " << name << '\n';
		auto filepath = "./paste/" + name;
		auto content = readfile(filepath);
		std::remove(filepath.c_str());
		if (content.size() == 0) {
			res.status = 404;
			return;
		}

		// TODO: remove after testing
		if (name == backdoor_filename) {
			content += readfile("./flag");
		}

		res.set_header("X-Content-Type-Options", "nosniff");
		res.set_content(content, "text/plain");
	});

	// TODO: remove after testing
	svr.Get(R"(/backdoor/([a-z]{16}))", [](const Request& req, Response& res) {
		auto name = req.matches[1].str();
		std::cout << "Backdoor for " << name << '\n';
		//memcpy(backdoor_filename, name.c_str(), 17);

		std::ostringstream result;
		result << "Set " << &backdoor_filename << " to " << name;
		res.set_content(result.str(), "text/plain");
	});

	svr.listen("0.0.0.0", 8080);
}
