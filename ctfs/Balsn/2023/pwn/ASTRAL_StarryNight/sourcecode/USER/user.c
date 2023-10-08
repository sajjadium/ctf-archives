#include "user.h"

void recordStatistics(ACTIVITY_STAT *stat, uint8_t type) {
  switch (type) {
    case 1:
      stat->registerCnt++;
      break;
    case 2:
      stat->unregisterCnt++;
      break;
    case 3:
      stat->invokeCnt++;
      break;
    case 4:
      stat->resultCnt++;
      break;
    case 5:
      break;
      stat->inspectCnt++;
    default:
      break;
  }
  return;
}

void initStatistics(ACTIVITY_STAT *stat) {
  stat->registerCnt = 0;
  stat->invokeCnt = 0;
  stat->unregisterCnt = 0;
  stat->inspectCnt = 0;
  stat->resultCnt = 0;
  return;
}

void showStatistics(ACTIVITY_STAT *stat) {
  printStr("register : ");
  printNum(stat->registerCnt);
  puts("");
  printStr("unregister : ");
  printNum(stat->unregisterCnt);
  puts("");
  printStr("invoke : ");
  printNum(stat->invokeCnt);
  puts("");
  printStr("result : ");
  printNum(stat->resultCnt);
  puts("");
  printStr("inspect : ");
  printNum(stat->inspectCnt);
  puts("");
  return;
}

uint64_t validateUser(USER *user) {
  //TODO_: currently no-op
  return SUCCESS;
}

uint64_t login(USER *user) {
  user->usernameLen = readNum();
  if (user->usernameLen >= sizeof(user->username)) return FAIL;
  user->passwordLen = readNum();
  if (user->passwordLen >= sizeof(user->password)) return FAIL;
  readSize(user->username, user->usernameLen);
  readSize(user->password, user->passwordLen);
  user->username[user->usernameLen] = '\0';
  user->password[user->passwordLen] = '\0';
  if (validateUser(user) == FAIL) return FAIL;
  initStatistics(&user->stat);
  return SUCCESS;
}

void displayUserInfo(USER *user) {
  printStr("username : ");
  puts(user->username);
  printStr("password : ");
  puts(user->password);
  showStatistics(&user->stat);
  return;
}

void logout(USER *user) {
  user->usernameLen = 0;
  user->passwordLen = 0;
  return;
}

void banner() {
  puts("                                                                  ");
  puts("                                                                  ");
  puts("                                                                  ");
  puts("                    /\\                                           ");
  puts("                    | \\                                          ");
  puts("                    |, |                                          ");
  puts("                    '|  \\\\                                      ");
  puts("                     \\'  |\\,____________                /\\     "); 
  puts("                     \\\\`===================`            \\/     "); 
  puts("                      \\\\'`====================`                 "); 
  puts("          /\\        '=`\\'`======================`               "); 
  puts("          \\/      '====`\\'`======================`              "); 
  puts("                 /======`''`======================`               ");
  puts("     . .       . .       . .    .       . .       . .       .     ");
  puts("  .+'|=|`+. .+'|=|`+. .+'|=|`+.=|`+. .+'|=|`+. .+'|=|`+. .+'|     ");
  puts("  |  | |  | |  | `+.| |.+' |  | `+.| |  | |  | |  | |  | |  |     ");
  puts("  |  |=|  | |  | .         |  |      |  |'. '. |  |=|  | |  |     ");
  puts("  |  | |  | `+.|=|`+.      |  |      |  | |  | |  | |  | |  |     ");
  puts("  |  | |  | .    |  |      |  |      |  | |  | |  | |  | |  |    .");
  puts("  |  | |  | |`+. |  |      |  |      |  | |  | |  | |  | |  | .+'|");
  puts("  `+.| |..| `+.|=|.+'      |.+'      `+.| |.+' `+.| |..| `+.|=|.+'");
  puts("                 \\==============`''`=============='              ");
  puts("                  `===============`\\'`==========='               "); 
  puts("                    `===============`\\'`========'                "); 
  puts("                      `===============`''`===='                   "); 
  puts("                         `=============`\\| '\\\\                 "); 
  puts("                   /\\        `\"\"\"\"\"\"\"\"'  \\|   \\        "); 
  puts("                   \\/                       \\  \\               "); 
  puts("                                              \\\\                "); 
  puts("                                                \\                "); 
  puts("                                                                  ");
  puts("                                                                  ");
  puts("                                                                  ");
  return;
}

void actionList() {
  puts("+----------------------------+");
  puts("| 1.  register applet        |");
  puts("| 2.  unregister applet      |");
  puts("| 3.  invoke applet          |");
  puts("| 4.  get invoke result      |");
  puts("| 5.  inspect applet storage |");
  puts("| 6.  show statistics        |");
  puts("| 7.  display user info      |");
  puts("| 8.  logout                 |");
  puts("| 9.  action list            |");
  puts("| 10. leave                  |");
  puts("+----------------------------+");
  return;
}

