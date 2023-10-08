#include "applet.h"

S_APPLET_STATE g_applet;

uint64_t initAppletStorage() {
  uint8_t appletDigest[DIGEST_SIZE];
  for (uint64_t i = 0; i <= APPLET_CNT_MAX + APPLET_NATIVE_CNT_MAX; i++) {
    g_applet.applets[i].id = APPLET_NIL;
  }
  for (uint64_t i = 0; i <= APPLET_TASK_CNT_MAX; i++) {
    g_applet.tasks[i].idx = APPLET_IDX_NIL;
  }
  //register native applets
  if (digestGenerateHelper(12, "builtin-time", NULL, NULL, NULL, appletDigest) == FAIL) return FAIL;
  g_applet.applets[APPLET_CNT_MAX].id = *((APPLET_ID*)appletDigest);
  g_applet.applets[APPLET_CNT_MAX].nativeFn = appletBuiltinTime;
  if (digestGenerateHelper(12, "builtin-rand", NULL, NULL, NULL, appletDigest) == FAIL) return FAIL;
  g_applet.applets[APPLET_CNT_MAX + 1].id = *((APPLET_ID*)appletDigest);
  g_applet.applets[APPLET_CNT_MAX + 1].nativeFn = appletBuiltinRand;
  if (digestGenerateHelper(25, "builtin-validate-preimage", NULL, NULL, NULL, appletDigest) == FAIL) return FAIL;
  g_applet.applets[APPLET_CNT_MAX + 2].id = *((APPLET_ID*)appletDigest);
  g_applet.applets[APPLET_CNT_MAX + 2].nativeFn = appletBuiltinValidatePreimage;
  if (digestGenerateHelper(12, "builtin-flag", NULL, NULL, NULL, appletDigest) == FAIL) return FAIL;
  g_applet.applets[APPLET_CNT_MAX + 3].id = *((APPLET_ID*)appletDigest);
  g_applet.applets[APPLET_CNT_MAX + 3].nativeFn = appletBuiltinFlag;
  return SUCCESS;
}

uint64_t findAppletIdx(APPLET_ID id, uint64_t *idx) {
  if (id == APPLET_NIL) return FAIL;
  for (uint64_t i = 0; i < APPLET_CNT_MAX + APPLET_NATIVE_CNT_MAX; i++) {
    if (g_applet.applets[i].id == id) {
      if (idx != NULL) {
        *idx = i;
      }
      return SUCCESS;
    }
  }
  return FAIL;
}

uint64_t digestGenerateHelper(uint64_t codeLen, uint8_t *code, uint8_t *n, uint8_t *e, uint8_t *nonce, uint8_t *digest) {
  uint8_t payload[DIGEST_PAYLOAD_SIZE_MAX];
  if (n != NULL) {
    memcpy((uint64_t)payload, (uint64_t)n, SIGNATURE_SIZE);
  } else {
    memset((uint64_t)payload, '\0', SIGNATURE_SIZE);
  }
  if (e != NULL) {
    memcpy((uint64_t)&payload[SIGNATURE_SIZE], (uint64_t)e, SIGNATURE_SIZE);
  } else {
    memset((uint64_t)&payload[SIGNATURE_SIZE], '\0', SIGNATURE_SIZE);
  }
  if (nonce != NULL) {
    memcpy((uint64_t)&payload[SIGNATURE_SIZE * 2], (uint64_t)nonce, SIGNATURE_SIZE);
  } else {
    memset((uint64_t)&payload[SIGNATURE_SIZE * 2], '\0', SIGNATURE_SIZE);
  }
  memcpy((uint64_t)&payload[SIGNATURE_SIZE * 3], (uint64_t)code, codeLen);
  if (hp_digestGenerate(SIGNATURE_SIZE * 3 + codeLen, payload, digest) == FAIL) return FAIL;
  return SUCCESS;
}

