#!/usr/bin/env -S python3 -u

import os
import subprocess as sp
from textwrap import dedent


def main():
    msg = dedent(
        """
        Enter assembly code
        Note: replace spaces with underscores, newlines with '|', e.g.,
          main:
            push 5
            call main
        becomes 'main:|push_5|call_main'
        """
    ).strip()
    print(msg)

    asm_code = input()

    input_path = "/tmp/input.asm"
    with open(input_path, "w") as f:
        f.write(asm_code.replace("_", " ").replace("|", "\n"))

    output_path = "/tmp/out.bin"

    p = sp.Popen(
        # Adjust path if running locally
        ["/app/stackception-asm", input_path, output_path],
        stdin=sp.DEVNULL,
        stdout=sp.DEVNULL,
        stderr=sp.PIPE,
    )

    p.wait(timeout=5)
    if p.returncode != 0:
        print("Assembly failed:")
        _, stderr = p.communicate()
        print(stderr.decode())
        exit(1)

    # Adjust path if running locally
    os.execve(
        "/app/stackception",
        ["/app/stackception", output_path],
        {
            "GLIBC_TUNABLES": "glibc.cpu.hwcaps=-ACPI,-ADX,AES,AESKLE,-AMD_IBPB,"
            + "-AMD_IBRS,-AMD_SSBD,-AMD_STIBP,-AMD_VIRT_SSBD,-AMX_BF16,"
            + "-AMX_COMPLEX,-AMX_FP16,-AMX_INT8,-AMX_TILE,-APIC,-APX_F,"
            + "-ARCH_CAPABILITIES,-AVX,-AVX10,-AVX10_XMM,-AVX10_YMM,-AVX10_ZMM,"
            + "-AVX2,-AVX512BW,-AVX512CD,-AVX512DQ,-AVX512ER,-AVX512F,-AVX512PF,"
            + "-AVX512VL,-AVX512_4FMAPS,-AVX512_4VNNIW,-AVX512_BF16,-AVX512_BITALG,"
            + "-AVX512_FP16,-AVX512_IFMA,-AVX512_VBMI,-AVX512_VBMI2,-AVX512_VNNI,"
            + "-AVX512_VP2INTERSECT,-AVX512_VPOPCNTDQ,-AVX_IFMA,-AVX_NE_CONVERT,"
            + "-AVX_VNNI,-AVX_VNNI_INT8,-BMI1,-BMI2,-CLDEMOTE,-CLFLUSHOPT,-CLFSH,"
            + "-CLWB,CMOV,CMPCCXADD,CMPXCHG16B,-CNXT_ID,-CORE_CAPABILITIES,-CX8,"
            + "-DCA,-DE,-DEPR_FPU_CS_DS,-DS,-DS_CPL,-DTES64,-EIST,-ENQCMD,-ERMS,"
            + "-F16C,-FMA,-FMA4,-FPU,-FSGSBASE,-FSRCS,-FSRM,-FSRS,-FXSR,-FZLRM,"
            + "-GFNI,-HLE,-HRESET,-HTT,-HYBRID,-IBRS_IBPB,IBT,-INDEX_1_ECX_16,"
            + "-INDEX_1_ECX_31,-INDEX_1_EDX_10,-INDEX_1_EDX_20,-INDEX_1_EDX_30,"
            + "-INDEX_7_EBX_22,-INDEX_7_EBX_6,-INDEX_7_ECX_13,-INDEX_7_ECX_15,"
            + "-INDEX_7_ECX_16,-INDEX_7_ECX_24,-INDEX_7_ECX_26,-INDEX_7_EDX_0,"
            + "-INDEX_7_EDX_1,-INDEX_7_EDX_12,-INDEX_7_EDX_13,-INDEX_7_EDX_17,"
            + "-INDEX_7_EDX_19,-INDEX_7_EDX_21,-INDEX_7_EDX_6,-INDEX_7_EDX_7,"
            + "-INDEX_7_EDX_9,-INVARIANT_TSC,-INVPCID,-KL,-L1D_FLUSH,-LAHF64_SAHF64,"
            + "-LAM,-LM,-LWP,-LZCNT,-MCA,-MCE,-MD_CLEAR,-MMX,-MONITOR,MOVBE,"
            + "-MOVDIR64B,-MOVDIRI,-MPX,-MSR,-MTRR,NX,-OSPKE,-OSXSAVE,-PAE,"
            + "-PAGE1GB,-PAT,-PBE,-PCID,-PCLMULQDQ,-PCONFIG,-PDCM,-PGE,-PKS,"
            + "-PKU,-POPCNT,-PREFETCHI,-PREFETCHW,-PREFETCHWT1,-PSE,-PSE_36,"
            + "-PSN,-PTWRITE,-RAO_INT,-RDPID,RDRAND,RDSEED,-RDTSCP,-RDT_A,"
            + "-RDT_M,-RTM,-RTM_ALWAYS_ABORT,SDBG,-SEP,SERIALIZE,-SGX,-SGX_LC,"
            + "SHA,SHSTK,SMAP,SMEP,-SMX,-SS,-SSBD,-SSE,-SSE2,-SSE3,-SSE4A,"
            + "-SSE4_1,-SSE4_2,-SSSE3,-STIBP,-SVM,-SYSCALL_SYSRET,-TBM,-TM,-TM2,"
            + "-TRACE,-TSC,-TSC_ADJUST,-TSC_DEADLINE,-TSXLDTRK,-UINTR,-UMIP,"
            + "-VAES,-VME,-VMX,-VPCLMULQDQ,-WAITPKG,-WBNOINVD,-WIDE_KL,-X2APIC,"
            + "-XFD,-XGETBV_ECX_1,-XOP,XSAVE,XSAVEC,-XSAVEOPT,-XSAVES,"
            + "-XTPRUPDCTRL:glibc.cpu.hwcaps_mask=all"
        },
    )


if __name__ == "__main__":
    main()
