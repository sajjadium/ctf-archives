BITS 64
global _start

%define CODE 1

;define constants
;memory management constants
%define MEMMIN 0x600000000000
%define MEMMAX 0x700000000000
%define PAGESIZE 0x1000
%define PAGEMASK 0xffff

;syscall constants
%define SYSCALLFAIL 0xffffffffffffffff

;meta constants
%define CONFRONT_STATE_ADDR 0x600000000000
%define WEAPON_MEM_POOL 0x610000000000
%define MAX_WEAPON_IDX 200
%define WEAPON_ARRAY_SIZE 0xc80

%define SLOT_NONE 0xffffffffffffffff
%define MAX_NAME_LEN 0x100
%define MAX_DESC_LEN 0x100

%define STAGE_MIN 0
%define STAGE_MAX 2000
%define LOC_NONE 0xffffffffffffffff

;action constants
%define IDLE 0x00
%define STARTBATTLE 0x01
%define RETREAT 0x02
%define CRAFTWEAPON 0x03
%define SWITCHWEAPON 0x04
%define ENHANCEWEAPON 0x05
%define DISPOSEWEAPON 0x06
%define ATTACK 0x07
%define DEFEND 0x08
%define MOVE 0x09
%define GIVEUP 0xff

;interaction constants
%define STATE_NONE 0
%define ATTACK_SET 0x10
%define ATTACK_CLEAR_MASK 0xffffffffffffff00
%define STATE_ATTACKHIGH_LEFT 0x10
%define STATE_ATTACKHIGH_RIGHT 0x11
%define STATE_ATTACKMIDDLE_LEFT 0x12
%define STATE_ATTACKMIDDLE_RIGHT 0x13
%define STATE_ATTACKLOW_LEFT 0x14
%define STATE_ATTACKLOW_RIGHT 0x15

%define DEFEND_SHIFT 8
%define DEFEND_SET 0x1000
%define DEFEND_CLEAR_MASK 0xffffffffffff00ff
%define STATE_DEFENDHIGH 0x1000
%define STATE_DEFENDMIDDLE 0x1100
%define STATE_DEFENDLOW 0x1200

%define NOT_UNDER_ATTACK 0xffffffffffffffff

;movement constants
%define MOVE_SHIFT 0x10
%define MOVE_SET 0x100000
%define MOVE_CLEAR_MASK 0xffffffffff00ffff
%define MOVE_LEFT 0x100000
%define MOVE_RIGHT 0x110000

;attribute constants
%define ATTR_FIRE 0x1
%define ATTR_ICE 0x2
%define ATTR_LIGHT 0x4
%define ATTR_DARKNESS 0x8
%define ATTR_NONE 0xf

;cooldown constants
%define ADVENTURER_BAREHANDED_COOLDOWN 3
%define ADVENTURER_MOVE_COOLDOWN 5

;initial constants
%define UNICORN_INIT_LOC 200
%define ADVENTURER_INIT_HP 800
%define ADVENTURER_INIT_ATTACK 11
%define ADVENTURER_INIT_DEFENSE 5
%define ADVENTURER_INIT_LOC 1800

;character constants
%define UNICORN_SIZE 200
%define UNICORN_HALF_SIZE 100
%define ADVENTURER_SIZE 80
%define ADVENTURER_HALF_SIZE 40

%define BAREHANDED_DELTA 40
%define BAREHANDED_RANGE 80
%define ADVENTURER_DEFENSE_GAUGE 10
%define BAREHANDED_MOVE_SPEED 40
%define UNICORN_MOVE_SPEED 50
%define UNICORN_DESIRED_DISTANCE 150

;unicorn stage constants
%define UNICORN_STAGE1 0
%define UNICORN_STAGE1_HP 10000
%define UNICORN_STAGE1_ATTACK 10
%define UNICORN_STAGE1_DEFENSE 10
%define UNICORN_STAGE1_DEFENSE_GAUGE 10
%define UNICORN_STAGE1_CD 10
%define UNICORN_STAGE1_ATTRIBUTE ATTR_NONE
%define UNICORN_STAGE1_DELTA 20
%define UNICORN_STAGE1_RANGE 400
%define UNICORN_STAGE2 1
%define UNICORN_STAGE2_HP 6000
%define UNICORN_STAGE2_ATTACK 100
%define UNICORN_STAGE2_DEFENSE 100
%define UNICORN_STAGE2_DEFENSE_GAUGE 100
%define UNICORN_STAGE2_ATTRIBUTE 0xc
%define UNICORN_STAGE2_CD 10
%define UNICORN_STAGE2_DELTA 40
%define UNICORN_STAGE2_RANGE 800
%define UNICORN_STAGE3 2
%define UNICORN_STAGE3_HP 3000
%define UNICORN_STAGE3_ATTACK 500
%define UNICORN_STAGE3_DEFENSE 1000
%define UNICORN_STAGE3_DEFENSE_GAUGE 1000
%define UNICORN_STAGE3_ATTRIBUTE 0
%define UNICORN_STAGE3_DELTA 80
%define UNICORN_STAGE3_RANGE 1600
%define UNICORN_STAGE3_CD 5

;weapon constants
%define WEAPON_MAX_LEVEL 5

;define structures
struc confrontState
  .unicornRand resq 1
  .isConfront resq 1
  .unicornStage resq 1
  .unicornHP resq 1
  .unicornAttack resq 1
  .unicornDefense resq 1
  .unicornState resq 1
  .unicornAttribute resq 1
  .unicornCD resq 1
  .unicornDefenseGauge resq 1
  .unicornLoc resq 1
  .unicornAttackSourceLoc resq 1
  .unicornAttackBoxLoc resq 1
  .adventurerHP resq 1
  .adventurerAttack resq 1
  .adventurerDefense resq 1
  .adventurerState resq 1
  .adventurerCD resq 1
  .adventurerDefenseGauge resq 1
  .adventurerLoc resq 1
  .adventurerAttackSourceLoc resq 1
  .adventurerAttackBoxLoc resq 1
  .adventurerWeaponIdx resq 1
  .adventurerName resb MAX_NAME_LEN
  .adventurerDesc resb MAX_DESC_LEN
  .adventurerWeapons resq MAX_WEAPON_IDX
endstruc

struc weaponEntry
  .ptr resq 1
  .size resq 1
endstruc

struc weapon
  .level resq 1
  .attack resq 1
  .defense resq 1
  .attribute resq 1
  .CD resq 1
  .range resq 1
  .delta resq 1
  .movespeed resq 1
  .name resb MAX_NAME_LEN
  .desc resb MAX_DESC_LEN
endstruc

struc actionStruct
  .action resq 1
  .union resb 0x278
endstruc

struc startBattleStruct
  .namelen resq 1
  .desclen resq 1
  .name resb MAX_NAME_LEN
  .desc resb MAX_DESC_LEN
endstruc

struc craftWeaponStruct
  .namelen resq 1
  .desclen resq 1
  .attack resq 1
  .defense resq 1
  .attribute resq 1
  .CD resq 1
  .range resq 1
  .delta resq 1
  .movespeed resq 1
  .name resb MAX_NAME_LEN
  .desc resb MAX_DESC_LEN
endstruc

struc switchWeaponStruct
  .targetIdx resq 1
endstruc

struc enhanceWeaponStruct
endstruc

struc disposeWeaponStruct
  .targetIdx resq 1
endstruc

struc attackStruct
  .level resq 1
endstruc

struc defendStruct
  .level resq 1
endstruc

struc moveStruct
  .direction resq 1
endstruc

;each function have a macro to allow writing concise code
%macro return 0
  jmp epilogue
%endmacro

%macro callFunc 1
  lea r10, [rel %1]
  call prologue
%endmacro

%macro exit 1
  mov rdi, %1
  callFunc _exit
%endmacro

%macro mmap 3
  mov rdx, %3
  mov rsi, %2
  mov rdi, %1
  callFunc _mmap
%endmacro

%macro munmap 2
  mov rsi, %2
  mov rdi, %1
  callFunc _munmap
%endmacro

%macro read 3
  mov rdx, %3
  lea rsi, %2
  mov rdi, %1
  callFunc _read
%endmacro

%macro write 3
  mov rdx, %3
  lea rsi, %2
  mov rdi, %1
  callFunc _write
%endmacro

%macro getMem 0
  mmap dr1, PAGESIZE, 3
  mov rdi, dr1
  add rdi, PAGESIZE
  mov dr1, rdi
%endmacro

%macro memset 3
  mov rdx, %3
  xor rsi, rsi
  mov sil, %2
  lea rdi, %1
  callFunc _memset
%endmacro

%macro memcpy 3
  mov rdx, %3
  lea rsi, %2
  lea rdi, %1
  callFunc _memcpy
%endmacro

%macro unicornRandNext 2
  mov rsi, %2
  mov rdi, %1
  callFunc _unicornRandNext
%endmacro

%macro isUnicornUnderAttack 1
  mov rdi, %1
  callFunc _isUnicornUnderAttack
%endmacro

%macro isAdventurerUnderAttack 1
  mov rdi, %1
  callFunc _isAdventurerUnderAttack
%endmacro

%macro resetWeaponMemPool 0
  callFunc _resetWeaponMemPool
%endmacro

%macro releaseAllWeapon 1
  mov rdi, %1
  callFunc _releaseAllWeapon
%endmacro

%macro findEmptyWeaponSlot 1
  mov rdi, %1
  callFunc _findEmptyWeaponSlot
%endmacro

%macro parseAction 2
  mov rsi, %2
  mov rdi, %1
  callFunc _parseAction
%endmacro

%macro recvAction 2
  mov rsi, %2
  mov rdi, %1
  callFunc _recvAction
%endmacro

%macro sendState 1
  mov rdi, %1
  callFunc _sendState
%endmacro

%macro adventurerAction 1
  mov rdi, %1
  callFunc _adventurerAction
%endmacro

%macro unicornAction 1
  mov rdi, %1
  callFunc _unicornAction
%endmacro

%macro doAction 1
  mov rdi, %1
  callFunc _doAction
%endmacro

%macro checkConfrontOver 1
  mov rdi, %1
  callFunc _checkConfrontOver
%endmacro

section .code
_start:
  ;-------------------------------------------------------
  %ifdef COMMENT
    //abuse dr1 to point to start of memory pool
    def _start():
      memPool_base = MEMMIN
      goto _main
  %endif
  ;-------------------------------------------------------
  %ifdef CODE
    mov rdi, MEMMIN
    mov dr1, rdi
    jmp _main
  %endif

__stack_chk_fail:
  ;-------------------------------------------------------
  %ifdef COMMENT
    def __stack_chk_fail():
      write(1,"stack smashing detected\n",0x18)
      exit(1)
  %endif
  ;-------------------------------------------------------
  %ifdef CODE
    write 1, [rel STACK_SMASHING], 0x18
    exit 1
  %endif

prologue:
  ;-------------------------------------------------------
  %ifdef COMMENT
    we change the calling convention slightly here
    and use r10 as pointer to function to call
    function call will be replaced with call prologue
    ret will be replaced with jmp epilogue
    +------------+ <- rsp/rbp upon leave
    |   canary   | <= canary
    |   rbp      | <= rbp
    |   r15      | <= r15
    |   r14      | <= r14
    |   r13      | <= r13
    |   r12      | <= r12
    |   r11      | <= r11
    +------------+ <- rsp upon entry
    |   rip      | <= pushed by caller
    +------------+
  %endif
  ;-------------------------------------------------------
  %ifdef CODE
    push r11
    push r12
    push r13
    push r14
    push r15
    push rbp
    mov rbp, dr0
    mov rbp, [rbp]
    push rbp
    mov rbp, rsp
    jmp r10
  %endif