uint64_t kAppletRegister(APPLET_REGISTER_REQ *req, APPLET_ID *id) {
  uint64_t codeVaddr, storageVaddr, appletId, spareSlot = -1;
  uint8_t appletDigest[DIGEST_SIZE];
  // check spare slot in applet list
  for (uint64_t i = 0; i < APPLET_CNT_MAX; i++) {
    if (g_applet.applets[i].id == APPLET_NIL) {
      spareSlot = i;
      break;
    }
  }
  if (spareSlot == -1) return FAIL;
  // generate appletId
  if (digestGenerateHelper(req->applet.codeLen, req->applet.code, req->userPubkeyN, req->userPubkeyE, req->userNonce, appletDigest) == FAIL) return FAIL;
  if (*(APPLET_ID*)appletDigest == APPLET_NIL) return FAIL;
  *id = *((APPLET_ID*)appletDigest);
  // check if applet already exists
  if (findAppletIdx(*id, NULL) == SUCCESS) return FAIL;
  // forward to processor for signature check
  if (hp_appletRegisterValidate(req->applet.codeLen, req->applet.code, req->authoritySignature) == FAIL) return FAIL;
  // allocate memory for code / signature / storage
  if (searchFreeVrange(g_runtimeContext.kernelMmapBase, KERN_PAGE_MIN, PAGE_UPALIGN(req->applet.codeLen), true, &codeVaddr) == FAIL) {
    if (searchFreeVrange(g_runtimeContext.kernelMmapBase, KERN_PAGE_MAX, PAGE_UPALIGN(req->applet.codeLen), false, &codeVaddr) == FAIL) {
      return FAIL;
    }
  }
  if (allocateVrange(codeVaddr, PAGE_UPALIGN(req->applet.codeLen), false, true) == FAIL) return FAIL;
  if (searchFreeVrange(g_runtimeContext.kernelMmapBase, KERN_PAGE_MIN, APPLET_STORAGE_SIZE, true, &storageVaddr) == FAIL) {
    if (searchFreeVrange(g_runtimeContext.kernelMmapBase, KERN_PAGE_MAX, APPLET_STORAGE_SIZE, false, &storageVaddr) == FAIL) {
      deallocateVrange(codeVaddr, PAGE_UPALIGN(req->applet.codeLen), false);
      return FAIL;
    }
  }
  if (allocateVrange(storageVaddr, APPLET_STORAGE_SIZE, false, true) == FAIL) {
    deallocateVrange(codeVaddr, PAGE_UPALIGN(req->applet.codeLen), false);
    return FAIL;
  }
  //insert entry
  g_applet.applets[spareSlot].codeLen = req->applet.codeLen;
  g_applet.applets[spareSlot].taskCnt = 0;
  g_applet.applets[spareSlot].code = (uint8_t*)codeVaddr;
  g_applet.applets[spareSlot].storage = (uint8_t*)storageVaddr;
  memcpy((uint64_t)codeVaddr, (uint64_t)req->applet.code, req->applet.codeLen);
  memcpy((uint64_t)g_applet.applets[spareSlot].userNonce, (uint64_t)req->userNonce, SIGNATURE_SIZE);
  memcpy((uint64_t)g_applet.applets[spareSlot].userPubkeyN, (uint64_t)req->userPubkeyN, SIGNATURE_SIZE);
  memcpy((uint64_t)g_applet.applets[spareSlot].userPubkeyE, (uint64_t)req->userPubkeyE, SIGNATURE_SIZE);
  memcpy((uint64_t)g_applet.applets[spareSlot].authoritySignature, (uint64_t)req->authoritySignature, SIGNATURE_SIZE);
  g_applet.applets[spareSlot].id = *id;
  return SUCCESS;
}

