#include <cstddef>
#include <iostream>
#include "bus.h"
#include <cstring>

SB_Bus* SB_Bus::_instance = nullptr;
static SB_Bus* g_spacebus = SB_Bus::GetInstance();

SB_Bus* SB_Bus::GetInstance(){
    if(SB_Bus::_instance == nullptr){
        SB_Bus::_instance = new SB_Bus{10,MSG_MAX_ID,10,10};
    }
    return SB_Bus::_instance;
}

SB_Bus::SB_Bus(std::uint8_t pipe_max_num, std::uint8_t msg_max_id, std::uint8_t msg_max_subs, std::uint8_t pipe_max_depth):
    pipe_max_num{pipe_max_num}, 
    msg_max_id{msg_max_id},
    msg_max_subs{msg_max_subs},
    pipe_max_depth{pipe_max_depth}{
        pipes = new SB_Pipe*[pipe_max_num]();
        msg_id_pipe_map = new std::uint8_t*[msg_max_id]();

        for(size_t i = 0; i < msg_max_id; i++){
            msg_id_pipe_map[i] = new std::uint8_t[msg_max_subs]();
        }
        msg_id_pipe_lens = new std::uint8_t[msg_max_id]();
};

SB_Bus::~SB_Bus(){
    delete[] pipes;

    for(size_t i = 0; i < msg_max_id; i++){
        delete[] msg_id_pipe_map[i];
    }
    delete[] msg_id_pipe_map;
}

size_t SB_Bus::SubscribePipe(std::uint8_t pipeNum, std::uint8_t msgID){
    if(msgID >= msg_max_id || pipeNum >= pipe_max_num){
        LOG_ERR("SubscribePipe: msg_id is outside of max range\n");
        return SB_FAIL;
    }

    if(GetPipeByNum(pipeNum) == nullptr){
        LOG_ERR("SubscribePipe: pipe(%d) does not exist\n", pipeNum);
        return SB_FAIL;
    }

    if(this->msg_id_pipe_lens[msgID] >= msg_max_subs){
        LOG_ERR("SubscribePipe: too many pipes subscribed to msgID: %d\n", msgID);
        return SB_FAIL;
    }

    // Lol no unsubscribing you scrubs
    this->msg_id_pipe_map[msgID][this->msg_id_pipe_lens[msgID]++] = pipeNum;

    return SB_SUCCESS;
}

SB_Pipe* SB_Bus::CreatePipe(std::uint8_t depth){
    if(depth > pipe_max_depth || this->num_pipes >= pipe_max_num){
        LOG_ERR("Depth is too large or num_pipes is too large\n");
        std::cout << static_cast<uint16_t>(pipe_max_depth) << " " 
            << static_cast<uint16_t>(pipe_max_num) << std::endl;
        return nullptr;
    }

    SB_Pipe* pipe = new SB_Pipe{depth, this->num_pipes};

    if(GetPipeByNum(pipe->num) != nullptr){
        LOG_ERR("Pipe Num already exists. Contact an admin if you didn't cause it.\n");
        exit(-1);
    }

    this->pipes[pipe->num] = pipe;
    this->num_pipes++;

    return pipe;
}

SB_Pipe* SB_Bus::GetPipeByNum(std::uint8_t pipeNum){
    if(pipeNum >= pipe_max_num || pipeNum >= this->num_pipes || this->pipes[pipeNum] == nullptr){
        return nullptr;
    }

    return this->pipes[pipeNum];
}

SB_Pipe::SB_Pipe(std::uint8_t depth, std::uint8_t num){
    this->depth = depth;
    this->num = num;
    this->queue_len = 0;
    this->queue = nullptr;
}

std::size_t SB_Pipe::RecvMsg(SB_Msg** msg){
    Node* node = nullptr;

    if((node = this->queue) == nullptr || (this->queue_len == 0)){
        LOG_ERR("The pipe (%u) queue was empty\n", this->num);
        return SB_QUEUE_EMTPY;
    }

    *msg = new SB_Msg{node->data, node->pipe_id, node->msg_id, node->size};

    this->queue = node->next;
    delete node;

    if(this->queue_len > 0)
        this->queue_len -= 1;
    
    return SB_SUCCESS;
}