epilogue:
  ;-------------------------------------------------------
  %ifdef COMMENT
    abuse that rdi, rsi, rdx are never preserved
    +------------+ <- rbp upon entry
    |   canary   | => rdi
    |   rbp      | => rbp
    |   r15      | => r15
    |   r14      | => r14
    |   r13      | => r13
    |   r12      | => r12
    |   r11      | => r11
    |   rip      | => rsi
    +------------+ <- rsp upon leave
  %endif
  ;-------------------------------------------------------
  %ifdef CODE
    mov rsp, rbp
    pop rdi
    pop rbp
    pop r15
    pop r14
    pop r13
    pop r12
    pop r11
    pop rsi
    mov rdx, dr0
    mov rdx, [rdx]
    xor rdi, rdx
    test rdi, rdi
    jnz __stack_chk_fail
    jmp rsi
  %endif

_exit:
  ;-------------------------------------------------------
  %ifdef COMMENT
    def exit(status):
      syscall(60,status)
      halt
  %endif
  ;-------------------------------------------------------
  %ifdef CODE
    mov rax, 60
    syscall
    hlt
  %endif

_mmap:
  ;-------------------------------------------------------
  %ifdef COMMENT
    def mmap(addr,size,prot):
      if addr&PAGEMASK!=0:
        return SYSCALLFAIL
      if addr>=MEMMAX or addr<MEMMIN:
        return SYSCALLFAIL
      if size!=PAGESIZE:
        return SYSCALLFAIL
      return syscall(9,addr,size,prot)
  %endif
  ;-------------------------------------------------------
  %ifdef CODE
    mov rax, 9
    ;addr must be 0x10000 aligned
    mov r8, PAGEMASK
    and r8, rdi
    jnz .illegal
    ;addr must be between MEMMIN and MEMMAX
    mov r8, MEMMAX
    cmp rdi, r8
    jae .illegal
    mov r8, MEMMIN
    cmp rdi, r8
    jb .illegal
    ;size must be equal to PAGESIZE
    cmp rsi, PAGESIZE
    jne .illegal
    syscall
    jmp .end
    .illegal:
    mov rax, SYSCALLFAIL
    .end:
    return
  %endif

_munmap:
  ;-------------------------------------------------------
  %ifdef COMMENT
    def munmap(addr,size):
      return syscall(11,addr,size)
  %endif
  ;-------------------------------------------------------
  %ifdef CODE
    mov rax, 11
    syscall
    return
  %endif

_write:
  ;-------------------------------------------------------
  %ifdef COMMENT
    def write(fd,buf,size):
      return syscall(1,fd,buf,size)
  %endif
  ;-------------------------------------------------------
  %ifdef CODE
    mov rax, 1
    syscall
    return
  %endif

_read:
  ;-------------------------------------------------------
  %ifdef COMMENT
    def read(fd,buf,size):
      return syscall(0,fd,buf,size)
  %endif
  ;-------------------------------------------------------
  %ifdef CODE
    mov rax, 0
    syscall
    return
  %endif

_memset:
  ;-------------------------------------------------------
  %ifdef COMMENT
    def memset(dst,chr,size):
      tiledChr = chr
      tiledChr = tiledChr|(tiledChr<<0x08)
      tiledChr = tiledChr|(tiledChr<<0x10)
      tiledChr = tiledChr|(tiledChr<<0x20)
      block = size/8
      for i in range(block):
        *(qword*)dst = tiledChr
        dst = (qword*)dst+1
      size-=block*8
      for i in range(size):
        *(byte*)dst = chr
        dst = (byte*)dst+1
      return
  %endif
  ;-------------------------------------------------------
  %ifdef CODE
    ;expand byte ro qword
    mov r8, rsi
    shl r8, 8
    or rsi, r8
    mov r8, rsi
    shl r8, 0x10
    or rsi, r8
    mov r8, rsi
    shl r8, 0x20
    or rsi, r8
    mov r8, rdx
    mov rax, rdx
    xor rdx, rdx
    mov r9, 8
    div r9
    test rax, rax
    jz .loop_multipleOf8End
    mov rcx, 0
    .loop_multipleOf8:
      mov qword [rdi], rsi
      add rdi, 8
      inc rcx
      cmp rax, rcx
      jne .loop_multipleOf8
    mov r9, 8
    mul r9
    sub r8, rax
    .loop_multipleOf8End:
    test r8, r8
    jz .loop_end
    mov rcx, 0
    .loop:
      mov byte [rdi], sil
      inc rdi
      inc rcx
      cmp r8, rcx
      jne .loop
    .loop_end:
    return
  %endif

_memcpy:
  ;-------------------------------------------------------
  %ifdef COMMENT
    def memcpy(dst,src,size):
      block = size/8
      for i in range(block):
        *(qword*)dst = *(qword*)src
        dst = *(qword*)dst+1
        src = *(qword*)src+1
      size-=block*8
      for i in range(size):
        *(byte*)dst = *(byte*)src
        dst = *(byte*)dst+1
        src = *(byte*)src+1
      return
  %endif
  ;-------------------------------------------------------
  %ifdef CODE
    mov r8, rdx
    mov rax, rdx
    xor rdx, rdx
    mov r9, 8
    div r9
    mov r9, rax
    test r9, r9
    jz .loop_multipleOf8End
    mov rcx, 0
    .loop_multipleOf8:
      mov rax, qword [rsi]
      mov qword [rdi], rax
      add rsi, 8
      add rdi, 8
      inc rcx
      cmp r9, rcx
      jne .loop_multipleOf8
    mov rax, r9
    mov r9, 8
    mul r9
    sub r8, rax
    .loop_multipleOf8End:
    test r8, r8
    jz .loop_end
    mov rcx, 0
    .loop:
      mov al, byte [rsi]
      mov byte [rdi], al
      inc rdi
      inc rsi
      inc rcx
      cmp r8, rcx
      jne .loop
    .loop_end:
    return
  %endif

_isUnicornUnderAttack:
  ;-------------------------------------------------------
  %ifdef COMMENT
    def isUnicornUnderAttack(confrontState):
      if confrontState.adventurerAttackBoxLoc==LOC_NONE:
        return NOT_UNDER_ATTACK
      attkLoc = confrontState.adventurerAttackBoxLoc
      attkSrc = confrontState.adventurerAttackSourceLoc
      if confrontState.adventurerWeaponIdx==SLOT_NONE:
        attkDelta = BAREHANDED_DELTA
        attkRange = BAREHANDED_RANGE
      else:
        curWeapon = confrontState.adventurerWeapons[confrontState.adventurerWeaponIdx].ptr
        attkDelta = curWeapon.delta
        attkRange = curWeapon.range
      hitBoxRight = confrontState.unicornLoc+UNICORN_HALF_SIZE
      hitBoxLeft = confrontState.unicornLoc-UNICORN_HALF_SIZE
      attkState = confront.adventurerState
      if attkState&1==0:
        if attkSrc>attkRange:
          leftLimit = attkSrc-attkRange
        else:
          leftLimit = STAGE_MIN
        if attkLoc-leftLimit<attkDelta:
          attkDelta = attkLoc-leftLimit
        if hitBoxLeft>=attkLoc:
          return NOT_UNDER_ATTACK
        if attkLoc>attkDelta:
          attkLeft = attkLoc-attkDelta
          if hitBoxRight<=attkLeft:
            return NOT_UNDER_ATTACK
      else:
        rightLimit = attkSrc+attkRange
        if rightLimit>=STAGE_MAX:
          rightLimit = STAGE_MAX
        if rightLimit-attkLoc<attkDelta:
          attkDelta = rightLimit-attkLoc
        if hitBoxRight<=attkLoc:
          return NOT_UNDER_ATTACK
        attkRight = attkLoc+attkDelta
        if attkRight<STAGE_MAX:
          if hitBoxLeft>=attkRight:
            return NOT_UNDER_ATTACK
      if confrontState.adventurerLoc==confrontState.unicornLoc:
        return 0x10|((attkState&0xf)>>1)
      elif confrontState.adventurerLoc>confrontState.unicornLoc:
        return (((attkState&1)^1)<<4)|((attkState&0xf)>>1)
      else:
        return ((attkState&1)<<4)|((attkState&0xf)>>1)
  %endif
  ;-------------------------------------------------------
  %ifdef CODE
    mov r11, rdi
    mov rax, qword [r11+confrontState.adventurerAttackBoxLoc]
    mov rsi, LOC_NONE
    cmp rax, rsi
    je .notUnderAttack
    mov r8, rax
    mov r15, qword [r11+confrontState.adventurerAttackSourceLoc]
    mov rax, qword [r11+confrontState.adventurerWeaponIdx]
    mov rsi, SLOT_NONE
    cmp rax, rsi
    je .bareHanded
    .hasWeapon:
    lea rsi, [r11+confrontState.adventurerWeapons]
    mov rdx, weaponEntry_size
    mul rdx
    add rax, rsi
    mov rax, qword [rax+weaponEntry.ptr]
    mov rsi, qword [rax+weapon.delta]
    mov r14, qword [rax+weapon.range]
    jmp .checkRegionOverlap
    .bareHanded:
    mov rsi, BAREHANDED_DELTA
    mov r14, BAREHANDED_RANGE
    .checkRegionOverlap:
    mov rax, qword [r11+confrontState.unicornLoc]
    mov r10, rax
    add r10, UNICORN_HALF_SIZE
    sub rax, UNICORN_HALF_SIZE
    mov rdx, qword [r11+confrontState.adventurerState]
    mov r9, rdx
    and rdx, 1
    jnz .attackRight
    .attackLeft:
    cmp r15, r14
    jbe .leftLimitZero
    .leftLimitNotZero:
    sub r15, r14
    jmp .leftLimitProcessed
    .leftLimitZero:
    mov r15, STAGE_MIN
    .leftLimitProcessed:
    mov r14, r8
    sub r14, r15
    cmp r14, rsi
    jae .leftLimitNotReached
    .leftLimitReached:
    mov rsi, r14
    .leftLimitNotReached:
    cmp rax, r8
    jae .notUnderAttack
    cmp r8, rsi
    jbe .underAttack
    sub r8, rsi
    cmp r10, r8
    jbe .notUnderAttack
    jmp .underAttack
    .attackRight:
    add r15, r14
    cmp r15, STAGE_MAX
    jae .rightLimitMax
    .rightLimitNotMax:
    jmp .rightLimitProcessed
    .rightLimitMax:
    mov r15, STAGE_MAX
    .rightLimitProcessed:
    sub r15, r8
    cmp r15, rsi
    jae .rightLimitNotReached
    .rightLimitReached:
    mov rsi, r15
    .rightLimitNotReached:
    cmp r10, r8
    jbe .notUnderAttack
    add r8, rsi
    cmp r8, STAGE_MAX
    jae .underAttack
    cmp rax, r8
    jae .notUnderAttack
    .underAttack:
    mov rax, r9
    and rax, 0xf
    shr rax, 1
    mov rsi, qword [r11+confrontState.adventurerLoc]
    mov rdx, qword [r11+confrontState.unicornLoc]
    cmp rsi, rdx
    je .samePos
    ja .toLeft
    .toRight:
    and r9, 0x1
    shl r9, 4
    or rax, r9
    jmp .done
    .toLeft:
    and r9, 0x1
    xor r9, 0x1
    shl r9, 4
    or rax, r9
    jmp .done
    .samePos:
    or rax, 0x10
    jmp .done
    .notUnderAttack:
    mov rax, NOT_UNDER_ATTACK
    .done:
    return
  %endif