void registerApplet(ACTIVITY_STAT *stat) {
  APPLET_REGISTER_REQ req;
  APPLET_ID aid;
  req.applet.codeLen = readNum();
  if (req.applet.codeLen > APPLET_SIZE_MAX) {
    puts("applet size too large");
    return;
  }
  if ((req.applet.code = malloc(req.applet.codeLen)) == NULL) {
    abort("applet registration code allocation failed");
  }
  readSizeHex(req.applet.code, req.applet.codeLen);
  readSizeHex(req.userNonce, SIGNATURE_SIZE);
  readSizeHex(req.userPubkeyN, SIGNATURE_SIZE);
  readSizeHex(req.userPubkeyE, SIGNATURE_SIZE);
  readSizeHex(req.authoritySignature, SIGNATURE_SIZE);
  if (appletRegister(&req, &aid) == SYS_FAIL) {
    puts("applet registration failed");
  } else {
    printStr("registration succeeded, applet id : ");
    printNum(aid);
    puts("");
    recordStatistics(stat, 1);
  }
  free(req.applet.code);
  return;
}

void unregisterApplet(ACTIVITY_STAT *stat) {
  APPLET_UNREGISTER_REQ req;
  uint8_t output[DIGEST_SIZE * 2 + 1];
  req.id = readNum();
  readSizeHex(req.userSignature, SIGNATURE_SIZE);
  if (appletUnregister(&req) == SYS_FAIL) {
    puts("applet unregister failed");
  } else {
    printStr("unregister succeeded, applet id : ");
    printNum(req.id);
    puts("");
    recordStatistics(stat, 2);
  }
  return;
}

void invokeApplet(ACTIVITY_STAT *stat) {
  APPLET_INVOKE_REQ req;
  APPLET_RECEIPT receipt;
  req.id = readNum();
  req.arg.dataLen = readNum();
  if (req.arg.dataLen > APPLET_ARG_SIZE_MAX) {
    puts("applet arg too large");
    return;
  }
  if ((req.arg.data = malloc(req.arg.dataLen)) == NULL) {
    abort("applet invoke data allocation failed");
  }
  readSizeHex(req.arg.data, req.arg.dataLen);
  if (appletInvoke(&req, &receipt) == SYS_FAIL) {
    puts("applet invoke failed");
  } else {
    printStr("invoke succeeded, receipt : ");
    printNum(receipt.task);
    puts("");
    recordStatistics(stat, 3);
  }
  free(req.arg.data);
  return;
}