size_t SB_Bus::SendMsg(const std::string& msg, bool ishex, uint8_t pipe_id, uint8_t msg_id){
    SB_Msg* payload = SB_Pipe::ParsePayload(msg, ishex, pipe_id, msg_id);

    if(!payload){
        LOG_ERR("Unable to parse msg\n");
        return SB_FAIL;
    }

    if(payload->msg_id >= this->msg_max_id){
        LOG_ERR("The msg_id of the payload is outside the MSG_MAX_ID\n");

        delete payload;
        return SB_FAIL;
    }

    size_t ret = SB_SUCCESS;
    uint8_t cur_pipe_num = 0xFF;
    SB_Pipe* pipe = nullptr;

    size_t i = 0;
    if(payload->pipe_id == UINT8_MAX){
        if(this->msg_id_pipe_lens[payload->msg_id] <= this->msg_max_subs){
            bool copy = true;
            for(i = 0; i < this->msg_id_pipe_lens[payload->msg_id]; i++){
                cur_pipe_num = this->msg_id_pipe_map[payload->msg_id][i];
                
                if(i == (this->msg_id_pipe_lens[payload->msg_id]-1)){
                    copy = false;
                }

                pipe = GetPipeByNum(cur_pipe_num);
                if(pipe->SendMsgToPipe(payload, copy) != SB_SUCCESS){
                    LOG_ERR("Unable to send payload to Pipe Num: %d\n", cur_pipe_num);
                    delete payload->data;
                    ret = SB_FAIL;
                }
            }
            if(i == 0){
                LOG_ERR("No pipes subscribed to Msg ID: %d\n", payload->msg_id);
                delete payload->data;
                ret = SB_FAIL;
            }
            payload->data = nullptr;
        }
        else{
            LOG_ERR("Too many pipes subscribed to Msg ID: %d. Bailing out...\n", payload->msg_id);
            exit(-1);
        }
    }
    else{
        for(i = 0; i < this->msg_id_pipe_lens[payload->msg_id]; i++){
            if(this->msg_id_pipe_map[payload->msg_id][i] == payload->pipe_id){
                cur_pipe_num = this->msg_id_pipe_map[payload->msg_id][i];
                break;
            }
        }

        if(payload->pipe_id == cur_pipe_num){
            pipe = GetPipeByNum(cur_pipe_num);
            if(pipe->SendMsgToPipe(payload, false) != SB_SUCCESS){
                LOG_ERR("Unable to send payload to Pipe ID: %d\n", cur_pipe_num);
                delete payload->data;
                ret = SB_FAIL;
            }
        }
        else{
            LOG_ERR("Unable to send payload with Msg ID: %d -> Pipe ID: %d. Not subscribed\n", payload->msg_id, payload->pipe_id);
            delete payload->data;
            ret = SB_FAIL;
        }
        payload->data = nullptr;
    }

    delete payload;

    return ret;
}

size_t SB_Pipe::SendMsgToPipe(SB_Msg* msg, bool copy){
    if(msg == nullptr)
        return SB_FAIL;
    
    if(this->queue_len >= this->depth)
        return SB_QUEUE_FULL;

    Node* node = nullptr;

    node = this->queue;

    while(node && node->next)
        node = node->next;

    if(!node){
        node = new Node{msg, msg->size, copy};
        this->queue = node;
    }
    else{
        node->next = new Node{msg, msg->size, copy};
        node = node->next;
    }

    this->queue_len++;

    return SB_SUCCESS;
}


size_t SB_Pipe::CalcPayloadLen(bool ishex, const std::string& s){
    if(ishex && (s.length() % 2 == 0)){
        return s.length() / 2;
    }
    else{
        return s.length();
    }
}

SB_Msg* SB_Pipe::ParsePayload(const std::string& s, bool ishex, uint8_t pipe_id, uint8_t msg_id){
    if(s.length() == 0){
        return nullptr;
    }

    uint8_t* msg_s = AllocatePlBuff(ishex, s);

    if(ishex){
        char cur_byte[3] = {0};

        for(size_t i = 0, j = 0; i < CalcPayloadLen(ishex, s); i+=2, j++){
            cur_byte[0] = s[i];
            cur_byte[1] = s[i+1];
            msg_s[j] = static_cast<uint8_t>(std::strtol(cur_byte, nullptr, 16));
        }
    }
    else{
        for(size_t i = 0; i < CalcPayloadLen(ishex, s); i++){
            msg_s[i] = static_cast<uint8_t>(s[i]);
        }
    }

    SB_Msg* payload = new SB_Msg{
        msg_s,
        pipe_id,
        msg_id,
        CalcPayloadLen(ishex, s)
    };
 
    return payload;
}

SB_Pipe::~SB_Pipe(){
    LOG("Destroying pipe: %d\n", this->num);
}

SB_Msg::~SB_Msg(){ 
    LOG("Clearing msg (%d : %d)\n", this->pipe_id, this->msg_id);
    delete this->data;
}

Node::Node(SB_Msg* msg, size_t size, bool copy){
    this->msg_id = msg->msg_id;
    this->size = msg->size;

    if(copy){
        this->data = new uint8_t[msg->size];
        memcpy(this->data, msg->data, this->size);
    }
    else{
        this->data = msg->data;
    }
    
    this->next = nullptr;
}

Node::~Node(){
    this->next = nullptr;
    this->data = nullptr;
}

uint8_t* SB_Pipe::AllocatePlBuff(bool ishex, const std::string& s){
    if(ishex){
        return new uint8_t[s.length() / 2];
    }
    else{
        return new uint8_t[s.length()];
    }
}

SB_Msg::SB_Msg(uint8_t* data, uint8_t pipe_id, uint8_t msg_id, size_t size){
    this->data = data;
    this->pipe_id = pipe_id;
    this->msg_id = msg_id;
    this->size = size;
}