_isAdventurerUnderAttack:
  ;-------------------------------------------------------
  %ifdef COMMENT
    def isAdventurerUnderAttack(confrontState):
      if confrontState.unicornAttackBoxLoc==LOC_NONE:
        return NOT_UNDER_ATTACK
      attkLoc = confrontState.unicornAttackBoxLoc
      attkSrc = confrontState.unicornAttackSourceLoc
      if confrontState.unicornStage==UNICORN_STAGE1:
        attkDelta = UNICORN_STAGE1_DELTA
        attkRange = UNICORN_STAGE1_RANGE
      elif confrontState.unicornStage==UNICORN_STAGE2:
        attkDelta = UNICORN_STAGE2_DELTA
        attkRange = UNICORN_STAGE2_RANGE
      else:
        attkDelta = UNICORN_STAGE3_DELTA
        attkRange = UNICORN_STAGE3_RANGE
      hitBoxRight = confrontState.adventurerLoc+ADVENTURER_HALF_SIZE
      hitBoxLeft = confrontState.advennturerLoc-ADVENTURER_HALF_SIZE
      attkState = confront.unicornState
      if attkState&1==0:
        if attkSrc>attkRange:
          leftLimit = attkSrc-attkRange
        else:
          leftLimit = STAGE_MIN
        if attkLoc-leftLimit<attkDelta:
          attkDelta = attkLoc-leftLimit
        if hitBoxLeft>=attkLoc:
          return NOT_UNDER_ATTACK
        if attkLoc>attkDelta:
          attkLeft = attkLoc-attkDelta
          if hitBoxRight<=attkLeft:
            return NOT_UNDER_ATTACK
      else:
        rightLimit = attkSrc+attkRange
        if rightLimit>=STAGE_MAX:
          rightLimit = STAGE_MAX
        if rightLimit-attkLoc<attkDelta:
          attkDelta = rightLimit-attkLoc
        if hitBoxRight<=attkLoc:
          return NOT_UNDER_ATTACK
        attkRight = attkLoc+attkDelta
        if attkRight<STAGE_MAX:
          if hitBoxLeft>=attkRight:
            return NOT_UNDER_ATTACK
      if confrontState.unicornLoc==confrontState.adventurerLoc:
        return 0x10|((attkState&0xf)>>1)
      elif confrontState.unicornLoc>confrontState.adventurerLoc:
        return (((attkState&1)^1)<<4)|((attkState&0xf)>>1)
      else:
        return ((attkState&1)<<4)|((attkState&0xf)>>1)
  %endif
  ;-------------------------------------------------------
  %ifdef CODE
    mov r11, rdi
    mov rax, qword [r11+confrontState.unicornAttackBoxLoc]
    mov rsi, LOC_NONE
    cmp rax, rsi
    je .notUnderAttack
    mov r8, rax
    mov r15, qword [r11+confrontState.unicornAttackSourceLoc]
    mov rax, qword [r11+confrontState.unicornStage]
    cmp rax, UNICORN_STAGE1
    je .unicorn_STAGE1
    cmp rax, UNICORN_STAGE2
    je .unicorn_STAGE2
    .unicorn_STAGE3:
    mov rsi, UNICORN_STAGE3_DELTA
    mov r14, UNICORN_STAGE3_RANGE
    jmp .checkRegionOverlap
    .unicorn_STAGE2:
    mov rsi, UNICORN_STAGE2_DELTA
    mov r14, UNICORN_STAGE2_RANGE
    jmp .checkRegionOverlap
    .unicorn_STAGE1:
    mov rsi, UNICORN_STAGE1_DELTA
    mov r14, UNICORN_STAGE1_RANGE
    .checkRegionOverlap:
    mov rax, qword [r11+confrontState.adventurerLoc]
    mov r10, rax
    add r10, ADVENTURER_HALF_SIZE
    sub rax, ADVENTURER_HALF_SIZE
    mov rdx, qword [r11+confrontState.unicornState]
    mov r9, rdx
    and rdx, 1
    jnz .attackRight
    .attackLeft:
    cmp r15, r14
    jbe .leftLimitZero
    .leftLimitNotZero:
    sub r15, r14
    jmp .leftLimitProcessed
    .leftLimitZero:
    mov r15, STAGE_MIN
    .leftLimitProcessed:
    mov r14, r8
    sub r14, r15
    cmp r14, rsi
    jae .leftLimitNotReached
    .leftLimitReached:
    mov rsi, r14
    .leftLimitNotReached:
    cmp rax, r8
    jae .notUnderAttack
    cmp r8, rsi
    jbe .underAttack
    sub r8, rsi
    cmp r10, r8
    jbe .notUnderAttack
    jmp .underAttack
    .attackRight:
    add r15, r14
    cmp r15, STAGE_MAX
    jae .rightLimitMax
    .rightLimitNotMax:
    jmp .rightLimitProcessed
    .rightLimitMax:
    mov r15, STAGE_MAX
    .rightLimitProcessed:
    sub r15, r8
    cmp r15, rsi
    jae .rightLimitNotReached
    .rightLimitReached:
    mov rsi, r15
    .rightLimitNotReached:
    cmp r10, r8
    jbe .notUnderAttack
    add r8, rsi
    cmp r8, STAGE_MAX
    jae .underAttack
    cmp rax, r8
    jae .notUnderAttack
    .underAttack:
    mov rax, r9
    and rax, 0xf
    shr rax, 1
    mov rsi, qword [r11+confrontState.unicornLoc]
    mov rdx, qword [r11+confrontState.adventurerLoc]
    cmp rsi, rdx
    je .samePos
    ja .toLeft
    .toRight:
    and r9, 0x1
    shl r9, 4
    or rax, r9
    jmp .done
    .toLeft:
    and r9, 0x1
    xor r9, 0x1
    shl r9, 4
    or rax, r9
    jmp .done
    .samePos:
    or rax, 0x10
    jmp .done
    .notUnderAttack:
    mov rax, NOT_UNDER_ATTACK
    .done:
    return
  %endif

_unicornRandNext:
  ;-------------------------------------------------------
  %ifdef COMMENT
    def unicornRandNext(confrontState,mod):
      randState = confrontState.unicornRand
      randState^=randState<<13
      randState^=randState>>7
      randState^=randState<<17
      confrontState.unicornRand = randState
      return randState%mod
  %endif
  ;-------------------------------------------------------
  %ifdef CODE
    mov r11, rdi
    mov rax, qword [r11+confrontState.unicornRand]
    mov rdx, rax
    shl rdx, 13
    xor rax, rdx
    mov rdx, rax
    shr rdx, 7
    xor rax, rdx
    mov rdx, rax
    shl rdx, 17
    xor rax, rdx
    mov qword [r11+confrontState.unicornRand], rax
    xor rdx, rdx
    div rsi
    mov rax, rdx
    return
  %endif

_resetWeaponMemPool:
  ;-------------------------------------------------------
  %ifdef COMMENT
    def resetWeaponMemPool():
      memPool_base = WEAPON_MEM_POOL
  %endif
  ;-------------------------------------------------------
  %ifdef CODE
    mov rdi, WEAPON_MEM_POOL
    mov dr1, rdi
    return
  %endif

_releaseAllWeapon:
  ;-------------------------------------------------------
  %ifdef COMMENT
    def releaseAllWeapon(confrontState):
      for i in range(WEAPON_MAX_IDX):
        curWeapon = confrontState.adventurerWeapons[i]
        if curWeapon.ptr!=NULL:
          mummap(curWeapon.ptr,curWeapon.size)
      resetWeaponMemPool()
      return
  %endif
  ;-------------------------------------------------------
  %ifdef CODE
    mov r11, rdi
    lea r12, [r11+confrontState.adventurerWeapons]
    mov rcx, 0
    .releaseWeaponLoop:
      mov rax, qword [r12+weaponEntry.ptr]
      test rax, rax
      jz .releaseWeaponNext
      mov rdi, qword [r12+weaponEntry.size]
      munmap rax, rdi
      .releaseWeaponNext:
      add r12, weaponEntry_size
      inc rcx
      cmp rcx, MAX_WEAPON_IDX
      jne .releaseWeaponLoop
    resetWeaponMemPool
    return
  %endif

_findEmptyWeaponSlot:
  ;-------------------------------------------------------
  %ifdef COMMENT
    def findEmptyWeaponSlot(confrontState):
      for i in range(MAX_WEAPON_IDX):
        if confrontState.weaponEntry[i].ptr==NULL:
          return i
      return SLOT_NONE
  %endif
  ;-------------------------------------------------------
  %ifdef CODE
    mov rcx, 0
    mov r11, rdi
    lea rdi, [r11+confrontState.adventurerWeapons]
    .loopForSlot:
      mov rax, qword [rdi+weaponEntry.ptr]
      test rax, rax
      jz .foundSlot
      inc rcx
      add rdi, weaponEntry_size
      cmp rcx, MAX_WEAPON_IDX
      jne .loopForSlot
    .noSlot:
    mov rax, SLOT_NONE
    jmp .done
    .foundSlot:
    mov rax, rcx
    .done:
    return
  %endif