uint64_t kAppletUnregister(APPLET_UNREGISTER_REQ *req) {
  uint64_t appletIdx;
  uint8_t appletDigest[DIGEST_SIZE];
  //check if req exist in applet list
  if (findAppletIdx(req->id, &appletIdx) == FAIL) return FAIL;
  if (appletIdx >= APPLET_CNT_MAX) return FAIL;
  if (g_applet.applets[appletIdx].taskCnt != 0) return FAIL;
  //decrypt signature to check if it matches digest(nonce + code)
  if (digestGenerateHelper(
        g_applet.applets[appletIdx].codeLen,
        g_applet.applets[appletIdx].code,
        g_applet.applets[appletIdx].userPubkeyN,
        g_applet.applets[appletIdx].userPubkeyE,
        g_applet.applets[appletIdx].userNonce,
        appletDigest
  ) == FAIL) {
    return FAIL;
  }
  if (hp_signatureValidate(
        appletDigest,
        g_applet.applets[appletIdx].userPubkeyN,
        g_applet.applets[appletIdx].userPubkeyE,
        req->userSignature
  ) == FAIL) {
    return FAIL;
  }
  //remove req entry from list
  g_applet.applets[appletIdx].id = APPLET_NIL;
  //release code / storage buffer 
  deallocateVrange((uint64_t)g_applet.applets[appletIdx].code, PAGE_UPALIGN(g_applet.applets[appletIdx].codeLen), false);
  g_applet.applets[appletIdx].code = NULL;
  deallocateVrange((uint64_t)g_applet.applets[appletIdx].storage, APPLET_STORAGE_SIZE, false);
  g_applet.applets[appletIdx].storage = NULL;
  return SUCCESS;
}

uint64_t kAppletInvokeUtil(APPLET_TASK_ID task) {
  uint64_t invokeRes;
  APPLET_ID caller = APPLET_NIL;
  if (g_applet.tasks[task].caller != TASK_NIL) {
    caller = g_applet.applets[g_applet.tasks[g_applet.tasks[task].caller].idx].id;
  }
  if ((invokeRes = hp_appletInvoke(
                     caller,
                     task,
                     g_applet.tasks[task].codeLen,
                     g_applet.tasks[task].code,
                     g_applet.tasks[task].authoritySignature,
                     g_applet.tasks[task].argLen,
                     g_applet.tasks[task].arg,
                     g_applet.tasks[task].storage
                   )
  ) == HP_APPLET_PROCESSOR_REJECT) {
    //this should never happen since kernel only registers validated applets
    deallocateVrange((uint64_t)g_applet.tasks[task].arg, APPLET_ARG_SIZE_MAX, false);
    g_applet.tasks[task].arg = NULL;
    APPLET_RECEIPT receipt = {.task = task};
    kAppletRecycle(&receipt);
    return FAIL;
  } else if (invokeRes == HP_APPLET_PROCESSOR_BUSY) {
    //mark it as pending to allow processor to fetch this task when ready
    g_applet.tasks[task].status = APPLET_PENDING;
  } else {
    g_applet.tasks[task].status = APPLET_PROCESSING;
    deallocateVrange((uint64_t)g_applet.tasks[task].arg, APPLET_ARG_SIZE_MAX, false);
    g_applet.tasks[task].arg = NULL;
  }
  return SUCCESS;
}

