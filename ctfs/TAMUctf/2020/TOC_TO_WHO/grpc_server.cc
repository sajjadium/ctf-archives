/*
 *
 * Copyright 2015, Google Inc.
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are
 * met:
 *
 *     * Redistributions of source code must retain the above copyright
 * notice, this list of conditions and the following disclaimer.
 *     * Redistributions in binary form must reproduce the above
 * copyright notice, this list of conditions and the following disclaimer
 * in the documentation and/or other materials provided with the
 * distribution.
 *     * Neither the name of Google Inc. nor the names of its
 * contributors may be used to endorse or promote products derived from
 * this software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
 * "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
 * LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
 * A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
 * OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
 * SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
 * LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
 * DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
 * THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
 * OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 *
 */

#include <ctime>

#include <google/protobuf/timestamp.pb.h>
#include <google/protobuf/duration.pb.h>

#include <stdio.h>
#include <fstream>
#include <iostream>
#include <memory>
#include <string>
#include <stdlib.h>
#include <unistd.h>
#include <map>
#include <cstring>
#include <google/protobuf/util/time_util.h>
#include <grpc++/grpc++.h>

#include "protobuf.grpc.pb.h"
#include "server.h"

using google::protobuf::Timestamp;
using google::protobuf::Duration;
using grpc::Server;
using grpc::ServerBuilder;
using grpc::ServerContext;
using grpc::ServerReader;
using grpc::ServerReaderWriter;
using grpc::ServerWriter;
using grpc::Status;
using tamuctf::ServiceUser;
using tamuctf::Request;
using tamuctf::Reply;
using tamuctf::EchoService;

class EchoServiceImpl final : public EchoService::Service {
    Status Login(ServerContext* context, const Request* request, Reply* reply) override {
        char* cmsg = login(const_cast<char*>(context->peer().c_str()),const_cast<char*>(request->username().c_str()),const_cast<char*>(request->msg().c_str()));
        std::string msg(cmsg);
        free(cmsg);
        reply->set_msg(msg);
        return Status::OK;
    }

    Status Logout(ServerContext* context, const ServiceUser* user, Reply* reply) override {
        char* cmsg = logout(const_cast<char*>(context->peer().c_str()), const_cast<char*>(user->username().c_str()));
        std::string msg(cmsg);
        reply->set_msg(msg);
        return Status::OK;
    }

    Status SendEcho(ServerContext* context, const Request* request, Reply* reply) override {
        char* cmsg = sendEcho(const_cast<char*>(context->peer().c_str()), const_cast<char*>(request->username().c_str()), const_cast<char*>(request->msg().c_str()));
        std::string msg(cmsg);
        reply->set_msg(msg);
        return Status::OK;
    }

    Status ReceiveEcho(ServerContext* context, const ServiceUser* user, Reply* reply) override {
        char* cmsg = receiveEcho(const_cast<char*>(context->peer().c_str()), const_cast<char*>(user->username().c_str()));
        std::string msg(cmsg);
        free(cmsg);
        reply->set_msg(msg);
        return Status::OK;
    }
};

void RunServer(std::string port_no) {
  std::string server_address = "0.0.0.0:"+port_no;
  EchoServiceImpl service;

  ServerBuilder builder;
  builder.AddListeningPort(server_address, grpc::InsecureServerCredentials());
  builder.RegisterService(&service);
  std::unique_ptr<Server> server(builder.BuildAndStart());
  std::cout << "Server listening on " << server_address << std::endl;

  server->Wait();
}

int main(int argc, char** argv) {
  
  std::string port = "3010";
  int opt = 0;
  while ((opt = getopt(argc, argv, "p:")) != -1){
    switch(opt) {
      case 'p':
          port = optarg;break;
      default:
	  std::cerr << "Invalid Command Line Argument\n";
    }
  }
  RunServer(port);

  return 0;
}
