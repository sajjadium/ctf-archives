#pragma once

#include "bus.h"

enum class STAR_MSGIDS : std::uint8_t{
    TEST_MSG=100,
    GET_STARS=101,              // NOT IMPLEMENTED UNTIL TESTING COMPLETE
    NUM_STARS=102,              // NOT IMPLEMENTED UNTIL TESTING COMPLETE
    BRIGHTEST_STARS=103,        // NOT IMPLEMENTED UNTIL TESTING COMPLETE
    RESET=104,                  // NOT IMPLEMENTED UNTIL TESTING COMPLETE
    CALIBRATE=105,              // NOT IMPLEMENTED UNTIL TESTING COMPLETE
    QUATERNION=106              // NOT IMPLEMENTED UNTIL TESTING COMPLETE
};

class StarTracker{
    public:
        StarTracker();
        ~StarTracker();
        size_t main_loop();
        size_t handle_msg();
        uint8_t get_pipe_id();
    protected:
        size_t test_msg(SB_Msg* msg);       // 100
    private:
        SB_Pipe* pipe;
};