uint64_t kAppletInvoke(APPLET_INVOKE_REQ *req, APPLET_RECEIPT *receipt, APPLET_TASK_ID caller) {
  uint64_t appletIdx, argVaddr, resVaddr, invokeRes, spareSlot = -1;
  //check if req exist in applet list
  if (findAppletIdx(req->id, &appletIdx) == FAIL) return FAIL;
  if (appletIdx >= APPLET_CNT_MAX && caller == TASK_NIL) return FAIL;
  //check if task queue is full
  for (uint64_t i = 0; i <= APPLET_TASK_CNT_MAX; i++) {
    if (g_applet.tasks[i].idx == APPLET_IDX_NIL) {
      spareSlot = i;
      break;
    }
  }
  if (spareSlot == -1) return FAIL;
  //insert to task queue
  if (appletIdx < APPLET_CNT_MAX) {
    if (getPhysAddr((uint64_t)g_applet.applets[appletIdx].storage, PDE64_RW, &g_applet.tasks[spareSlot].storage) == FAIL ||
        getPhysAddr((uint64_t)g_applet.applets[appletIdx].code, 0, &g_applet.tasks[spareSlot].code) == FAIL ||
        getPhysAddr((uint64_t)g_applet.applets[appletIdx].authoritySignature, 0, &g_applet.tasks[spareSlot].authoritySignature) == FAIL 
    ) {
      return FAIL;
    }
    g_applet.tasks[spareSlot].codeLen = g_applet.applets[appletIdx].codeLen;
  }
  if (searchFreeVrange(g_runtimeContext.kernelMmapBase, KERN_PAGE_MIN, APPLET_ARG_SIZE_MAX, true, &argVaddr) == FAIL) {
    if (searchFreeVrange(g_runtimeContext.kernelMmapBase, KERN_PAGE_MAX, APPLET_ARG_SIZE_MAX, false, &argVaddr) == FAIL) {
      return FAIL;
    }
  }
  if (allocateVrange(argVaddr, APPLET_ARG_SIZE_MAX, false, true) == FAIL) return FAIL;
  if (searchFreeVrange(g_runtimeContext.kernelMmapBase, KERN_PAGE_MIN, APPLET_RES_SIZE_MAX, true, &resVaddr) == FAIL) {
    if (searchFreeVrange(g_runtimeContext.kernelMmapBase, KERN_PAGE_MAX, APPLET_RES_SIZE_MAX, false, &resVaddr) == FAIL) {
      deallocateVrange(argVaddr, APPLET_ARG_SIZE_MAX, false);
      return FAIL;
    }
  }
  if (allocateVrange(resVaddr, APPLET_RES_SIZE_MAX, false, true) == FAIL) {
    deallocateVrange(argVaddr, APPLET_ARG_SIZE_MAX, false);
    return FAIL;
  }
  memcpy(argVaddr, (uint64_t)req->arg.data, req->arg.dataLen);
  g_applet.applets[appletIdx].taskCnt++;
  g_applet.tasks[spareSlot].idx = appletIdx;
  g_applet.tasks[spareSlot].caller = caller;
  g_applet.tasks[spareSlot].status = APPLET_DONE;
  g_applet.tasks[spareSlot].argLen = req->arg.dataLen;
  g_applet.tasks[spareSlot].arg = (uint8_t*)argVaddr;
  g_applet.tasks[spareSlot].resLen = APPLET_RES_SIZE_MAX;
  g_applet.tasks[spareSlot].res = (uint8_t*)resVaddr;
  g_applet.tasks[spareSlot].context.memory = NULL;
  g_applet.tasks[spareSlot].callRes = NULL;
  g_applet.tasks[spareSlot].callResLen = 0;
  if (appletIdx < APPLET_CNT_MAX) {
    //send to processor
    if (kAppletInvokeUtil(spareSlot) == FAIL) return FAIL;
  } else {
    g_applet.applets[appletIdx].nativeFn(spareSlot, &req->arg);
    deallocateVrange(argVaddr, APPLET_ARG_SIZE_MAX, false);
    kAppletResume(caller, spareSlot);
    APPLET_RECEIPT receipt = {.task = spareSlot};
    kAppletRecycle(&receipt);
  }
  //return task id
  if (receipt != NULL) {
    receipt->task = spareSlot;
  }
  return SUCCESS;
}

