#pragma once
#include <cstddef>
#include <string>

// Debugging (yes logs are enabled on the remote chal)
#define DEBUG 1
#if DEBUG
    #define LOG printf
#else
    #define LOG(...) while(0){}
#endif

#define LOG_ERR(...) fprintf(stderr, __VA_ARGS__)

// DO NOT CHANGE BELOW
#define NOT_IN_USE     0xFF
#define MSG_MAX_ID     UINT8_MAX
#define SB_SUCCESS     0
#define SB_FAIL        1
#define SB_QUEUE_FULL  7
#define SB_QUEUE_EMTPY 8

struct SB_Msg{
    SB_Msg(uint8_t* data, uint8_t pipe_id, uint8_t msg_id, size_t size);
    ~SB_Msg();
    std::uint8_t pipe_id;
    std::uint8_t msg_id;
    size_t size;
    uint8_t *data;
};
class Node{
    public:
        Node(SB_Msg* msg, size_t size, bool copy);
        ~Node();
        Node* next;
        uint8_t msg_id;
        uint8_t pipe_id;
        size_t size;
        uint8_t* data;
};

class SB_Pipe{
    public:
        SB_Pipe(std::uint8_t depth, std::uint8_t num);
        ~SB_Pipe();

        static SB_Msg* ParsePayload(const std::string& msg, bool ishex, uint8_t pipe_id, uint8_t msg_id);

        static void FreeNode(Node* node);
        size_t RecvMsg(SB_Msg** msg);
        size_t SendMsgToPipe(SB_Msg* payload, bool copy);
        std::uint8_t num;
    private:
        static uint8_t* AllocatePlBuff(bool ishex, const std::string& s);
        static size_t CalcPayloadLen(bool ishex, const std::string& s);
        std::uint8_t depth;
        std::uint8_t queue_len;
        Node* queue;
};

class SB_Bus{
    public:
        ~SB_Bus();
        SB_Pipe* CreatePipe(std::uint8_t depth);
        SB_Pipe* GetPipeByNum(std::uint8_t pipeNum);
        size_t   SubscribePipe(std::uint8_t pipeNum, std::uint8_t msgID);
        size_t   SendMsg(const std::string& msg, bool ishex, uint8_t pipe_id, uint8_t msg_id);
        static SB_Bus* GetInstance();
    private:
        SB_Bus(std::uint8_t pipe_max_num, std::uint8_t msg_max_id, std::uint8_t msg_max_subs, std::uint8_t pipe_max_depth);
        const std::uint8_t pipe_max_num;
        const std::uint8_t msg_max_id;
        const std::uint8_t msg_max_subs;
        const std::uint8_t pipe_max_depth;
        static SB_Bus* _instance;
    protected:
        std::uint8_t num_pipes;
        SB_Pipe** pipes;

        std::uint8_t** msg_id_pipe_map;
        std::uint8_t* msg_id_pipe_lens;
};
