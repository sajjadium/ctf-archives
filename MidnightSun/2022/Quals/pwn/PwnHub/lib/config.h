/* config.h.  Generated from config.h.in by configure.  */
/* Define if building with SELinux support.  Set by --with-selinux.  */
/* #undef HAVE_SELINUX */

/* Defined if building with SELinux support & audit libs are detected. */
/* #undef HAVE_LIBAUDIT */

/* Defined if building with SELinux support & libcap libs are detected.  */
/* #undef HAVE_LIBCAP */

/* Define to the assembler line separator character for multiple
   assembler instructions per line.  Default is `;'  */
/* #undef ASM_LINE_SEP */

/* Define if __attribute__((section("foo"))) puts quotes around foo.  */
/* #undef HAVE_SECTION_QUOTES */

/* Define if the assembler supports the `.set' directive.  */
#define HAVE_ASM_SET_DIRECTIVE 1

/* On powerpc64, use overlapping .opd entries.  */
/* #undef USE_PPC64_OVERLAPPING_OPD */

/* Define if _Unwind_Find_FDE should be exported from glibc.  */
/* #undef EXPORT_UNWIND_FIND_FDE */

/* Define if static NSS modules are wanted.  */
/* #undef DO_STATIC_NSS */

/* Assume that the compiler supports __builtin_expect.
   This macro is necessary for proper compilation of code
   shared between GNU libc and GNU gettext projects.  */
#define HAVE_BUILTIN_EXPECT 1

/* Define if the compiler supports __builtin_memset.  */
#define HAVE_BUILTIN_MEMSET 1

/* Define if compiler accepts -ftree-loop-distribute-patterns.  */
#define HAVE_CC_INHIBIT_LOOP_TO_LIBCALL 1

/* Define if compiler accepts -fno-stack-protector in an
   __attribute__ ((__optimize__)).  */
#define HAVE_CC_NO_STACK_PROTECTOR 1

/* The level of stack protection in use for glibc as a whole.
   May be overridden on a file-by-file basis.  */
#ifndef STACK_PROTECTOR_LEVEL
#define STACK_PROTECTOR_LEVEL 3
#endif

/* Define if the linker supports the -z combreloc option.  */
#define HAVE_Z_COMBRELOC 1

/* Define if _rtld_local structure should be forced into .sdata section.  */
/* #undef HAVE_SDATA_SECTION */

/* Define if compiler supports AVX512.  */
#define HAVE_AVX512_SUPPORT 1

/* Define if assembler supports AVX512DQ.  */
#define HAVE_AVX512DQ_ASM_SUPPORT 1

/* Define if assembler supports z10 zarch instructions as default on S390.  */
/* #undef HAVE_S390_MIN_Z10_ZARCH_ASM_SUPPORT */

/* Define if assembler supports z196 zarch instructions as default on S390.  */
/* #undef HAVE_S390_MIN_Z196_ZARCH_ASM_SUPPORT */

/* Define if assembler supports z13 zarch instructions as default on S390.  */
/* #undef HAVE_S390_MIN_Z13_ZARCH_ASM_SUPPORT */

/* Define if assembler supports arch13 zarch instruction as default on S390.  */
/* #undef HAVE_S390_MIN_ARCH13_ZARCH_ASM_SUPPORT */

/* Define if assembler supports vector instructions on S390.  */
/* #undef HAVE_S390_VX_ASM_SUPPORT */

/* Define if gcc supports vector registers as clobbers in inline assembly
   on S390.  */
/* #undef HAVE_S390_VX_GCC_SUPPORT */

/* Define if assembler supports arch13 instructions on S390.  */
/* #undef HAVE_S390_ARCH13_ASM_SUPPORT */

/* Define if assembler supports Intel MPX.  */
#define HAVE_MPX_SUPPORT 1

/* Define if the compiler\'s exception support is based on libunwind.  */
/* #undef HAVE_CC_WITH_LIBUNWIND */

/* Define if the access to static and hidden variables is position independent
   and does not need relocations.  */
#define PI_STATIC_AND_HIDDEN 1

/* Define this to disable the 'hidden_proto' et al macros in
   include/libc-symbols.h that avoid PLT slots in PIE.  */
/* #undef NO_HIDDEN_EXTERN_FUNC_IN_PIE */

/* Define this to disable the 'hidden_proto' et al macros in
   include/libc-symbols.h that avoid PLT slots in the shared objects.  */
/* #undef NO_HIDDEN */

/* Define this to disable in rtld the 'hidden_proto' et al macros in
   include/libc-symbols.h that avoid PLT slots in the shared objects.  */
/* #undef NO_RTLD_HIDDEN */

/* Define this to disable lazy relocations in DSOs.  */
/* #undef BIND_NOW */

/* AArch64 big endian ABI */
/* #undef HAVE_AARCH64_BE */

/* C-SKY ABI version.  */
/* #undef CSKYABI */

/* C-SKY floating-point ABI.  */
/* #undef CSKY_HARD_FLOAT */

/* RISC-V integer ABI for ld.so.  */
/* #undef RISCV_ABI_XLEN */

