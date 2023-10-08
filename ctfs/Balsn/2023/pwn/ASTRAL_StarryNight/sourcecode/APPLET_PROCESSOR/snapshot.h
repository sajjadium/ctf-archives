#ifndef __SNAPSHOT_HEADER__
#define __SNAPSHOT_HEADER__

typedef struct SNAPSHOT {
  APPLET_TASK_ID task;
  uint8_t checkpointDigest[DIGEST_SIZE];
} SNAPSHOT;

extern SNAPSHOT snapshot[APPLET_TASK_CNT_MAX];

#endif
