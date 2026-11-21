#pragma once

#define RES_SLEEP 3
#define handle_error()                                          \
  do {                                                          \
    sleep(RES_SLEEP);                                           \
    fprintf(stderr,"[!] Restarting due to error in %s:%d %s\n", \
        __FILE__, __LINE__, __FUNCTION__);                      \
    execv(argv[0], argv);                                       \
    exit(1);                                                    \
  } while(0);

// ./argv[0] <START> <MAX>
// For example ./argv[0] 0 10 -> Retry 10 times in case of error
if(argc != 3) {
  fprintf(stderr, "[!] Initialize the daemon properly: %s 0 MAX\n", argv[0]);
  return 1;
}

// Read maximum reboots our daemon should try before giving up
long int max = strtol(argv[2], NULL, 10);
if(max < 0)
  max = 0;

// Read current restart counter
long int counter = strtol(argv[1], NULL, 10);
if(counter < 0)
  counter = 0;
counter++;

// Check if we reached the limit of restarts
if(counter > max) {
  fprintf(stderr, "[!] Maximum number of errors (%li) reached\n", max);
  return 1;
}

// Update argv[1] with updated counter in case we have to restart
char newargv1[20]; // 20 == ceil(log10(2^64))
memset(newargv1, 0x0, sizeof(newargv1));
snprintf(newargv1, sizeof(newargv1), "%li", counter);
argv[1] = newargv1;