/* RISC-V floating-point ABI for ld.so.  */
/* #undef RISCV_ABI_FLEN */

/* Linux specific: minimum supported kernel version.  */
#define __LINUX_KERNEL_VERSION (3 * 65536 + 2 * 256 + 0)

/* kFreeBSD specific: minimum supported kernel version.  */
/* #undef __KFREEBSD_KERNEL_VERSION */

/* Override abi-tags ABI version if necessary.  */
#define __ABI_TAG_VERSION 3,2,0

/* Mach/Hurd specific: define if mig supports the `retcode' keyword.  */
/* #undef HAVE_MIG_RETCODE */

/* Mach specific: define if the `host_page_size' RPC is available.  */
/* #undef HAVE_HOST_PAGE_SIZE */

/* Mach/i386 specific: define if the `i386_io_perm_*' RPCs are available.  */
/* #undef HAVE_I386_IO_PERM_MODIFY */

/* Mach/i386 specific: define if the `i386_set_gdt' RPC is available.  */
/* #undef HAVE_I386_SET_GDT */

/* Define if inlined system calls are available.  */
#define HAVE_INLINED_SYSCALLS 1

/* Define if your compiler defaults to -msecure-plt mode on ppc.  */
/* #undef HAVE_PPC_SECURE_PLT */

/* Define if __stack_chk_guard canary should be randomized at program startup.  */
#define ENABLE_STACKGUARD_RANDOMIZE 1

/* Package description.  */
#define PKGVERSION "(GNU libc) "

/* Bug reporting address.  */
#define REPORT_BUGS_TO "<https://www.gnu.org/software/libc/bugs.html>"

/* Define if multi-arch DSOs should be generated.  */
#define USE_MULTIARCH 1

/* Define if `.ctors' and `.dtors' sections shouldn't be used.  */
#define NO_CTORS_DTORS_SECTIONS 1

/* Define if obsolete RPC code should be made available for user-level code
   to link against.  */
#define LINK_OBSOLETE_RPC 1

/* Define if obsolete libnsl code should be made available for user-level
   code to link against.  */
#define LINK_OBSOLETE_NSL 1

/* Define if Systemtap <sys/sdt.h> probes should be defined.  */
/* #undef USE_STAP_PROBE */

/* Define if library functions should try to contact the nscd daemon.  */
#define USE_NSCD 1

/* Define if the dynamic linker should consult an ld.so.cache file.  */
#define USE_LDCONFIG 1

/* Define to 1 if STT_GNU_IFUNC support actually works.  */
#define HAVE_IFUNC 1

/* Define if gcc supports attribute ifunc.  */
#define HAVE_GCC_IFUNC 1

/* Define if the linker defines __ehdr_start.  */
#define HAVE_EHDR_START 1

/*
 */

#ifndef	_LIBC

/* These symbols might be defined by some sysdeps configures.
   They are used only in miscellaneous generator programs, not
   in compiling libc itself.   */

/* sysdeps/generic/configure.ac */
/* #undef HAVE_PSIGNAL */

/* sysdeps/unix/configure.ac */
/* #undef HAVE_STRERROR */

/* sysdeps/unix/common/configure.ac */
/* #undef HAVE_SYS_SIGLIST */
/* #undef HAVE__SYS_SIGLIST */
/* #undef HAVE__CTYPE_ */
/* #undef HAVE___CTYPE_ */
/* #undef HAVE___CTYPE */
/* #undef HAVE__CTYPE__ */
/* #undef HAVE__CTYPE */
/* #undef HAVE__LOCP */

#endif

/*
 */

#ifdef	_LIBC

/* The zic and zdump programs need these definitions.  */

#define	HAVE_STRERROR	1

/* The locale code needs these definitions.  */

#define HAVE_REGEX 1

/* The ARM hard-float ABI is being used.  */
/* #undef HAVE_ARM_PCS_VFP */

/* The ARM movw/movt instructions using PC-relative relocs work right.  */
#define ARM_PCREL_MOVW_OK 0

/* The pt_chown binary is being built and used by grantpt.  */
#define HAVE_PT_CHOWN 0

/* Define if the compiler supports __builtin_trap without
   any external dependencies such as making a function call.  */
#define HAVE_BUILTIN_TRAP 1

/* ports/sysdeps/mips/configure.in  */
/* Define if using the IEEE 754-2008 NaN encoding on the MIPS target.  */
/* #undef HAVE_MIPS_NAN2008 */

/* The PowerPC64 ELFv2 ABI is being used.  */
/* #undef HAVE_ELFV2_ABI */

/* PowerPC32 uses fcfid for integer to floating point conversions.  */
#define HAVE_PPC_FCFID 0

/* PowerPC32 uses fctidz for floating point to long long conversions.  */
#define HAVE_PPC_FCTIDZ 0

/* Build glibc with tunables support.  */
#define HAVE_TUNABLES 0

/* Define if static PIE is enabled.  */
#define ENABLE_STATIC_PIE 0

/* Some compiler options may now allow to use ebp in __asm__ (used mainly
   in i386 6 argument syscall issue).  */
#define CAN_USE_REGISTER_ASM_EBP 0

#endif