_parseAction:
  ;-------------------------------------------------------
  %ifdef COMMENT
    def parseAction(confrontState,actionStruct):
      if confrontState.isConfront==0:
        if actionStruct.action==STARTBATTLE:
          confrontState.isConfront = 1
          namelen = actionStruct.startBattleStruct.namelen
          if namelen>MAX_NAME_LEN:
            namelen = MAX_NAME_LEN
          memcpy(confrontState.adventurerName,actionStruct.startBattleStruct.name,namelen)
          desclen = actionStruct.startBattleStruct.desclen
          if desclen>MAX_DESC_LEN:
            desclen = MAX_DESC_LEN
          memcpy(confrontState.adventurerDesc,actionStruct.startBattleStruct.desc,desclen)
          confrontState.unicornRand = canary
          confrontState.unicornStage = UNICORN_STAGE1
          confrontState.unicornHP = UNICORN_STAGE1_HP
          confrontState.unicornAttack = UNICORN_STAGE1_ATTACK
          confrontState.unicornDefense = UNICORN_STAGE1_DEFENSE
          confrontState.unicornState = STATE_NONE
          confrontState.unicornAttribute = UNICORN_STAGE1_ATTRIBUTE
          confrontState.unicornCD = 0
          confrontState.unicornDefenseGauge = UNICORN_STAGE1_DEFENSE_GAUGE
          confrontState.unicornLoc = UNICORN_INIT_LOC
          confrontState.unicornAttackBoxLoc = LOC_NONE
          confrontState.unicornAttackSourceLoc = LOC_NONE
          confrontState.adventurerHP = ADVENTURER_INIT_HP
          confrontState.adventurerAttack = ADVENTURER_INIT_ATTACK
          confrontState.adventurerDefense = ADVENTURER_INIT_DEFENSE
          confrontState.adventurerState = STATE_NONE
          confrontState.adventurerCD = 0
          confrontState.adventurerDefenseGauge = ADVENTURER_DEFENSE_GAUGE
          confrontState.adventurerLoc = ADVENTURER_INIT_LOC
          confrontState.adventurerAttackBoxLoc = LOC_NONE
          confrontState.adventurerAttackSourceLoc = LOC_NONE
          confrontState.adventurerWeaponIdx = SLOT_NONE
          memset(confrontState.adventurerWeapons,0,WEAPON_ARRAY_SIZE)
          return 0
        elif actionStruct.action==GIVEUP:
          return 1
      elif confrontState.adventurerCD==0:
        if actionStruct.action==IDLE:
          return 0
        elif actionStruct.action==CRAFTWEAPON:
          if actionStruct.craftWeaponStruct.range<=STAGE_MAX:
            if actionStruct.craftWeaponStruct.delta!=0:
              if actionStruct.craftWeaponStruct<=STAGE_MAX:
                slotIdx = findEmptyWeaponSlot(confrontState)
                if slotIdx!=SLOT_NONE:
                  newWeapon = getMem()
                  if newWeapon!=SYSCALLFAIL:
                    confrontState.adventurerWeapons[slotIdx].ptr = newWeapon
                    confrontState.adventurerWeapons[slotIdx].size = PAGESIZE
                    namelen = actionStruct.craftWeaponStruct.namelen
                    if namelen>MAX_NAME_LEN:
                      namelen = MAX_NAME_LEN
                    memcpy(newWeapon.name,actionStruct.craftWeaponStruct.name,namelen)
                    desclen = actionStruct.craftWeaponStruct.desclen
                    if desclen>MAX_DESC_LEN:
                      desclen = MAX_DESC_LEN
                    memcpy(newWeapon.desc,actionStruct.craftWeaponStruct.desc,desclen)
                    newWeapon.level = 0
                    newWeapon.attack = actionStruct.craftWeaponStruct.attack
                    newWeapon.defense = actionStruct.craftWeaponStruct.defense
                    newWeapon.attribute = actionStruct.craftWeaponStruct.attribute
                    newWeapon.CD = actionStruct.craftWeaponStruct.CD
                    newWeapon.range = actionStruct.craftWeaponStruct.range
                    newWeapon.delta = actionStruct.craftWeaponStruct.delta
                    newWeapon.movespeed = actionStruct.craftWeaponStruct.movespeed
          return 2
        elif actionStruct.action==SWITCHWEAPON:
          slotIdx = actionStruct.switchWeaponStruct.targetIdx
          if slotIdx==MAX_WEAPON_IDX:
            confrontState.adventurerWeaponIdx = SLOT_NONE
          elif slotIdx<MAX_WEAPON_IDX:
            if confrontState.adventurerWeapons[slotIdx].ptr!=NULL
              confrontState.adventurerWeaponIdx = slotIdx
          return 2
        elif actionStruct.action==ENHANCEWEAPON:
          if confrontState.adventureWeaponIdx!=SLOT_NONE:
            curWeapon = confrontState.adventurerWeapons[confrontState.adventurerWeaponIdx].ptr
            if curWeapon.level<WEAPON_LEVEL_MAX:
              curWeapon.level+=1
              curWeapon.attack*=2
              curWeapon.defense*=2
          return 2
        elif actionStruct.action==DISPOSEWEAPON:
          if actionStruct.disposeWeaponStruct.targetIdx==confrontState.adventurerWeaponIdx:
            confrontState.adventurerWeaponIdx = SLOT_NONE
          curWeapon = confrontState.adventurerWeapons[actionStruct.disposeWeaponStruct.targetIdx]
          munmap(curWeapon.ptr,curWeapon.size)
          curWeapon.ptr = NULL
          curWeapon.size = 0
          return 2
        elif actionStruct.action==ATTACK:
          if confrontState.adventurerAttackBoxLoc==LOC_NONE:
            attkState = actionStruct.attackStruct.level
            if attkState<3:
              attkState<<=1
              if confrontState.adventurerLoc<confrontState.unicornLoc:
                attkState|=1
              attkState|=ATTACK_SET
              confrontState.adventurerState|=attkState
              confrontState.adventurerAttackBoxLoc = confrontState.adventurerLoc
              confrontState.adventurerAttackSourceLoc = confrontState.adventurerLoc
              if confrontState.adventurerWeaponIdx==SLOT_NONE:
                confrontState.adventurerCD = ADVENTURER_BAREHANDED_COOLDOWN
              else:
                confrontState.adventurerCD = confrontState.adventurerWeapons[confrontState.adventurerWeaponIdx].ptr.CD
          return 0
        elif actionStruct.action==DEFEND:
          dfndState = actionStruct.defendStruct.level
          dfndState>>=DEFEND_SHIFT
          if dfndState<3:
            dfndState<<=DEFEND_SHIFT
            dfndState|=DEFEND_SET
            confrontState.adventurerState|=dfndState
          return 0
        elif actionStruct.action==MOVE:
          moveState = actionStruct.moveStruct.direction
          moveState>>=MOVE_SHIFT
          if moveState<2:
            moveState<<=MOVE_SHIFT
            moveState|=MOVE_SET
            confrontState.adventurerState|=moveState
          return 0
      else:
        if actionStruct.action==RETREAT:
          confrontState.inConfront = 0
          releaseAllWeapon(confrontState)
          return 0
      return 0
  %endif
  ;-------------------------------------------------------
  %ifdef CODE
    mov r11, rdi
    mov r12, rsi
    ;check isConfront
    mov rax, qword [r11+confrontState.isConfront]
    test rax, rax
    jnz .isConfrontSet
    ;only these two options are only available without isConfront set
    mov rax, qword [r12+actionStruct.action]
    cmp rax, STARTBATTLE
    je .startconfront
    cmp rax, GIVEUP
    je .giveup
    jmp .donothing
    .isConfrontSet:
    ;check if cooldown is equal to 0
    mov rax, qword [r11+confrontState.adventurerCD]
    test rax, rax
    jz .canAct
    mov rax, qword [r12+actionStruct.action]
    cmp rax, RETREAT
    je .retreat
    jmp .donothing
    .canAct:
    mov rax, qword [r12+actionStruct.action]
    cmp rax, IDLE
    je .donothing
    cmp rax, CRAFTWEAPON
    je .craftweapon
    cmp rax, SWITCHWEAPON
    je .switchweapon
    cmp rax, ENHANCEWEAPON
    je .enhanceweapon
    cmp rax, DISPOSEWEAPON
    je .disposeweapon
    cmp rax, ATTACK
    je .attack
    cmp rax, DEFEND
    je .defend
    cmp rax, MOVE
    je .move
    jmp .donothing
    .startconfront:
      ;set isConfront
      mov byte [r11+confrontState.isConfront], 1
      ;load name
      mov rax, qword [r12+actionStruct.union+startBattleStruct.namelen]
      cmp rax, MAX_NAME_LEN
      jbe .startconfront_namelenChecked
      mov rax, MAX_NAME_LEN
      .startconfront_namelenChecked:
      memcpy [r11+confrontState.adventurerName], [r12+actionStruct.union+startBattleStruct.name], rax
      ;load description
      mov rax, qword [r12+actionStruct.union+startBattleStruct.desclen]
      cmp rax, MAX_DESC_LEN
      jbe .startconfront_desclenChecked
      mov rax, MAX_DESC_LEN
      .startconfront_desclenChecked:
      memcpy [r11+confrontState.adventurerDesc], [r12+actionStruct.union+startBattleStruct.desc], rax
      ;set initial stats
      mov rax, dr0
      mov rax, qword [rax]
      mov qword [r11+confrontState.unicornRand], rax
      mov qword [r11+confrontState.unicornStage], UNICORN_STAGE1
      mov qword [r11+confrontState.unicornHP], UNICORN_STAGE1_HP
      mov qword [r11+confrontState.unicornAttack], UNICORN_STAGE1_ATTACK
      mov qword [r11+confrontState.unicornDefense], UNICORN_STAGE1_DEFENSE
      mov qword [r11+confrontState.unicornState], STATE_NONE
      mov qword [r11+confrontState.unicornAttribute], UNICORN_STAGE1_ATTRIBUTE
      mov qword [r11+confrontState.unicornCD], 0
      mov qword [r11+confrontState.unicornDefenseGauge], UNICORN_STAGE1_DEFENSE_GAUGE
      mov qword [r11+confrontState.unicornLoc], UNICORN_INIT_LOC
      mov rax, LOC_NONE
      mov qword [r11+confrontState.unicornAttackBoxLoc], rax
      mov qword [r11+confrontState.unicornAttackSourceLoc], rax
      mov qword [r11+confrontState.adventurerHP], ADVENTURER_INIT_HP
      mov qword [r11+confrontState.adventurerAttack], ADVENTURER_INIT_ATTACK
      mov qword [r11+confrontState.adventurerDefense], ADVENTURER_INIT_DEFENSE
      mov qword [r11+confrontState.adventurerState], STATE_NONE
      mov qword [r11+confrontState.adventurerCD], 0
      mov qword [r11+confrontState.adventurerDefenseGauge], ADVENTURER_DEFENSE_GAUGE
      mov qword [r11+confrontState.adventurerLoc], ADVENTURER_INIT_LOC
      mov rax, LOC_NONE
      mov qword [r11+confrontState.adventurerAttackBoxLoc], rax
      mov qword [r11+confrontState.adventurerAttackSourceLoc], rax
      mov rax, SLOT_NONE
      mov qword [r11+confrontState.adventurerWeaponIdx], rax
      memset [r11+confrontState.adventurerWeapons], 0, WEAPON_ARRAY_SIZE
      jmp .donothing
    .retreat:
      ;unset isConfront
      mov qword [r11+confrontState.isConfront], 0
      ;release all weapons
      releaseAllWeapon r11
      jmp .donothing
    .craftweapon:
      mov rax, qword [r12+actionStruct.union+craftWeaponStruct.range]
      cmp rax, STAGE_MAX
      ja .weaponCmdDone
      mov rax, qword [r12+actionStruct.union+craftWeaponStruct.delta]
      test rax, rax
      jz .weaponCmdDone
      cmp rax, STAGE_MAX
      ja .weaponCmdDone
      findEmptyWeaponSlot r11
      mov rdi, SLOT_NONE
      cmp rax, rdi
      je .weaponCmdDone
      mov r13, rax
      getMem
      cmp rax, SYSCALLFAIL
      je .weaponCmdDone
      mov r14, rax
      lea rdi, [r11+confrontState.adventurerWeapons]
      mov rax, r13
      mov rsi, weaponEntry_size
      mul rsi
      add rax, rdi
      mov qword [rax+weaponEntry.ptr], r14
      mov qword [rax+weaponEntry.size], PAGESIZE
      ;load name
      mov rax, qword [r12+actionStruct.union+craftWeaponStruct.namelen]
      cmp rax, MAX_NAME_LEN
      jbe .craftweapon_namelenChecked
      mov rax, MAX_NAME_LEN
      .craftweapon_namelenChecked:
      memcpy [r14+weapon.name], [r12+actionStruct.union+craftWeaponStruct.name], rax
      ;load description
      mov rax, qword [r12+actionStruct.union+craftWeaponStruct.desclen]
      cmp rax, MAX_DESC_LEN
      jbe .craftweapon_desclenChecked
      mov rax, MAX_DESC_LEN
      .craftweapon_desclenChecked:
      memcpy [r14+weapon.desc], [r12+actionStruct.union+craftWeaponStruct.desc], rax
      ;load remaining attributes
      mov qword [r14+weapon.level], 0
      mov rax, qword [r12+actionStruct.union+craftWeaponStruct.attack]
      mov qword [r14+weapon.attack], rax
      mov rax, qword [r12+actionStruct.union+craftWeaponStruct.defense]
      mov qword [r14+weapon.defense], rax
      mov rax, qword [r12+actionStruct.union+craftWeaponStruct.attribute]
      mov qword [r14+weapon.attribute], rax
      mov rax, qword [r12+actionStruct.union+craftWeaponStruct.CD]
      mov qword [r14+weapon.CD], rax
      mov rax, qword [r12+actionStruct.union+craftWeaponStruct.range]
      mov qword [r14+weapon.range], rax
      mov rax, qword [r12+actionStruct.union+craftWeaponStruct.delta]
      mov qword [r14+weapon.delta], rax
      mov rax, qword [r12+actionStruct.union+craftWeaponStruct.movespeed]
      mov qword [r14+weapon.movespeed], rax
      jmp .weaponCmdDone
    .switchweapon:
      lea rdi, [r11+confrontState.adventurerWeapons]
      mov rax, qword [r12+actionStruct.union+switchWeaponStruct.targetIdx]
      cmp rax, MAX_WEAPON_IDX
      ja .weaponCmdDone
      jb .notDisarm
      mov rax, SLOT_NONE
      mov qword [r11+confrontState.adventurerWeaponIdx], rax
      jmp .weaponCmdDone
      .notDisarm:
      mov rsi, weaponEntry_size
      mul rsi
      add rax, rdi
      mov rax, qword [rax+weaponEntry.ptr]
      test rax, rax
      jz .weaponCmdDone
      mov rax, qword [r12+actionStruct.union+switchWeaponStruct.targetIdx]
      mov qword [r11+confrontState.adventurerWeaponIdx], rax
      jmp .weaponCmdDone
    .enhanceweapon:
      mov rax, [r11+confrontState.adventurerWeaponIdx]
      mov rdi, SLOT_NONE
      cmp rax, rdi
      je .weaponCmdDone
      lea rdi, [r11+confrontState.adventurerWeapons]
      mov rsi, weaponEntry_size
      mul rsi
      add rax, rdi
      mov rax, [rax+weaponEntry.ptr]
      mov rdi, qword [rax+weapon.level]
      cmp rdi, WEAPON_MAX_LEVEL
      jae .weaponCmdDone
      inc rdi
      mov qword [rax+weapon.level], rdi
      mov rdi, qword [rax+weapon.attack]
      add rdi, rdi
      mov qword [rax+weapon.attack], rdi
      mov rdi, qword [rax+weapon.defense]
      add rdi, rdi
      mov qword [rax+weapon.defense], rdi
      jmp .weaponCmdDone
    .disposeweapon:
      lea rdi, [r11+confrontState.adventurerWeapons]
      mov rax, qword [r12+actionStruct.union+disposeWeaponStruct.targetIdx]
      mov rsi, qword [r11+confrontState.adventurerWeaponIdx]
      cmp rax, rsi
      jne .disposeweapon_disarmed
      mov rsi, SLOT_NONE
      mov qword [r11+confrontState.adventurerWeaponIdx], rsi
      .disposeweapon_disarmed:
      mov rsi, weaponEntry_size
      mul rsi
      add rax, rdi
      mov rdi, qword [rax+weaponEntry.ptr]
      mov rsi, qword [rax+weaponEntry.size]
      mov r13, rax
      munmap rdi, rsi
      mov qword [r13+weaponEntry.ptr], 0
      mov qword [r13+weaponEntry.size], 0
      jmp .weaponCmdDone
    .attack:
      ;can only attack when no other attack box exists
      mov rax, [r11+confrontState.adventurerAttackBoxLoc]
      mov rdi, LOC_NONE
      cmp rax, rdi
      jne .donothing
      ;decide attack level (HIGH/MIDDLE/LOW)
      mov rax, [r12+actionStruct.union+attackStruct.level]
      cmp rax, 3
      jae .donothing
      shl rax, 1
      ;decide attack orientation
      mov rdi, [r11+confrontState.adventurerLoc]
      mov rsi, [r11+confrontState.unicornLoc]
      cmp rdi, rsi
      jae .attack_leftOriented
      .attack_rightOriented:
      or rax, 1
      .attack_leftOriented:
      ;set state to attack
      or rax, ATTACK_SET
      mov rdi, [r11+confrontState.adventurerState]
      or rax, rdi
      mov [r11+confrontState.adventurerState], rax
      ;set attack box
      mov rax, [r11+confrontState.adventurerLoc]
      mov [r11+confrontState.adventurerAttackBoxLoc], rax
      mov [r11+confrontState.adventurerAttackSourceLoc], rax
      ;update cooldown time, we need to check if adventurer is armed here
      mov rax, [r11+confrontState.adventurerWeaponIdx]
      mov rdi, SLOT_NONE
      cmp rax, rdi
      jne .attack_armed
      mov qword [r11+confrontState.adventurerCD], ADVENTURER_BAREHANDED_COOLDOWN
      jmp .attack_done
      .attack_armed:
      lea rdi, [r11+confrontState.adventurerWeapons]
      mov rsi, weaponEntry_size
      mul rsi
      add rax, rdi
      mov rax, qword [rax+weaponEntry.ptr]
      mov rax, qword [rax+weapon.CD]
      mov [r11+confrontState.adventurerCD], rax
      .attack_done:
      jmp .donothing
    .defend:
      ;decide defend level (HIGH/MIDDLE/LOW)
      mov rax, [r12+actionStruct.union+defendStruct.level]
      shr rax, DEFEND_SHIFT
      cmp rax, 3
      jae .donothing
      shl rax, DEFEND_SHIFT
      ;set state to defend
      or rax, DEFEND_SET
      mov rdi, [r11+confrontState.adventurerState]
      or rax, rdi
      mov [r11+confrontState.adventurerState], rax
      jmp .donothing
    .move:
      ;decide move direction
      mov rax, qword [r12+actionStruct.union+moveStruct.direction]
      shr rax, MOVE_SHIFT
      cmp rax, 2
      jae .donothing
      shl rax, MOVE_SHIFT
      or rax, MOVE_SET
      mov rdi, [r11+confrontState.adventurerState]
      or rax, rdi
      mov [r11+confrontState.adventurerState], rax
      jmp .donothing
    .giveup:
      mov rax, 1
      jmp .done
    .weaponCmdDone:
      mov rax, 2
      jmp .done
    .donothing:
      mov rax, 0
    .done:
      return
  %endif