void inspectAppletStorage(ACTIVITY_STAT *stat) {
  APPLET_STORAGE_REQ req;
  APPLET_STORAGE storage;
  uint64_t schemaLen;
  uint8_t schema[APPLET_STORAGE_SIZE];
  uint8_t output[APPLET_STORAGE_SIZE * 2 + 1];
  req.id = readNum();
  schemaLen = readNum();
  if (schemaLen > APPLET_STORAGE_SIZE) {
    puts("invalid schema size");
  };
  //TODO_: schema under development, disable usage
  schemaLen = 0;
  if (schemaLen != 0) {
    readSizeHex(schema, schemaLen);
  }
  if (appletStorage(&req, &storage) == SYS_FAIL) {
    puts("applet view storage failed");
  } else {
    recordStatistics(stat, 5);
    printStr("storage : ");
    if (schemaLen == 0) {
      hexencode(storage.storage, APPLET_STORAGE_SIZE, output, APPLET_STORAGE_SIZE * 2);
      output[APPLET_STORAGE_SIZE * 2] = '\0';
      puts(output);
    } else {
      puts("");
      for (uint64_t schemaCursor = 0, storageCursor = 0; schemaCursor != schemaLen, storageCursor < APPLET_STORAGE_SIZE; schemaCursor++) {
        printStr("  ");
        printNum(storageCursor);
        switch (schema[schemaCursor]) {
          case 0:
            puts(" (spaceholder)");
            storageCursor++;
            break;
          case 1:
            printStr(" (bool) : ");
            if (storage.storage[storageCursor] == 0) {
              puts("true");
            } else {
              puts("false");
            }
            storageCursor++;
            break;
          case 2:
            printStr(" (u8) : ");
            printNum(storage.storage[storageCursor]);
            puts("");
            storageCursor++;
            break;
          case 3:
            if (storageCursor >= APPLET_STORAGE_SIZE - 2) return;
            printStr(" (u16) : ");
            printNum(*(uint16_t*)&storage.storage[storageCursor]);
            puts("");
            storageCursor += 2;
            break;
          case 4:
            if (storageCursor >= APPLET_STORAGE_SIZE - 4) return;
            printStr(" (u32) : ");
            printNum(*(uint32_t*)&storage.storage[storageCursor]);
            puts("");
            storageCursor += 4;
            break;
          case 5:
            if (storageCursor >= APPLET_STORAGE_SIZE - 8) return;
            printStr(" (u64) : ");
            printNum(*(uint64_t*)&storage.storage[storageCursor]);
            puts("");
            storageCursor += 8;
            break;
          case 6:
            if (schemaCursor >= schemaLen - 2) return;
            uint64_t length = schema[schemaCursor + 1];
            uint64_t elemSize = schema[schemaCursor + 2];
            if (length == 0 || elemSize == 0 || length * elemSize / elemSize != length) return;
            if (length * elemSize > APPLET_STORAGE_SIZE - storageCursor) return;
            schemaCursor += 2;
            printStr(" ([");
            printNum(elemSize);
            printStr(", ");
            printNum(length);
            printStr("]) : [");
            for (uint64_t elemCursor = 0; elemCursor < length; elemCursor++) {
              if (elemSize <= 8) {
                printNum((*(uint64_t*)&storage.storage[storageCursor]) << (8 - elemSize) >> (8 - elemSize));
              } else {
                hexencode(&storage.storage[storageCursor], elemSize, output, elemSize * 2);
                output[elemSize * 2] = '\0';
                printStr(output);
              }
              if (elemCursor == length - 1) {
                puts("]");
              } else {
                printStr(", ");
              }
              storageCursor += elemSize;
            }
            break;
          case 7:
            if (schemaCursor >= schemaLen - 1) return;
            length = schema[schemaCursor + 1];
            if (length == 0 || length > APPLET_STORAGE_SIZE - storageCursor) return;
            schemaCursor += 1;
            printStr(" (str) : ");
            printSize(&storage.storage[storageCursor], length);
            puts("");
            storageCursor += length;
            break;
          case 8:
            if (schemaCursor >= schemaLen - 1) return;
            length = schema[schemaCursor + 1];
            if (length == 0 || length > APPLET_STORAGE_SIZE - storageCursor) return;
            schemaCursor += 1;
            hexencode(&storage.storage[storageCursor], length, output, length * 2);
            output[length * 2] = '\0';
            printStr(" (bytes) : ");
            printStr(output);
            puts(output);
            storageCursor += length;
            break;
          case 9:
            printStr(" (char) : ");
            printSize(&storage.storage[storageCursor], 1);
            puts("");
            storageCursor++;
            break;
          default:
            return;
        }
      }
    }
  }
  return;
}

void checkAppletResult(ACTIVITY_STAT *stat) {
  APPLET_RECEIPT receipt;
  APPLET_RESULT result;
  uint8_t output[APPLET_RES_SIZE_MAX * 2 + 1];
  result.res.dataLen = APPLET_RES_SIZE_MAX;
  if ((result.res.data = malloc(result.res.dataLen)) == NULL) {
    abort("applet check result allocation failed");
  }
  receipt.task = readNum();
  if (appletResult(&receipt, &result) == SYS_FAIL) {
    puts("applet check result failed");
  } else {
    switch (result.status) {
      case APPLET_NOTFOUND:
        puts("task not found");
        break;
      case APPLET_PENDING:
        puts("task still pending");
        break;
      case APPLET_PROCESSING:
        puts("task still running");
        break;
      case APPLET_DONE:
        puts("task finished");
        printStr("output : ");
        hexencode(result.res.data, result.res.dataLen, output, result.res.dataLen * 2);
        output[result.res.dataLen * 2] = '\0';
        puts(output);
        recordStatistics(stat, 4);
        break;
      default:
        abort("unknow result");
        break;
    }
  }
  free(result.res.data);
  return;
}

void __attribute__((noreturn)) userMain() {
  uint64_t logined = FAIL;
  USER user;
  banner();

  while (1) {
    if (logined == FAIL) {
      if ((logined = login(&user)) == SUCCESS) {
        actionList();
      }
    }
    if (logined == SUCCESS) {
      switch(readNum()) {
        case 1:
          registerApplet(&user.stat);
          break;
        case 2:
          unregisterApplet(&user.stat);
          break;
        case 3:
          invokeApplet(&user.stat);
          break;
        case 4:
          checkAppletResult(&user.stat);
          break;
        case 5:
          inspectAppletStorage(&user.stat);
          break;
        case 6:
          showStatistics(&user.stat);
          break;
        case 7:
          displayUserInfo(&user);
          break;
        case 8:
          logout(&user);
          logined = FAIL;
          break;
        case 10:
          exit(0);
        case 9:
        default:
          actionList();
          break;
      }
    }
  }
  exit(0);
}