uint64_t kAppletResult(APPLET_RECEIPT *receipt, APPLET_RESULT *result) {
  uint64_t resSize;
  //check if in result list
  if (receipt->task > APPLET_TASK_CNT_MAX) return FAIL;
  if (g_applet.tasks[receipt->task].idx == APPLET_IDX_NIL) {
    result->status = APPLET_NOTFOUND;
    return SUCCESS;
  }
  if (g_applet.tasks[receipt->task].status == APPLET_PENDING || g_applet.tasks[receipt->task].status == APPLET_PROCESSING) {
    result->status = g_applet.tasks[receipt->task].status;
    return SUCCESS;
  }
  //shouldn't happen, just in case
  if (g_applet.tasks[receipt->task].status != APPLET_DONE) return FAIL; 
  result->status = APPLET_DONE;
  if (result->res.dataLen > g_applet.tasks[receipt->task].resLen) {
    result->res.dataLen = g_applet.tasks[receipt->task].resLen;
  }
  memcpy((uint64_t)result->res.data, (uint64_t)g_applet.tasks[receipt->task].res, result->res.dataLen);
  return SUCCESS;
}

uint64_t kAppletRecycle(APPLET_RECEIPT *receipt) {
  if (receipt->task > APPLET_TASK_CNT_MAX) return FAIL;
  if (g_applet.tasks[receipt->task].idx == APPLET_IDX_NIL) return FAIL;
  if (g_applet.tasks[receipt->task].res != NULL) {
    deallocateVrange((uint64_t)g_applet.tasks[receipt->task].res, APPLET_RES_SIZE_MAX, false);
  }
  g_applet.applets[g_applet.tasks[receipt->task].idx].taskCnt--;
  g_applet.tasks[receipt->task].idx = APPLET_IDX_NIL;
  return SUCCESS;
}
  
uint64_t kAppletStorage(APPLET_STORAGE_REQ *req, APPLET_STORAGE *res) {
  uint64_t appletIdx;
  if (findAppletIdx(req->id, &appletIdx) == FAIL) return FAIL;
  if (appletIdx >= APPLET_CNT_MAX) return FAIL;
  memcpy((uint64_t)res->storage, (uint64_t)g_applet.applets[appletIdx].storage, APPLET_STORAGE_SIZE);
  return SUCCESS;
}

uint64_t kAppletResume(APPLET_TASK_ID caller, APPLET_TASK_ID callee) {
  uint64_t appletResumeRes;
  if (callee != TASK_NIL) {
    g_applet.tasks[caller].callRes = g_applet.tasks[callee].res;
    g_applet.tasks[caller].callResLen = g_applet.tasks[callee].resLen;
    g_applet.tasks[callee].res = NULL;
  }
  if ((appletResumeRes = hp_appletResume(
                           caller,
                           &g_applet.tasks[caller].context,
                           g_applet.tasks[caller].callResLen,
                           g_applet.tasks[caller].callRes
  )) == HP_APPLET_PROCESSOR_REJECT) {
    //this should never happen since kernel does not tamper with cached context
    APPLET_TASK_ID curTask = caller;
    while (curTask != TASK_NIL) {
      if (g_applet.tasks[curTask].callRes != NULL) {
        deallocateVrange((uint64_t)g_applet.tasks[curTask].callRes, APPLET_RES_SIZE_MAX, false);
        g_applet.tasks[curTask].callRes = NULL;
      }
      deallocateVrange((uint64_t)g_applet.tasks[curTask].context.memory, APPLET_CONTEXT_MEMORY_SIZE, false);
      g_applet.tasks[curTask].context.memory = NULL;
      APPLET_RECEIPT receipt = {.task = curTask};
      curTask = g_applet.tasks[curTask].caller;
      kAppletRecycle(&receipt);
    }
    return FAIL;
  } else if (appletResumeRes == HP_APPLET_PROCESSOR_BUSY) {
    //mark it as pending to allow processor to fetch this task when ready
    g_applet.tasks[caller].status = APPLET_PENDING;
  } else {
    //the applet is resumed, we can free our context and callRes
    g_applet.tasks[caller].status = APPLET_PROCESSING;
    if (g_applet.tasks[caller].callRes != NULL) {
      deallocateVrange((uint64_t)g_applet.tasks[caller].callRes, APPLET_RES_SIZE_MAX, false);
      g_applet.tasks[caller].callRes = NULL;
    }
    deallocateVrange((uint64_t)g_applet.tasks[caller].context.memory, APPLET_CONTEXT_MEMORY_SIZE, false);
    g_applet.tasks[caller].context.memory = NULL;
  }
  return SUCCESS;
}