_sendState:
  ;-------------------------------------------------------
  %ifdef COMMENT
    def sendState(confrontState):
      char buf[0x80]
      buf[0] = '\xff'
      write(1,buf,1)
      write(1,confrontState.isConfront,offset(confrontState,adventurerWeapons)-offset(confrontState,isConfront))
      return
  %endif
  ;-------------------------------------------------------
  %ifdef CODE
    sub rsp, 0x80
    mov r11, rdi
    mov qword [rsp], 0xff
    write 1, [rsp], 1
    mov r12, confrontState.adventurerWeapons
    sub r12, confrontState.isConfront
    write 1, [r11+confrontState.isConfront], r12
    return
  %endif

_recvAction:
  ;-------------------------------------------------------
  %ifdef COMMENT
    def recvAction(buf,size):
      l = 4
      cursor = buf
      while True:
        res = read(0,cursor,l)
        if res==SYSCALLFAIL:
          exit(0)
        l-=res
        cursor+=res
      l = *(dword*)buf
      if l>size:
        exit(0)
      cursor = buf
      while True:
        res = read(0,cursor,l)
        if res==SYSCALLFAIL:
          exit(0)
        l-=res
        cursor+=res
      return
  %endif
  ;-------------------------------------------------------
  %ifdef CODE
    mov r11, rdi
    mov r14, rsi
    mov r12, 4
    mov r13, r11
    .getsize:
      read 0, [r13], r12
      mov rdi, SYSCALLFAIL
      cmp rax, rdi
      je .recvFailed
      sub r12, rax
      add r13, rax
      test r12, r12
      jnz .getsize
    mov r12d, dword [r11]
    cmp r12, r14
    ja .recvFailed
    .getdata:
      read 0, [r11], r12
      mov rdi, SYSCALLFAIL
      cmp rax, rdi
      je .recvFailed
      sub r12, rax
      add r11, rax
      test r12, r12
      jnz .getdata
    return
    .recvFailed:
    exit 0
  %endif

_adventurerAction:
  ;-------------------------------------------------------
  %ifdef COMMENT
    def adventurerAction(confrontState):
      char buf[0x280]
      recvAction(buf,0x280)
      parseAction(confrontState,buf)
      return
  %endif
  ;-------------------------------------------------------
  %ifdef CODE
    sub rsp, 0x280
    mov r11, rdi
    recvAction rsp, 0x280
    parseAction r11, rsp
    return
  %endif

