#include "relay.hpp"
#include "settings.hpp"
#include "wqueue.hpp"

#include <drogon/drogon.h>

#include <iostream>
#include <random>
#include <sstream>
#include <utility>

using namespace drogon;

std::stringstream makeStream()
{
	std::stringstream ss;
	ss << std::hex << std::setfill('0');
	return ss;
}

std::string randomKey()
{
	static std::random_device rd;
	static std::mt19937 gen(rd());
	static std::stringstream ss = makeStream();
	std::uniform_int_distribution dist{0, 255};
	ss.str("");
	for (int i = 0; i < 16; i++) {
		ss << std::setw(2) << dist(gen);
	}
	return ss.str();
}


class JuceWorker : public Worker<std::string>
{
public:
	using Worker<std::string>::Worker;

	static std::string getAudioFile(const std::string& path)
	{
		if (auto audio = path + "/" INPUT_AUDIO_FILENAME_NO_EXT ".mp3"; juce::File(audio).existsAsFile()) {
			return audio;
		} else if (audio = path + "/" INPUT_AUDIO_FILENAME_NO_EXT ".wav"; juce::File(audio).existsAsFile()) {
			return audio;
		}
		return "";
	}

	virtual std::pair<bool, std::string> process(const std::string& key) override
	{
		auto path = app().getUploadPath() + "/" + key;
		auto score = path + "/" INPUT_SCORE_FILENAME;
		auto outfile = path + "/" OUTPUT_AUDIO_FILENAME;
		auto audio = getAudioFile(path);
		if (audio.empty()) {
			std::cout << "[ERROR] couldn't find audio file" << std::endl;
			return {false, "your audio file mysteriously vanished"};
		}

		auto res = generateRhythmicBleeps(key, audio, score, outfile);

		if (res.wasOk()) {
			std::cout << "(" << key << "): successfully generated audio" << std::endl;
			return {true, ""};
		} else {
			std::cout << "[ERROR] (" << key << ") " << res.getErrorMessage() << std::endl;
			return {false, res.getErrorMessage().toStdString()};
		}
	}
};

void logRequest(const HttpRequestPtr& req)
{
	auto q = req->getQuery();
	LOG_INFO << req->getMethodString() << " - " << req->getPeerAddr().toIp() << " - " << req->getOriginalPath()
			 << (q.empty() ? "" : "?" + q);
}

bool checkFileExists(const char* s)
{
	if (FILE* f = fopen(s, "r")) {
		fclose(f);
		return true;
	}
	return false;
}


int main()
{
	WorkQueue<std::string> wqueue;

	for (int i = 0; i < NUM_WORKERS; i++) {
		auto worker = new JuceWorker(wqueue);
		worker->start();
	}

	app().loadConfigFile("config.json");

	app().registerHandler("/", [](const HttpRequestPtr& req, std::function<void(const HttpResponsePtr&)>&& callback) {
		logRequest(req);
		auto resp = HttpResponse::newHttpViewResponse("upload");
		callback(resp);
	});

	app().registerHandler("/upload",
						  [&](const HttpRequestPtr& req, std::function<void(const HttpResponsePtr&)>&& callback) {
							  logRequest(req);

							  MultiPartParser fileUpload;
							  if (fileUpload.parse(req) != 0 || fileUpload.getFiles().size() != 2) {
								  auto resp = HttpResponse::newHttpResponse();
								  resp->setBody("Expected two files: audio and score.");
								  resp->setStatusCode(k403Forbidden);
								  callback(resp);
								  return;
							  }

							  std::unordered_map<std::string, HttpFile> map = fileUpload.getFilesMap();
							  if (!map.contains("audio")) {
								  auto resp = HttpResponse::newHttpResponse();
								  resp->setBody("Missing file: audio.");
								  resp->setStatusCode(k403Forbidden);
								  callback(resp);
								  return;
							  }
							  if (!map.contains("score")) {
								  auto resp = HttpResponse::newHttpResponse();
								  resp->setBody("Missing file: score.");
								  resp->setStatusCode(k403Forbidden);
								  callback(resp);
								  return;
							  }

							  auto key = randomKey();
							  auto resp = HttpResponse::newHttpResponse();
							  resp->setBody(key);
							  resp->setStatusCode(k200OK);
							  callback(resp);

							  auto audio = map.find("audio")->second;
							  auto score = map.find("score")->second;

							  auto path = app().getUploadPath() + "/" + key;
							  LOG_INFO << "saving files to " << path;
							  auto audioPath =
								  path + "/" INPUT_AUDIO_FILENAME_NO_EXT "." + std::string{audio.getFileExtension()};
							  audio.saveAs(audioPath);
							  score.saveAs(path + "/" INPUT_SCORE_FILENAME);

							  LOG_INFO << "enqueueing " << key;
							  wqueue.enqueue(key);
						  },
						  {Post});

	app().registerHandler(
		"/status?id={}",
		[&](const HttpRequestPtr& req, std::function<void(const HttpResponsePtr&)>&& callback, const std::string& key) {
			logRequest(req);

			auto resp = HttpResponse::newHttpResponse();
			auto status = wqueue.getStatus(key);
			if (status.state() == QueueStatus::None)
				resp->setStatusCode(k404NotFound);
			else
				resp->setStatusCode(k200OK);

			LOG_INFO << "get status [" << key << "]: " << status.to_string();
			resp->setBody(status.to_string());
			callback(resp);
		});

	app().registerHandler(
		"/audio?id={}",
		[&](const HttpRequestPtr& req, std::function<void(const HttpResponsePtr&)>&& callback, const std::string& key) {
			logRequest(req);

			auto file = app().getUploadPath() + "/" + key + "/" OUTPUT_AUDIO_FILENAME;

			if (key.find("..") == std::string::npos	   // "Don't be a script kiddie."
				&& key.find('\0') == std::string::npos // "Try harder."
				&& checkFileExists(file.c_str()))
			{
				auto resp = HttpResponse::newFileResponse(file, "", CT_CUSTOM, "audio/wav");
				callback(resp);
			} else {
				auto resp = HttpResponse::newHttpResponse();
				resp->setStatusCode(k404NotFound);
				callback(resp);
			}
		});


	LOG_INFO << "running webserver...";
	app().run();
}