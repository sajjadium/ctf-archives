#include <stdint.h>
#include <arpa/inet.h>
#define PORT 4001


#define SOCKET_FAIL 0x80010001
#define STATUS_SUCCESS 0x0

#define SLOT_MAX 90

typedef struct boat_coords
{
    double lat;
    double lon;
} boat_coords_t;

enum STATUS {
    under_way_engine =  0,
    at_anchor =         1,
    fishing =           7,
    under_way_sailing = 8,
};

typedef struct A_AIS_BDC {
    enum STATUS status;
    uint32_t boat_id;
    boat_coords_t position;
} A_AIS_BDC_t;

typedef struct A_AIS_MSG {
    enum STATUS status;
    uint32_t boat_id;
    uint32_t dest_id;
    boat_coords_t position;
} A_AIS_MSG_t;
// AIS Addressed Binary Message
typedef struct AIS_BAM_BDC {
    uint32_t boat_id;
    int8_t slot_size;
    uint8_t crc;
    char data[1];   
} AIS_BAM_BDC_t;

typedef struct AIS_BAM_MSG {
    uint32_t boat_id;
    uint32_t dest_id;
    int8_t slot_size;
    uint8_t crc;
    char data[1];   
} AIS_BAM_MSG_t;
typedef struct AIS_SAFETY_MSG {
    uint32_t sender_id;
    uint32_t dest_id;
    int8_t slot_size;
    char data[1];
} AIS_SAFETY_MSG_t;

typedef struct AIS_SAFETY_BDC {
    uint32_t boat_id;
    int8_t slot_size;
    char data[1];
} AIS_SAFETY_BDC_t;


typedef struct AIS_SAFETY_ACK
{
    uint32_t boat_id;
    uint32_t bytes_copied;
} AIS_SAFETY_ACK_t;

enum boats_enum {
    boat1 = 0,
    boat2,
    boat3,
    boat4,
    boat5,
    boat6,
    boat7,
    boat8,
    boat9,
    boat10,
};


typedef struct boat {
    char boat_name[0x10];
    uint32_t boat_id;
    boat_coords_t coords;
    uint8_t active;
} boat_t;

enum MSG_TYPE {
    POS_SCH_REPORT =  1,
    POS_ASS_REPORT =  2,
    POS_SPC_REPORT =  3,
    BIN_ADDR_MSG =    4,
    BIN_ADDR_ACK =    5,
    BIN_ADDR_BDC =    6,
    SAFETY_MSG =      12,
    SAFETY_ACK =      13,
    SAFETY_BDC =      14,
    INTERROGATE =     15,
    INTERROGATE_RSP = 16
}; 

typedef struct location {
    double lat;
    double lon;
} location_t;

typedef struct header {
    uint16_t senderBoatID;
    uint16_t receiverBoatID;
} header_t;

typedef struct ais_frame {
    uint32_t preamble;   // 0x55555555
    uint8_t start_flag;  // 0x7e
    uint8_t type;
    uint8_t crc;
    uint8_t data[SLOT_MAX];
    uint8_t stop_flag;   // 0x7e
}__attribute__((packed, aligned(1))) ais_frame_t;

typedef struct position_report {
    header_t header;
    location_t coords;
} position_report_t;