_unicornAction:
  ;-------------------------------------------------------
  %ifdef COMMENT
    def unicornAction(confrontState):
      if confrontState.isConfront==0:
        return
      if confrontState.unicornHP>UNICORN_STAGE2_HP:
        pass
      elif confrontState.unicornHP>UNICORN_STAGE3_HP:
        if confrontState.unicornStage!=UNICORN_STAGE2:
          confrontState.unicornStage = UNICORN_STAGE2
          confrontState.unicornAttack = UNICORN_STAGE2_ATTACK
          confrontState.unicornDefense = UNICORN_STAGE2_DEFENSE
          confrontState.unicornDefenseGauge = UNICORN_STAGE2_DEFENSE_GAUGE
          confrontState.unicornAttribute = UNICORN_STAGE2_ATTRIBUTE
      else:
        if confrontState.unicornStage!=UNICORN_STAGE3:
          confrontState.unicornStage = UNICORN_STAGE3
          confrontState.unicornAttack = UNICORN_STAGE3_ATTACK
          confrontState.unicornDefense = UNICORN_STAGE3_DEFENSE
          confrontState.unicornDefenseGauge = UNICORN_STAGE3_DEFENSE_GAUGE
          confrontState.unicornAttribute = UNICORN_STAGE3_ATTRIBUTE
      if confrontState.unicornCD!=0:
        return
      if confrontState.unicornAttackBoxLoc==LOC_NONE:
        attkState = confrontState.unicornState
        if confrontState.unicornStage==UNICORN_STAGE1:
          confrontState.unicornCD = UNICORN_STAGE1_CD
          confrontState.unicornAttackBoxLoc = confrontState.unicornLoc
          confrontState.unicornAttackSourceLoc = confrontState.unicornLoc
          if confrontState.unicornLoc<confrontState.adventurerLoc:
            attkState|=1
        else:
          if confrontState.unicornStage==UNICORN_STAGE2:
            confrontState.unicornCD = UNICORN_STAGE2_CD
            maxDist = 400
          else:
            confrontState.unicornCD = UNICORN_STAGE3_CD
            maxDist = 100
          unicornLoc = confrontState.unicornLoc
          adventurerLoc = confrontState.adventurerLoc
          if unicornLoc>=adventurerLoc:
            if unicornLoc-adventurerLoc>maxDist:
              if adventurerLoc<=maxDist:
                attkSrc = STAGE_MIN
              else:
                attkSrc = adventurerLoc-maxDist
              attkState|=1
            else:
              attkSrc = unicornLoc
          else:
            if adventurerLoc-unicornLoc>maxDist:
              attkSrc = adventurerLoc+maxDist
              if attkSrc>=STAGE_MAX:
                attkSrc = STAGE_MAX
            else:
              attkSrc = unicornLoc
              attkState|=1
          confrontState.unicornAttackBoxLoc = attkSrc
          confrontState.unicornAttackSourceLoc = attkSrc
        attkState|=ATTACK_SET
        attkState|=unicornRandNext(confrontState,3)<<1
        confrontState.unicornState = attkState
        return
      attkType = isUnicornUnderAttack(confrontState)
      if attkType!=NO_UNDER_ATTACK:
        if attkType&0x10!=0:
          dfndState = ((attkType&0xf)<<DEFEND_SHIFT)|DEFEND_SET
          confrontState.unicornState|=dfndState
          return
      unicornLoc = confrontState.unicornLoc
      adventurerLoc = confrontState.adventurerLoc
      if unicornLoc<adventurerLoc:
        if adventurerLoc<UNICORN_DESIRED_DISTANCE:
          confrontState.unicornState|=MOVE_RIGHT
        else:
          distance = adventurerLoc-unicornLoc
          if distance>UNICORN_DESIRED_DISTANCE:
            confrontState.unicornState|=MOVE_RIGHT
          elif distance<UNICORN_DESIRED_DISTANCE:
            confrontState.unicornState|=MOVE_LEFT
      else:
        if adventurerLoc>STAGE_MAX-UNICORN_DESIRED_DISTANCE:
          confrontState.unicornState|=MOVE_LEFT
        else:
          distance = unicornLoc-adventurerLoc
          if distance>UNICORN_DESIRED_DISTANCE:
            confrontState.unicornState|=MOVE_LEFT
          elif distance<UNICORN_DESIRED_DISTANCE:
            confrontState.unicornState|=MOVE_RIGHT
      return
  %endif
  ;-------------------------------------------------------
  %ifdef CODE
    mov r11, rdi
    ;check isConfront
    mov rax, qword [r11+confrontState.isConfront]
    test rax, rax
    jz .done
    ;move unicorn to next stage if necessary
    mov rax, qword [r11+confrontState.unicornHP]
    mov rdi, UNICORN_STAGE2_HP
    cmp rax, rdi
    ja .Stage1
    mov rdi, UNICORN_STAGE3_HP
    cmp rax, rdi
    ja .Stage2
    .Stage3:
    mov rax, qword [r11+confrontState.unicornStage]
    cmp rax, UNICORN_STAGE3
    je .StageDone
    mov qword [r11+confrontState.unicornStage], UNICORN_STAGE3
    mov qword [r11+confrontState.unicornAttack], UNICORN_STAGE3_ATTACK
    mov qword [r11+confrontState.unicornDefense], UNICORN_STAGE3_DEFENSE
    mov qword [r11+confrontState.unicornDefenseGauge], UNICORN_STAGE3_DEFENSE_GAUGE
    mov qword [r11+confrontState.unicornAttribute], UNICORN_STAGE3_ATTRIBUTE
    jmp .StageDone
    .Stage2:
    mov rax, qword [r11+confrontState.unicornStage]
    cmp rax, UNICORN_STAGE2
    je .StageDone
    mov qword [r11+confrontState.unicornStage], UNICORN_STAGE2
    mov qword [r11+confrontState.unicornAttack], UNICORN_STAGE2_ATTACK
    mov qword [r11+confrontState.unicornDefense], UNICORN_STAGE2_DEFENSE
    mov qword [r11+confrontState.unicornDefenseGauge], UNICORN_STAGE2_DEFENSE_GAUGE
    mov qword [r11+confrontState.unicornAttribute], UNICORN_STAGE2_ATTRIBUTE
    .Stage1:
    .StageDone:
    ;check if cooldown is equal to 0
    mov rax, qword [r11+confrontState.unicornCD]
    test rax, rax
    jnz .done
    mov rax, qword [r11+confrontState.unicornAttackBoxLoc]
    mov rdi, LOC_NONE
    cmp rax, rdi
    jne .cantAttack
    mov r12, qword [r11+confrontState.unicornState]
    mov rax, qword [r11+confrontState.unicornStage]
    cmp rax, UNICORN_STAGE1
    je .attack_Stage1
    cmp rax, UNICORN_STAGE2
    je .attack_Stage2
    .attack_Stage3:
    ;at this stage, attacks can be spawned behind the adventurer at extremely near pos
    ;attack CD is also extremely short
    mov qword [r11+confrontState.unicornCD], UNICORN_STAGE3_CD
    mov rdx, 100
    jmp .attack_Stage2_3_common
    .attack_Stage2:
    ;at this stage, attacks can be spawned behind the adventurer at moderate pos
    mov qword [r11+confrontState.unicornCD], UNICORN_STAGE2_CD
    mov rdx, 400
    .attack_Stage2_3_common:
    mov rax, [r11+confrontState.unicornLoc]
    mov rdi, [r11+confrontState.adventurerLoc]
    cmp rax, rdi
    jae .attack_Stage2_3_unicornAtRight
    .attack_Stage2_3_unicornAtLeft:
    mov rsi, rdi
    sub rsi, rax
    cmp rsi, rdx
    jbe .attack_Stage2_3_attackFromLeftUnicorn
    add rdi, rdx
    cmp rdi, STAGE_MAX
    jae .attack_Stage2_3_attackFromRightWall
    .attack_Stage2_3_attackFromRightVoid:
    mov qword [r11+confrontState.unicornAttackBoxLoc], rdi
    mov qword [r11+confrontState.unicornAttackSourceLoc], rdi
    jmp .attack_Common_decideLevel
    .attack_Stage2_3_attackFromRightWall:
    mov qword [r11+confrontState.unicornAttackBoxLoc], STAGE_MAX
    mov qword [r11+confrontState.unicornAttackSourceLoc], STAGE_MAX
    jmp .attack_Common_decideLevel
    .attack_Stage2_3_attackFromLeftUnicorn:
    mov qword [r11+confrontState.unicornAttackBoxLoc], rax
    mov qword [r11+confrontState.unicornAttackSourceLoc], rax
    or r12, 1
    jmp .attack_Common_decideLevel
    .attack_Stage2_3_unicornAtRight:
    mov rsi, rax
    sub rsi, rdi
    cmp rsi, rdx
    jbe .attack_Stage2_3_attackFromRightUnicorn
    cmp rdi, rdx
    jbe .attack_Stage2_3_attackFromLeftWall
    .attack_Stage2_3_attackFromLeftVoid:
    sub rdi, rdx
    mov qword [r11+confrontState.unicornAttackBoxLoc], rdi
    mov qword [r11+confrontState.unicornAttackSourceLoc], rdi
    or r12, 1
    jmp .attack_Common_decideLevel
    .attack_Stage2_3_attackFromLeftWall:
    mov qword [r11+confrontState.unicornAttackBoxLoc], STAGE_MIN
    mov qword [r11+confrontState.unicornAttackSourceLoc], STAGE_MIN
    or r12, 1
    jmp .attack_Common_decideLevel
    .attack_Stage2_3_attackFromRightUnicorn:
    mov qword [r11+confrontState.unicornAttackBoxLoc], rax
    mov qword [r11+confrontState.unicornAttackSourceLoc], rax
    jmp .attack_Common_decideLevel
    .attack_Stage1:
    mov qword [r11+confrontState.unicornCD], UNICORN_STAGE1_CD
    mov rax, qword [r11+confrontState.unicornLoc]
    mov qword [r11+confrontState.unicornAttackBoxLoc], rax
    mov qword [r11+confrontState.unicornAttackSourceLoc], rax
    mov rax, [r11+confrontState.unicornLoc]
    mov rdi, [r11+confrontState.adventurerLoc]
    cmp rax, rdi
    jae .attack_Stage1_attackFromRightUnicorn
    .attack_Stage1_attackFromLeftUnicorn:
    or r12, 1
    .attack_Stage1_attackFromRightUnicorn:
    .attack_Common_decideLevel:
    or r12, ATTACK_SET
    unicornRandNext r11, 3
    shl rax, 1
    or rax, r12
    mov qword [r11+confrontState.unicornState], rax
    jmp .done
    .cantAttack:
    ;else if under attack and defendable, defend
    isUnicornUnderAttack r11
    mov rdi, NOT_UNDER_ATTACK
    cmp rax, rdi
    je .dontDefend
    mov rdi, rax
    and rdi, 0x10
    jz .dontDefend
    and rax, 0xf
    shl rax, DEFEND_SHIFT
    mov rdi, qword [r11+confrontState.unicornState]
    or rax, DEFEND_SET
    or rax, rdi
    mov qword [r11+confrontState.unicornState], rax
    jmp .done
    .dontDefend:
    ;else try to maintain a static distance from adventurer
    mov rax, qword [r11+confrontState.unicornLoc]
    mov rdi, qword [r11+confrontState.adventurerLoc]
    cmp rax, rdi
    jae .move_unicornOnTheRight
    .move_unicornOnTheLeft:
    cmp rdi, UNICORN_DESIRED_DISTANCE
    jb .move_unicornMoveRight
    sub rdi, rax
    cmp rdi, UNICORN_DESIRED_DISTANCE
    ja .move_unicornMoveRight
    jb .move_unicornMoveLeft
    jmp .dontMove
    .move_unicornOnTheRight:
    mov rsi, STAGE_MAX
    sub rsi, UNICORN_DESIRED_DISTANCE
    cmp rdi, rsi
    ja .move_unicornMoveLeft
    sub rax, rdi
    cmp rax, UNICORN_DESIRED_DISTANCE
    jb .move_unicornMoveRight
    ja .move_unicornMoveLeft
    jmp .dontMove
    .move_unicornMoveLeft:
    mov rax, qword [r11+confrontState.unicornState]
    or rax, MOVE_LEFT
    mov qword [r11+confrontState.unicornState], rax
    jmp .done
    .move_unicornMoveRight:
    mov rax, qword [r11+confrontState.unicornState]
    or rax, MOVE_RIGHT
    mov qword [r11+confrontState.unicornState], rax
    jmp .done
    .dontMove:
    .done:
    return
  %endif

