#include <iostream>
#include <unistd.h>
#include "startracker.h"

StarTracker::StarTracker(){
    SB_Bus* spacebus = SB_Bus::GetInstance();
    this->pipe = spacebus->CreatePipe(10);

    uint64_t ret = 0;

    ret |= spacebus->SubscribePipe(this->pipe->num, static_cast<uint8_t>(STAR_MSGIDS::TEST_MSG));
    ret |= spacebus->SubscribePipe(this->pipe->num, static_cast<uint8_t>(STAR_MSGIDS::GET_STARS));
    ret |= spacebus->SubscribePipe(this->pipe->num, static_cast<uint8_t>(STAR_MSGIDS::NUM_STARS));
    ret |= spacebus->SubscribePipe(this->pipe->num, static_cast<uint8_t>(STAR_MSGIDS::BRIGHTEST_STARS));
    ret |= spacebus->SubscribePipe(this->pipe->num, static_cast<uint8_t>(STAR_MSGIDS::RESET));
    ret |= spacebus->SubscribePipe(this->pipe->num, static_cast<uint8_t>(STAR_MSGIDS::CALIBRATE));
    ret |= spacebus->SubscribePipe(this->pipe->num, static_cast<uint8_t>(STAR_MSGIDS::QUATERNION));

    if(ret != 0){
        std::cout << ret;
        std::cout << "Could not subscribe pipe to all startracker msg ids..." << std::endl;
        exit(1);
    }
}

StarTracker::~StarTracker(){

}

size_t StarTracker::main_loop(){

    while(true){
        this->handle_msg();
        sleep(1);
    }
}

size_t StarTracker::handle_msg(){
    SB_Msg* msg = nullptr;
    size_t ret = SB_FAIL;

    ret = this->pipe->RecvMsg(&msg);
    if(ret != SB_SUCCESS) return ret;

    STAR_MSGIDS msg_id = static_cast<STAR_MSGIDS>(msg->msg_id);
    switch(msg_id){
        case STAR_MSGIDS::TEST_MSG:
            std::cout << "StarTracker: Testing Message" << std::endl;
            ret = this->test_msg(msg);
            break;
        default:
            std::cout << "Got unknown msg_id for Startracker or DISABLED" << std::endl;
            ret = SB_FAIL;
    }

    delete msg;
    return ret;
}

uint8_t StarTracker::get_pipe_id(){
    return this->pipe->num;
}

size_t StarTracker::test_msg(SB_Msg* msg){ // 100   

    for(size_t i = 0; i < msg->size; i++){
        printf("%#x ", msg->data[i]);
    }

    std::cout << std::endl;

    return SB_SUCCESS;
}