void kAppletInterrupt(uint8_t type, uint8_t *req) {
  APPLET_INVOKE_REQ invokeReq;
  uint64_t contextVaddr;
  if (type == APPLET_INVOKE_INTERRUPT) {
    HYPER_APPLET_CONTEXT *appletContext = (HYPER_APPLET_CONTEXT*)req;
    if (appletContext->task > APPLET_TASK_CNT_MAX ||
        g_applet.tasks[appletContext->task].idx == APPLET_IDX_NIL ||
        g_applet.tasks[appletContext->task].idx >= APPLET_CNT_MAX ||
        g_applet.tasks[appletContext->task].status != APPLET_PROCESSING
    ) {
      goto NEXTTASK;
    }
    //snapshot applet state
    if (searchFreeVrange(g_runtimeContext.kernelMmapBase, KERN_PAGE_MIN, APPLET_CONTEXT_MEMORY_SIZE, true, &contextVaddr) == FAIL) {
      if (searchFreeVrange(g_runtimeContext.kernelMmapBase, KERN_PAGE_MAX, APPLET_CONTEXT_MEMORY_SIZE, false, &contextVaddr) == FAIL) {
        goto NEXTTASK;
      }
    }
    if (allocateVrange(contextVaddr, APPLET_CONTEXT_MEMORY_SIZE, false, true) == FAIL) goto NEXTTASK;
    memcpy((uint64_t)contextVaddr, (uint64_t)&appletContext->memory, APPLET_CONTEXT_MEMORY_SIZE);
    memcpy((uint64_t)g_applet.tasks[appletContext->task].context.regs, (uint64_t)&appletContext->regs, sizeof(uint64_t) * APPLET_REG_CNT);
    g_applet.tasks[appletContext->task].context.memory = (uint8_t*)contextVaddr;
    //cross applet invoke
    invokeReq.id = g_applet.tasks[appletContext->task].context.regs[0];
    invokeReq.arg.dataLen = g_applet.tasks[appletContext->task].context.regs[1];
    invokeReq.arg.data = (uint8_t*)g_applet.tasks[appletContext->task].context.regs[2];
    if (invokeReq.arg.dataLen > APPLET_ARG_SIZE_MAX || 
        (APPLET_SEG_OFFSET(invokeReq.arg.dataLen) + APPLET_SEG_OFFSET(invokeReq.arg.data) > APPLET_SEG_SIZE_MAX) ||
        (uint64_t)invokeReq.arg.data >= APPLET_ADDR_MAX
    ) {
      g_applet.tasks[appletContext->task].callResLen = 0;
      g_applet.tasks[appletContext->task].callRes = "";
      if (kAppletResume(appletContext->task, TASK_NIL) == FAIL) goto NEXTTASK;
      return;
    }
    invokeReq.arg.data = &g_applet.tasks[appletContext->task].context.memory[
      APPLET_SEG_IDX(invokeReq.arg.data) * APPLET_SEG_SIZE_MAX + APPLET_SEG_OFFSET(invokeReq.arg.data)
    ];
    //set caller status to pending
    g_applet.tasks[appletContext->task].status = APPLET_PENDING;
    if (kAppletInvoke(&invokeReq, NULL, appletContext->task) == FAIL) {
      if (kAppletResume(appletContext->task, TASK_NIL) == FAIL) goto NEXTTASK;
      return;
    }
    return;
  } else if (type == APPLET_RES_INTERRUPT) {
    HYPER_APPLET_RES *appletRes = (HYPER_APPLET_RES*)req;
    if (appletRes->task > APPLET_TASK_CNT_MAX ||
        g_applet.tasks[appletRes->task].idx == APPLET_IDX_NIL ||
        g_applet.tasks[appletRes->task].idx >= APPLET_CNT_MAX ||
        g_applet.tasks[appletRes->task].status != APPLET_PROCESSING
    ) {
      goto NEXTTASK;
    }
    //collect result + commit storage changes
    if (appletRes->resLen > APPLET_RES_SIZE_MAX) {
      appletRes->resLen = 0;
    }
    memcpy((uint64_t)g_applet.tasks[appletRes->task].res, (uint64_t)appletRes->res, appletRes->resLen);
    memcpy(g_applet.tasks[appletRes->task].storage, (uint64_t)appletRes->storage, APPLET_STORAGE_SIZE);
    g_applet.tasks[appletRes->task].resLen = appletRes->resLen;
    if (g_applet.tasks[appletRes->task].caller != TASK_NIL) {
      if (g_applet.tasks[g_applet.tasks[appletRes->task].caller].idx == APPLET_IDX_NIL) goto NEXTTASK;
      //this is an applet invoke, set return value for caller usage
      g_applet.tasks[g_applet.tasks[appletRes->task].caller].callRes = g_applet.tasks[appletRes->task].res;
      g_applet.tasks[g_applet.tasks[appletRes->task].caller].callResLen = g_applet.tasks[appletRes->task].resLen;
      g_applet.tasks[appletRes->task].res = NULL;
      //cleanup callee task
      APPLET_RECEIPT receipt = {.task = appletRes->task};
      kAppletRecycle(&receipt);
    } else {
      //this is an outermost call, set status to prepare for user query
      g_applet.tasks[appletRes->task].status = APPLET_DONE;
    }
NEXTTASK:
    //search for next task to run
    for (uint64_t i = 0; i <= APPLET_TASK_CNT_MAX; i++) {
      if (g_applet.tasks[i].idx != APPLET_IDX_NIL && g_applet.tasks[i].status == APPLET_PENDING) {
        if (g_applet.tasks[i].context.memory == NULL) {
          if (kAppletInvokeUtil(i) == FAIL) continue;
          break;
        } else if (g_applet.tasks[i].callRes != NULL) {
          if (kAppletResume(i, TASK_NIL)) continue;
          break;
        }
      }
    }
  }
  return;
}