_doAction:
  ;-------------------------------------------------------
  %ifdef COMMENT
    def doAction(confrontState):
      if confrontState.isConfront==0:
        return
      attkType = isUnicornUnderAttack(confrontState)
      if attkType!=NOT_UNDER_ATTACK:
        confrontState.adventurerAttackBoxLoc = LOC_NONE
        confrontState.adventurerState&=ATTACK_CLEAR_MASK
        if confrontState.adventurerWeaponIdx==SLOT_NONE:
          attkAttr = 0
          attkStat = confrontState.adventurerAttack
        else:
          curWeapon = confrontState.adventurerWeapons[confrontState.adventurerWeaponIdx].ptr
          attkAttr = curWeapon.attribute
          attkStat = curWeapon.attack
        effectiveAttr = attkAttr&confrontState.unicornAttribute
        dfnsStat = confrontState.unicornDefense
        dfndState = confrontState.unicornState
        dfnsBroken = False
        if dfndState&DEFEND_SET!=0:
          if attkType&0x10!=0:
            attkLevel = attkType&0xf
            dfndLevel = dfndState>>DEFEND_SHIFT
            if attkLevel&dfndLevel!=0:
              if confrontState.unicornDefenseGauge==0:
                dfnsBroken = True
              else:
                conforntState.unicornDefenseGauge-=1
                dfnsStat*=2
        if dfnsBroken==False:
          if attkStat>dfnsStat:
            attkStat-=dfnsStat
            if effectiveAttr==0:
              attkStat/=2
          else:
            attkStat = 0
        else:
          attkStat*=2
        if confrontState.unicornHP<=attkStat:
          confrontState.unicornHP = 0
        else:
          confrontState.unicornHP-=attkStat
      attkType = isAdventurerUnderAttack(confrontState)
      if attkType!=NOT_UNDER_ATTACK:
        confrontState.unicornAttackBoxLoc = LOC_NONE
        confrontState.unicornState&=ATTACK_CLEAR_MASK
        attkStat = confrontState.unicornAttack
        dfnsStat = confrontState.adventurerDefense
        dfndState = confrontState.adventurerState
        dfnsBroken = False
        if dfndState&DEFEND_SET!=0:
          if attkType&0x10!=0:
            attkLevel = attkType&0xf
            dfndLevel = dfndState>>DEFEND_SHIFT
            if attkLevel&dfndLevel!=0:
              if confrontState.adventurerDefenseGauge==0:
                dfnsBroken = True
              else:
                if confrontState.adventurerWeaponIdx==SLOT_NONE:
                  dfnsStat = confrontState.adventurerDefense*2
                else:
                  dfnsStat = confrontState.adventurerWeapons[confrontState.adventurerWeaponIdx].ptr.defense*2
                conforntState.adventurerDefenseGauge-=1
                unicornDfns*=2
        if dfnsBroken==False:
          if attkStat>dfnsStat:
            attkStat-=dfnsStat
          else:
            attkStat = 0
        else:
          attkStat*=2
        if confrontState.adventurerHP<=attkStat:
          confrontState.adventurerHP = 0
        else:
          confrontState.adventurerHP-=attkStat
      if confrontState.adventurerAttackBoxLoc!=LOC_NONE:
        attkLoc = confrontState.adventurerAttackBoxLoc
        attkSrc = confrontState.adventurerAttackSourceLoc
        if confrontState.adventurerWeaponIdx==SLOT_NONE:
          attkDelta = BAREHANDED_DELTA
          attkRange = BAREHANDED_RANGE
        else:
          curWeapon = confrontState.adventurerWeapons[confrontState.adventurerWeaponIdx].ptr
          attkDelta = curWeapon.delta
          attkRange = curWeapon.range
        if confrontState.adventurerState&1==0:
          if attkSrc<=attkRange:
            leftLimit = STAGE_MIN
          else:
            leftLimit = attkSrc-attkRange
          if attkLoc<=attkDelta+leftLimit:
            confrontState.adventurerAttackSourceLoc = LOC_NONE
            confrontState.adventurerState&=ATTACK_CLEAR_MASK
            attkLoc = LOC_NONE
          else:
            attkLoc-=attkDelta
        else:
          rightLimit = attkSrc+attkRange
          if rightLimit>=STAGE_MAX:
            rightLimit = STAGE_MAX
          attkLoc+=attkDelta
          if attkLoc>=rightLimit:
            confrontState.adventurerAttackSourceLoc = LOC_NONE
            confrontState.adventurerState&=ATTACK_CLEAR_MASK
            attkLoc = LOC_NONE
        confrontState.adventurerAttackBoxLoc = attkLoc
      if confrontState.unicornAttackBoxLoc!=LOC_NONE:
        attkLoc = confrontState.unicornAttackBoxLoc
        attkSrc = confrontState.unicornAttackSourceLoc
        if confrontState.unicornStage==UNICORN_STAGE1:
          attkDelta = UNICORN_STAGE1_DELTA
          attkRange = UNICORN_STAGE1_RANGE
        elif confrontState.unicornStage==UNICORN_STAGE2:
          attkDelta = UNICORN_STAGE2_DELTA
          attkRange = UNICORN_STAGE2_RANGE
        else:
          attkDelta = UNICORN_STAGE3_DELTA
          attkRange = UNICORN_STAGE3_RANGE
        if confrontState.unicornState&1==0:
          if attkSrc<=attkRange:
            leftLimit = STAGE_MIN
          else:
            leftLimit = attkSrc-attkRange
          if attkLoc<=attkDelta+leftLimit:
            confrontState.unicornAttackSourceLoc = LOC_NONE
            confrontState.unicornState&=ATTACK_CLEAR_MASK
            attkLoc = LOC_NONE
          else:
            attkLoc-=attkDelta
        else:
          rightLimit = attkSrc+attkRange
          if rightLimit>=STAGE_MAX:
            rightLimit = STAGE_MAX
          attkLoc+=attkDelta
          if attkLoc>=rightLimit:
            confrontState.unicornAttackSourceLoc = LOC_NONE
            confrontState.unicornState&=ATTACK_CLEAR_MASK
            attkLoc = LOC_NONE
        confrontState.adventurerAttackBoxLoc = attkLoc
      moveState = confrontState.adventurerState
      if moveState&MOVE_SET!=0:
        confrontState.adventurerState&=MOVE_CLEAR_MASK
        if confrontState.adventurerWeaponIdx==SLOT_NONE:
          speed = BAREHANDED_MOVE_SPEED
        else:
          speed = confrontState.adventurerWeapons[confrontState.adventurerWeaponIdx].ptr.movespeed
        curLoc = confrontState.adventurerLoc
        margin = ADVENTURER_HALF_SIZE
        if (moveState>>MOVE_SHIFT)&1==0:
          if curLoc<=margin+speed:
            curLoc = ADVENTURER_HALF_SIZE
          else:
            curLoc-=speed
        else:
          if curLoc+speed>=STAGE_MAX-margin:
            curLoc = STAGE_MAX-margin
          else:
            curLoc = curLoc+speed
        confrontState.adventurerLoc = curLoc
      moveState = confrontState.unicornState
      if moveState&MOVE_SET!=0:
        confrontState.unicornState&=MOVE_CLEAR_MASK
        speed = UNICORN_MOVE_SPEED
        curLoc = confrontState.unicornLoc
        margin = UNICORN_HALF_SIZE
        if (moveState>>MOVE_SHIFT)&1==0:
          if curLoc<=margin+speed:
            curLoc = UNICORN_HALF_SIZE
          else:
            curLoc-=speed
        else:
          if curLoc+speed>=STAGE_MAX-margin:
            curLoc = STAGE_MAX-margin
          else:
            curLoc = curLoc+speed
        confrontState.unicornLoc = curLoc
      if confrontState.adventurerCD!=0:
        confrontState.adventurerCD-=1
      if confrontState.unicornCD!=0:
        confrontState.unicornCD-=1
      if confrontState.adventurerState&DEFEND_SET==0:
        if confrontState.adventurerDefenseGauge<ADENTURER_DEFENSE_GAUGE:
          confrontState.adventurerDefenseGauge+=1
      confrontState.adventurerState&=DEFEND_CLEAR_MASK
      if confrontState.unicornState&DEFEND_SET==0:
        if confrontState.unicornStage==UNICORN_STAGE1:
          gaugeMax = UNICORN_STAGE1_DEFENSE_GAUGE
        elif confrontState.unicornStage==UNICORN_STAGE2:
          gaugeMax = UNICORN_STAGE2_DEFENSE_GAUGE
        else:
          gaugeMax = UNICORN_STAGE3_DEFENSE_GAUGE
        if confrontState.unicornDefenseGauge<gaugeMax:
          confrontState.unicornDefenseGauge+=1
      confrontState.unicornState&=DEFEND_CLEAR_MASK
      return
  %endif
  ;-------------------------------------------------------
  %ifdef CODE
    mov r11, rdi
    mov rax, qword [r11+confrontState.isConfront]
    test rax, rax
    jz .done
    ;check attack interaction first
    isUnicornUnderAttack r11
    mov r12, rax
    mov rdi, NOT_UNDER_ATTACK
    cmp rax, rdi
    je .unicornNotUnderAttack
    .unicornUnderAttack:
    mov rax, LOC_NONE
    mov qword [r11+confrontState.adventurerAttackBoxLoc], rax
    mov rax, qword [r11+confrontState.adventurerState]
    mov rdi, ATTACK_CLEAR_MASK
    and rax, rdi
    mov qword [r11+confrontState.adventurerState], rax
    mov rax, qword [r11+confrontState.adventurerWeaponIdx]
    mov rdi, SLOT_NONE
    cmp rax, rdi
    je .adventurerAttackWithoutWeapon
    .adventurerAttackWithWeapon:
    lea rdi, [r11+confrontState.adventurerWeapons]
    mov rsi, weaponEntry_size
    mul rsi
    add rax, rdi
    mov rax, qword [rax+weaponEntry.ptr]
    mov r15, qword [rax+weapon.attribute]
    mov r13, qword [rax+weapon.attack]
    jmp .adventurerWeaponFetched
    .adventurerAttackWithoutWeapon:
    mov r15, 0
    mov r13, qword [r11+confrontState.adventurerAttack]
    .adventurerWeaponFetched:
    mov rdi, r15
    mov rdx, qword [r11+confrontState.unicornAttribute]
    and rdi, rdx
    mov r14, rdi
    mov rax, r12
    mov r12, qword [r11+confrontState.unicornDefense]
    mov rdi, qword [r11+confrontState.unicornState]
    mov rsi, rdi
    and rsi, DEFEND_SET
    jz .unicornNoDefend
    .unicornHasDefend:
    mov rdx, rax
    and rdx, 0x10
    jz .unicornIneffectiveDefend
    and rax, 0xf
    shr rdi, DEFEND_SHIFT
    and rax, rdi
    jz .unicornIneffectiveDefend
    .unicornEffectiveDefend:
    mov rax, qword [r11+confrontState.unicornDefenseGauge]
    test rax, rax
    jz .unicornDefenseGaugeBroken
    dec rax
    mov qword [r11+confrontState.unicornDefenseGauge], rax
    add r12, r12
    .unicornIneffectiveDefend:
    .unicornNoDefend:
    cmp r13, r12
    jbe .unicornHarmProcessed
    sub r13, r12
    test r14, r14
    jnz .attributeMatch
    .attributeMismatch:
    shr r13, 1
    .attributeMatch:
    jmp .applyUnicornHarm
    .unicornDefenseGaugeBroken:
    add r13, r13
    .applyUnicornHarm:
    mov rax, qword [r11+confrontState.unicornHP]
    cmp rax, r13
    jbe .unicornHPZero
    sub rax, r13
    jmp .setUnicornHP
    .unicornHPZero:
    mov rax, 0
    .setUnicornHP:
    mov qword [r11+confrontState.unicornHP], rax
    .unicornHarmProcessed:
    .unicornNotUnderAttack:
    isAdventurerUnderAttack r11
    mov r12, rax
    mov rdi, NOT_UNDER_ATTACK
    cmp rax, rdi
    je .adventurerNotUnderAttack
    .adventurerUnderAttack:
    mov rdi, LOC_NONE
    mov qword [r11+confrontState.unicornAttackBoxLoc], rdi
    mov rax, qword [r11+confrontState.unicornState]
    mov rdi, ATTACK_CLEAR_MASK
    and rax, rdi
    mov qword [r11+confrontState.unicornState], rax
    mov r13, qword [r11+confrontState.unicornAttack]
    mov rdi, qword [r11+confrontState.adventurerState]
    mov rsi, rdi
    and rsi, DEFEND_SET
    jz .adventurerNoDefend
    mov rax, r12
    and rax, 0x10
    jz .adventurerIneffectiveDefend
    and r12, 0xf
    shr rdi, DEFEND_SHIFT
    and r12, rdi
    jz .adventurerIneffectiveDefend
    mov rdi, qword [r11+confrontState.adventurerDefenseGauge]
    test rdi, rdi
    jz .adventurerDefenseGaugeBroken
    mov rax, qword [r11+confrontState.adventurerWeaponIdx]
    mov rdi, SLOT_NONE
    cmp rax, rdi
    je .adventurerDefendWithoutWeapon
    .adventurerDefendWithWeapon:
    lea rdi, [r11+confrontState.adventurerWeapons]
    mov rsi, weaponEntry_size
    mul rsi
    add rax, rdi
    mov rax, qword [rax+weaponEntry.ptr]
    mov r14, qword [rax+weapon.defense]
    add r14, r14
    jmp .adventurerDefenseFetched
    .adventurerDefendWithoutWeapon:
    mov r14, qword [r11+confrontState.adventurerDefense]
    add r14, r14
    jmp .adventurerDefenseFetched
    .adventurerIneffectiveDefend:
    .adventurerNoDefend:
    mov r14, qword [r11+confrontState.adventurerDefense]
    .adventurerDefenseFetched:
    cmp r13, r14
    jbe .adventurerHarmProcessed
    sub r13, r14
    jmp .applyAdventurerHarm
    .adventurerDefenseGaugeBroken:
    add r13, r13
    .applyAdventurerHarm:
    mov rax, qword [r11+confrontState.adventurerHP]
    cmp rax, r13
    jbe .adventurerHPZero
    sub rax, r13
    jmp .setAdventurerHP
    .adventurerHPZero:
    mov rax, 0
    .setAdventurerHP:
    mov qword [r11+confrontState.adventurerHP], rax
    .adventurerHarmProcessed:
    .adventurerNotUnderAttack:
    ;proceed attack boxes
    mov rax, qword [r11+confrontState.adventurerAttackBoxLoc]
    mov rdi, LOC_NONE
    cmp rax, rdi
    je .proceedBox_adventurerIsntAttacking
    .proceedBox_adventurerIsAttacking:
    mov r12, rax
    mov r15, qword [r11+confrontState.adventurerAttackSourceLoc]
    mov rax, qword [r11+confrontState.adventurerWeaponIdx]
    mov rdi, SLOT_NONE
    cmp rax, rdi
    je .proceedBox_adventurerAttackWithoutWeapon
    .proceedBox_adventurerAttackWithWeapon:
    lea rdi, [r11+confrontState.adventurerWeapons]
    mov rsi, weaponEntry_size
    mul rsi
    add rax, rdi
    mov rax, qword [rax+weaponEntry.ptr]
    mov r13, qword [rax+weapon.delta]
    mov r14, qword [rax+weapon.range]
    jmp .proceedBox_checkAdventurerAttackDirection
    .proceedBox_adventurerAttackWithoutWeapon:
    mov r13, BAREHANDED_DELTA
    mov r14, BAREHANDED_RANGE
    .proceedBox_checkAdventurerAttackDirection:
    mov rax, qword [r11+confrontState.adventurerState]
    and rax, 1
    jnz .proceedBox_adventurerAttackTowardRight
    .proceedBox_adventurerAttackTowardLeft:
    cmp r15, r14
    jbe .proceedBox_adventurerAttackLeftLimitAtMin
    .proceedBox_adventurerAttackLeftLimitNotAtMin:
    sub r15, r14
    jmp .proceedBox_checkAdventurerAttackLeftLimit
    .proceedBox_adventurerAttackLeftLimitAtMin:
    mov r15, STAGE_MIN
    .proceedBox_checkAdventurerAttackLeftLimit:
    mov r14, r13
    add r14, r15
    cmp r12, r14
    jbe .proceedBox_adventurerAttackReachedLimit
    .proceedBox_adventurerAttackHasntReachedLeftLimit:
    mov rax, r12
    sub rax, r13
    jmp .proceedBox_setNewAdventurerAttackBox
    .proceedBox_adventurerAttackTowardRight:
    add r15, r14
    cmp r15, STAGE_MAX
    jae .proceedBox_adventurerAttackRightLimitAtMax
    .proceedBox_adventurerAttackRightLimitNotAtMax:
    jmp .proceedBox_checkAdventurerAttackRightLimit
    .proceedBox_adventurerAttackRightLimitAtMax:
    mov r15, STAGE_MAX
    .proceedBox_checkAdventurerAttackRightLimit:
    add r12, r13
    cmp r12, r15
    jae .proceedBox_adventurerAttackReachedLimit
    .proceedBox_adventurerAttackHasntReachedRightLimit:
    mov rax, r12
    jmp .proceedBox_setNewAdventurerAttackBox
    .proceedBox_adventurerAttackReachedLimit:
    mov rax, LOC_NONE
    mov qword [r11+confrontState.adventurerAttackSourceLoc], rax
    mov rdi, qword [r11+confrontState.adventurerState]
    and rdi, ATTACK_CLEAR_MASK
    mov qword [r11+confrontState.adventurerState], rdi
    .proceedBox_setNewAdventurerAttackBox:
    mov qword [r11+confrontState.adventurerAttackBoxLoc], rax
    .proceedBox_adventurerIsntAttacking:
    mov rax, qword [r11+confrontState.unicornAttackBoxLoc]
    mov rdi, LOC_NONE
    cmp rax, rdi
    je .proceedBox_unicornIsntAttacking
    .proceedBox_unicornIsAttacking:
    mov r12, rax
    mov r15, qword [r11+confrontState.unicornAttackSourceLoc]
    mov rax, qword [r11+confrontState.unicornStage]
    cmp rax, UNICORN_STAGE1
    je .proceedBox_unicornStage1
    cmp rax, UNICORN_STAGE2
    je .proceedBox_unicornStage2
    .proceedBox_unicornStage3:
    mov r13, UNICORN_STAGE3_DELTA
    mov r14, UNICORN_STAGE3_RANGE
    jmp .proceedBox_checkUnicornAttackDirection
    .proceedBox_unicornStage2:
    mov r13, UNICORN_STAGE2_DELTA
    mov r14, UNICORN_STAGE2_RANGE
    jmp .proceedBox_checkUnicornAttackDirection
    .proceedBox_unicornStage1:
    mov r13, UNICORN_STAGE1_DELTA
    mov r14, UNICORN_STAGE1_RANGE
    .proceedBox_checkUnicornAttackDirection:
    mov rax, qword [r11+confrontState.unicornState]
    and rax, 1
    jnz .proceedBox_unicornAttackTowardRight
    .proceedBox_unicornAttackTowardLeft:
    cmp r15, r14
    jbe .proceedBox_unicornAttackLeftLimitAtMin
    .proceedBox_unicornAttackLeftLimitNotAtMin:
    sub r15, r14
    jmp .proceedBox_checkUnicornAttackLeftLimit
    .proceedBox_unicornAttackLeftLimitAtMin:
    mov r15, STAGE_MIN
    .proceedBox_checkUnicornAttackLeftLimit:
    mov r14, r13
    add r14, r15
    cmp r12, r14
    jbe .proceedBox_unicornAttackReachedLimit
    .proceedBox_unicornAttackHasntReachedLeftLimit:
    mov rax, r12
    sub rax, r13
    jmp .proceedBox_setNewUnicornAttackBox
    .proceedBox_unicornAttackTowardRight:
    add r15, r14
    cmp r15, STAGE_MAX
    jae .proceedBox_unicornAttackRightLimitAtMax
    .proceedBox_unicornAttackRightLimitNotAtMax:
    jmp .proceedBox_checkUnicornAttackRightLimit
    .proceedBox_unicornAttackRightLimitAtMax:
    mov r15, STAGE_MAX
    .proceedBox_checkUnicornAttackRightLimit:
    add r12, r13
    cmp r12, r15
    jae .proceedBox_unicornAttackReachedLimit
    .proceedBox_unicornAttackHasntReachedRightLimit:
    mov rax, r12
    jmp .proceedBox_setNewUnicornAttackBox
    .proceedBox_unicornAttackReachedLimit:
    mov rax, LOC_NONE
    mov qword [r11+confrontState.unicornAttackSourceLoc], rax
    mov rdi, qword [r11+confrontState.unicornState]
    and rdi, ATTACK_CLEAR_MASK
    mov qword [r11+confrontState.unicornState], rdi
    .proceedBox_setNewUnicornAttackBox:
    mov qword [r11+confrontState.unicornAttackBoxLoc], rax
    .proceedBox_unicornIsntAttacking:
    ;process move actions
    mov rax, qword [r11+confrontState.adventurerState]
    mov r12, rax
    and rax, MOVE_SET
    jz .adventurerNotMoving
    .adventurerIsMoving:
    mov rax, r12
    and rax, MOVE_CLEAR_MASK
    mov qword [r11+confrontState.adventurerState], rax
    mov rax, qword [r11+confrontState.adventurerWeaponIdx]
    mov rdi, SLOT_NONE
    cmp rax, rdi
    je .adventurerMoveWithoutWeapon
    .adventurerMoveWithWeapon:
    lea rdi, [r11+confrontState.adventurerWeapons]
    mov rsi, weaponEntry_size
    mul rsi
    add rax, rdi
    mov rax, qword [rax+weaponEntry.ptr]
    mov rax, qword [rax+weapon.movespeed]
    jmp .checkAdventurerMoveDirection
    .adventurerMoveWithoutWeapon:
    mov rax, BAREHANDED_MOVE_SPEED
    .checkAdventurerMoveDirection:
    mov rdi, qword [r11+confrontState.adventurerLoc]
    mov rsi, ADVENTURER_HALF_SIZE
    shr r12, MOVE_SHIFT
    and r12, 1
    jnz .adventurerMovingRight
    .adventurerMovingLeft:
    add rsi, rax
    cmp rdi, rsi
    jbe .adventurerMoveToMin
    sub rdi, rax
    mov rax, rdi
    jmp .doAdventurerMove
    .adventurerMoveToMin:
    mov rax, ADVENTURER_HALF_SIZE
    jmp .doAdventurerMove
    .adventurerMovingRight:
    mov rdx, STAGE_MAX
    sub rdx, rsi
    add rdi, rax
    cmp rdi, rdx
    jae .adventurerMoveToMax
    mov rax, rdi
    jmp .doAdventurerMove
    .adventurerMoveToMax:
    mov rax, rdx
    .doAdventurerMove:
    mov qword [r11+confrontState.adventurerLoc], rax
    .adventurerNotMoving:
    mov rax, qword [r11+confrontState.unicornState]
    mov r12, rax
    and rax, MOVE_SET
    jz .unicornNotMoving
    .unicornIsMoving:
    mov rax, r12
    and rax, MOVE_CLEAR_MASK
    mov qword [r11+confrontState.unicornState], rax
    mov rax, UNICORN_MOVE_SPEED
    mov rdi, qword [r11+confrontState.unicornLoc]
    mov rsi, UNICORN_HALF_SIZE
    shr r12, MOVE_SHIFT
    and r12 ,1
    jnz .unicornMovingRight
    .unicornMovingLeft:
    add rsi, rax
    cmp rdi, rsi
    jbe .unicornMoveToMin
    sub rdi, rax
    mov rax, rdi
    jmp .doUnicornMove
    .unicornMoveToMin:
    mov rax, UNICORN_HALF_SIZE
    jmp .doUnicornMove
    .unicornMovingRight:
    mov rdx, STAGE_MAX
    sub rdx, rsi
    add rdi, rax
    cmp rdi, rdx
    jae .unicornMoveToMax
    mov rax, rdi
    jmp .doUnicornMove
    .unicornMoveToMax:
    mov rax, rdx
    .doUnicornMove:
    mov qword [r11+confrontState.unicornLoc], rax
    .unicornNotMoving:
    ;update CD
    mov rax, qword [r11+confrontState.adventurerCD]
    test rax, rax
    jz .adventurerZeroCD
    .adventurerNonZeroCD:
    dec rax
    mov qword [r11+confrontState.adventurerCD], rax
    .adventurerZeroCD:
    mov rax, qword [r11+confrontState.unicornCD]
    test rax, rax
    jz .unicornZeroCD
    .unicornNonZeroCD:
    dec rax
    mov qword [r11+confrontState.unicornCD], rax
    .unicornZeroCD:
    ;update defend gauge and clear defend state
    mov rax, qword [r11+confrontState.adventurerState]
    mov rdi, rax
    and rdi, DEFEND_SET
    jnz .adventurerIsDefending
    .adventurerIsNotDefending:
    mov rdi, qword [r11+confrontState.adventurerDefenseGauge]
    mov rsi, ADVENTURER_DEFENSE_GAUGE
    cmp rdi, rsi
    jae .adventurerIsDefending
    inc rdi
    mov qword [r11+confrontState.adventurerDefenseGauge], rdi
    .adventurerIsDefending:
    mov rdi, DEFEND_CLEAR_MASK
    and rax, rdi
    mov qword [r11+confrontState.adventurerState], rax
    mov rax, qword [r11+confrontState.unicornState]
    mov rdi, rax
    and rdi, DEFEND_SET
    jnz .unicornIsDefending
    .unicornIsNotDefending:
    mov rdi, qword [r11+confrontState.unicornDefenseGauge]
    mov rsi, qword [r11+confrontState.unicornStage]
    cmp rsi, UNICORN_STAGE1
    je .unicornDefendStage1GaugeCheck
    cmp rsi, UNICORN_STAGE2
    je .unicornDefendStage2GaugeCheck
    .unicornDefendStage3GaugeCheck:
    mov rsi, UNICORN_STAGE3_DEFENSE_GAUGE
    jmp .unicornDefendGenericGaugeCheck
    .unicornDefendStage2GaugeCheck:
    mov rsi, UNICORN_STAGE2_DEFENSE_GAUGE
    jmp .unicornDefendGenericGaugeCheck
    .unicornDefendStage1GaugeCheck:
    mov rsi, UNICORN_STAGE1_DEFENSE_GAUGE
    .unicornDefendGenericGaugeCheck:
    cmp rdi, rsi
    jae .unicornIsDefending
    inc rdi
    mov qword [r11+confrontState.unicornDefenseGauge], rdi
    .unicornIsDefending:
    mov rdi, DEFEND_CLEAR_MASK
    and rax, rdi
    mov qword [r11+confrontState.unicornState], rax
    .done:
    return
  %endif

