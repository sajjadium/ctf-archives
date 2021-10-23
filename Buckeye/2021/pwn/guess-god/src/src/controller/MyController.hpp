#ifndef MyController_hpp
#define MyController_hpp

#include "dto/DTOs.hpp"
#include <iostream>
#include <sstream>

#include "oatpp/web/server/api/ApiController.hpp"
#include "oatpp/core/macro/codegen.hpp"
#include "oatpp/core/macro/component.hpp"
#include "oatpp/core/data/stream/FileStream.hpp"
#include "oatpp/web/mime/multipart/InMemoryPartReader.hpp"
#include "oatpp/web/mime/multipart/Reader.hpp"
#include "oatpp/web/mime/multipart/PartList.hpp"

namespace multipart = oatpp::web::mime::multipart;

#include OATPP_CODEGEN_BEGIN(ApiController) //<-- Begin Codegen

/**
 * Sample Api Controller.
 */
class MyController : public oatpp::web::server::api::ApiController {
public:
  /**
   * Constructor with object mapper.
   * @param objectMapper - default object mapper used to serialize/deserialize DTOs.
   */
  MyController(OATPP_COMPONENT(std::shared_ptr<ObjectMapper>, objectMapper))
    : oatpp::web::server::api::ApiController(objectMapper)
  {
    OATPP_LOGD("MyController", "Constructor");
  }

public:
  
  ENDPOINT("GET", "/", root) {
    auto dto = MyDto::createShared();
    dto->statusCode = 200;
    dto->message = "Hello World!";
    return createDtoResponse(Status::CODE_200, dto);
  }

  ENDPOINT("GET", "/files/{fileId}", getFileById, PATH(Int32, fileId), QUERY(Boolean, extract, "extract", "false")) {
    OATPP_LOGD("GetFile", "fileId=%d", *fileId);
    
    /* Check if file exists */
    lock.lock();
    auto exists = fileMap.find(fileId) != fileMap.end();
    lock.unlock();
    
    if (exists) {
      /* File exists */
      auto f = get_file(fileId, extract);
      
      if (f == NULL) {
        auto dto = MyDto::createShared();
        dto->statusCode = 500;
        dto->message = "Internal server error";
        return createDtoResponse(Status::CODE_500, dto);
      }
      
      return createResponse(Status::CODE_200, f);
    } else {
      auto dto = MyDto::createShared();
      dto->statusCode = 404;
      dto->message = "File not found";
      return createDtoResponse(Status::CODE_404, dto);
    }
    return createResponse(Status::CODE_200, "OK");
  }

  /* File uploads */
  ENDPOINT("POST", "/upload/{fileId}", upload, PATH(Int32, fileId), REQUEST(std::shared_ptr<IncomingRequest>, request)) {
    
    lock.lock();
    auto exists = fileMap.find(fileId) != fileMap.end();
    lock.unlock();

    OATPP_LOGD("UploadFile", "fileId=%d", *fileId);
    if (exists) {
      auto dto = MyDto::createShared();
      dto->statusCode = 400;
      dto->message = "File already exists";
      return createDtoResponse(Status::CODE_400, dto);
    }

    std::ostringstream filename;
    filename << "files/" << fileId;
    auto filename_str = filename.str();
    
    /* Prepare multipart container. */
    auto multipart = std::make_shared<multipart::PartList>(request->getHeaders());
    multipart::Reader multipartReader(multipart.get());
    multipartReader.setPartReader("file", multipart::createInMemoryPartReader(128 * 1024 /* 128K max upload */));
    request->transferBody(&multipartReader);
    
    auto filePart = multipart->getNamedPart("file");

    /* Assert part is not null */
    OATPP_ASSERT_HTTP(filePart, Status::CODE_400, "Missing file upload");
 
    filePart->getInMemoryData()->saveToFile(filename_str.c_str());
    
    lock.lock();
    fileMap[fileId] = filename_str;
    lock.unlock();
    return createResponse(Status::CODE_200, "OK");
  }

private:
  std::map<std::pair<int, bool>,std::shared_ptr<oatpp::base::StrBuffer>> fileCache;
  std::map<int, std::string> fileMap;
  std::mutex lock;
  
  /* helper functions */
  std::shared_ptr<oatpp::base::StrBuffer> get_file(int file_id, bool compress);
};

#include OATPP_CODEGEN_END(ApiController) //<-- End Codegen

#endif /* MyController_hpp */