/* native */
uint64_t appletBuiltinTime(APPLET_TASK_ID task, APPLET_INPOUT *arg) {
  uint64_t timestamp;
  hp_time(&timestamp);
  g_applet.tasks[task].resLen = sizeof(uint64_t);
  *((uint64_t*)(g_applet.tasks[task].res)) = timestamp;
  return SUCCESS;
}

uint64_t appletBuiltinRand(APPLET_TASK_ID task, APPLET_INPOUT *arg) {
  uint64_t rand;
  hp_rand(&rand);
  g_applet.tasks[task].resLen = sizeof(uint64_t);
  *((uint64_t*)(g_applet.tasks[task].res)) = rand;
  return SUCCESS;
}

uint64_t appletBuiltinValidatePreimage(APPLET_TASK_ID task, APPLET_INPOUT *arg) {
  uint16_t status;
  uint8_t digest[DIGEST_SIZE];
  if (arg->dataLen < APPLET_NONCE_SIZE * 2) {
    status = 0xffff;
  } else {
    hp_digestGenerate(APPLET_NONCE_SIZE, &arg->data[APPLET_NONCE_SIZE], digest);
    if (memcmp((uint64_t)digest, (uint64_t)arg->data, APPLET_NONCE_SIZE) == SUCCESS) {
      status = 1;
    } else {
      status = 0;
    }
  }
  g_applet.tasks[task].resLen = sizeof(uint16_t);
  *((uint16_t*)(g_applet.tasks[task].res)) = status;
  return SUCCESS;
}

uint64_t appletBuiltinFlag(APPLET_TASK_ID task, APPLET_INPOUT *arg) {
  hp_appletspaceFlag();
  g_applet.tasks[task].resLen = 0;
  return SUCCESS;
}