_checkConfrontOver:
  ;-------------------------------------------------------
  %ifdef COMMENT
    def checkConfrontOver(confrontState):
      if confrontState.isConfront==0:
        return 0
      if confrontState.unicornHP==0:
        syscall(0xfedcba9876543210)
        exit(0)
      if confrontState.adventurerHP==0:
        return 1
      return 0
  %endif
  ;-------------------------------------------------------
  %ifdef CODE
    mov r11, rdi
    mov rax, qword [r11+confrontState.isConfront]
    test rax, rax
    jz .done
    mov rax, qword [r11+confrontState.unicornHP]
    test rax, rax
    jnz .checkAdventurerDefeated
    mov rax, 0xfedcba9876543210
    syscall
    exit 0
    .checkAdventurerDefeated:
    mov rax, 0
    mov rdi, qword [r11+confrontState.adventurerHP]
    test rdi, rdi
    jnz .done
    .defeated:
    mov rax, 1
    .done:
    return
  %endif

_main:
  ;-------------------------------------------------------
  %ifdef COMMENT
    def main():
      confrontState = getMem()
      resetWeaponMemPool()
      while True:
        actionType = adventurerAction(confrontState)
        if actionType==1:
          break
        if actionType!=2:
          unicornAction(confrontState)
        sendState(confronState)
        if actionType!=2:
          doAction(confrontState)
          if checkConfrontOver(confrontState)!=0:
            break
      write(1,"game over\n",10)
      exit(0)
  %endif
  ;-------------------------------------------------------
  %ifdef CODE
    ;allocate buffer for confront state
    getMem
    resetWeaponMemPool
    .confrontLoop:
      adventurerAction CONFRONT_STATE_ADDR
      mov r11, rax
      cmp r11, 1
      je .done
      cmp r11, 2
      je .skipUnicornAction
      unicornAction CONFRONT_STATE_ADDR
      .skipUnicornAction:
      sendState CONFRONT_STATE_ADDR
      cmp r11, 2
      je .skipDoAction
      doAction CONFRONT_STATE_ADDR
      checkConfrontOver CONFRONT_STATE_ADDR
      test rax, rax
      jnz .done
      .skipDoAction:
      jmp .confrontLoop
    .done:
    write 1, [rel GAME_OVER], 10
    exit 0
  %endif

section .data
align 0x1000, db 0
STACK_SMASHING db "stack smashing detected", 0xa
GAME_OVER db "game over",0xa
