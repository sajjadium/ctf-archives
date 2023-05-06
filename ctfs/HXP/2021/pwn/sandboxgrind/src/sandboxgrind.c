#include "pub_tool_basics.h"
#include "pub_tool_libcassert.h"
#include "pub_tool_libcbase.h"
#include "pub_tool_libcprint.h"
#include "pub_tool_machine.h"
#include "pub_tool_tooliface.h"

#define __STRINGIFY(arg) #arg
#define STRINGIFY(arg) __STRINGIFY(arg)

#define SB_(name) sb_ ## name

static void SB_(instrument_fn)(IRSB *sbOut, const HChar *name, void *addr, IRExpr *guard, HWord args)
{
    IRExpr **argv = mkIRExprVec_1(mkIRExpr_HWord(args));
    IRDirty *di = unsafeIRDirty_0_N(1, name, VG_(fnptr_to_fnentry)(addr), argv);
    if (guard)
        di->guard = guard;
    addStmtToIRSB(sbOut, IRStmt_Dirty(di));
}

#define SB_INSTRUMENT_FN(sbOut, fn, guard, args) \
    SB_(instrument_fn)((sbOut), STRINGIFY(fn), (void *) (&fn), (guard), (args))

static void VG_REGPARM(1) SB_(illegal)(HWord reason)
{
    // Note the abort, and exit
    if (reason >= (HWord) Ijk_INVALID) {
        VG_(printf)("Encountered illegal operation: ");
        ppIRJumpKind((IRJumpKind) reason);
        VG_(printf)("\n");
    } else {
        VG_(printf)("Encountered illegal operation\n");
    }
    VG_(exit)(0);
}

static void SB_(instrument_jump)(IRSB *sbOut, IRJumpKind jk, IRExpr *dst, IRExpr *guard)
{
    switch (jk) {
    case Ijk_Boring:
    case Ijk_Call:
    case Ijk_Ret:
    case Ijk_Yield:
        return; // Ignore "normal" jumps and calls
    // For some reason, IRJumpKind has a ton of syscalls, but we don't allow any of them. Same goes
    // for any emulation errors and invalid instructions. We don't abort here, because they may still
    // be unreachable (we need to evaluate the guard expression first).
    default:
        SB_INSTRUMENT_FN(sbOut, SB_(illegal), guard, jk); // Abort on invalid instructions and emulation errors
        return;
    }
}

static void SB_(instrument_dirty_call)(IRSB *sbOut, IRCallee *cee, IRExpr *guard)
{
    // If Valgrind thinks something is too difficult to JIT, it turns it into a Dirty call
    // We capture those as well, of course.
    // However, they don't actually happen all that often, so we just have a list of allowed targets.
#define SB_CHECK_CALLEE(cee, fn) \
    do { \
        extern void fn(void); /* Signature is probably wrong, but we only need the address, and in C there is no name mangling */ \
        if (VG_(strcmp)(STRINGIFY(fn), cee->name) == 0 && cee->addr == VG_(fnptr_to_fnentry)(fn)) \
            return; \
    } while (0)

    SB_CHECK_CALLEE(cee, amd64g_dirtyhelper_AES);
    SB_CHECK_CALLEE(cee, amd64g_dirtyhelper_AESKEYGENASSIST);
    SB_CHECK_CALLEE(cee, amd64g_dirtyhelper_CPUID_avx2);
    SB_CHECK_CALLEE(cee, amd64g_dirtyhelper_CPUID_avx_and_cx16);
    SB_CHECK_CALLEE(cee, amd64g_dirtyhelper_CPUID_baseline);
    SB_CHECK_CALLEE(cee, amd64g_dirtyhelper_CPUID_sse3_and_cx16);
    SB_CHECK_CALLEE(cee, amd64g_dirtyhelper_CPUID_sse42_and_cx16);
    SB_CHECK_CALLEE(cee, amd64g_dirtyhelper_FINIT);
    SB_CHECK_CALLEE(cee, amd64g_dirtyhelper_FLDENV);
    SB_CHECK_CALLEE(cee, amd64g_dirtyhelper_FNSAVE);
    SB_CHECK_CALLEE(cee, amd64g_dirtyhelper_FNSAVES);
    SB_CHECK_CALLEE(cee, amd64g_dirtyhelper_FRSTOR);
    SB_CHECK_CALLEE(cee, amd64g_dirtyhelper_FRSTORS);
    SB_CHECK_CALLEE(cee, amd64g_dirtyhelper_FSTENV);
    SB_CHECK_CALLEE(cee, amd64g_dirtyhelper_IN);
    SB_CHECK_CALLEE(cee, amd64g_dirtyhelper_loadF80le);
    SB_CHECK_CALLEE(cee, amd64g_dirtyhelper_OUT);
    SB_CHECK_CALLEE(cee, amd64g_dirtyhelper_PCMPxSTRx);
    SB_CHECK_CALLEE(cee, amd64g_dirtyhelper_RDRAND);
    SB_CHECK_CALLEE(cee, amd64g_dirtyhelper_RDTSC);
    SB_CHECK_CALLEE(cee, amd64g_dirtyhelper_RDTSCP);
    SB_CHECK_CALLEE(cee, amd64g_dirtyhelper_storeF80le);
    SB_CHECK_CALLEE(cee, amd64g_dirtyhelper_SxDT);
    SB_CHECK_CALLEE(cee, amd64g_dirtyhelper_XRSTOR_COMPONENT_0);
    SB_CHECK_CALLEE(cee, amd64g_dirtyhelper_XRSTOR_COMPONENT_1_EXCLUDING_XMMREGS);
    SB_CHECK_CALLEE(cee, amd64g_dirtyhelper_XSAVE_COMPONENT_0);
    SB_CHECK_CALLEE(cee, amd64g_dirtyhelper_XSAVE_COMPONENT_1_EXCLUDING_XMMREGS);

    SB_INSTRUMENT_FN(sbOut, SB_(illegal), guard, 0);
}

static IRSB* SB_(instrument)(VgCallbackClosure *closure,
                             IRSB *bb,
                             const VexGuestLayout *layout,
                             const VexGuestExtents *vge,
                             const VexArchInfo *archinfo_host,
                             IRType gWordTy,
                             IRType hWordTy)
{
    IRSB* sbOut = deepCopyIRSBExceptStmts(bb);

    for (Int i = 0; i < bb->stmts_used; i++) {
        IRStmt* st = bb->stmts[i];
        switch (st->tag) {
        case Ist_Dirty:
            // Call to a C helper function
            SB_(instrument_dirty_call)(sbOut, st->Ist.Dirty.details->cee, st->Ist.Dirty.details->guard);
            break;
        case Ist_Exit:
            // (Conditional) exit from BB
            SB_(instrument_jump)(sbOut, st->Ist.Exit.jk, IRExpr_Const(st->Ist.Exit.dst), st->Ist.Exit.guard);
            break;
        default:
            break;
        }
        addStmtToIRSB(sbOut, st);
    }
    SB_(instrument_jump)(sbOut, bb->jumpkind, bb->next, NULL);
    return sbOut;
}

static void SB_(post_clo_init)(void) {}
static void SB_(fini)(Int exitcode) {}

static void SB_(pre_clo_init)(void)
{
    VG_(details_name)("sandboxgrind");
    VG_(details_version)(NULL);
    VG_(details_description)("a valgrind sandbox");
    VG_(details_copyright_author)("Copyright (C) 2021 hxp");
    VG_(details_bug_reports_to)("#hxpctf");
    VG_(basic_tool_funcs)(SB_(post_clo_init), SB_(instrument), SB_(fini));
}

VG_DETERMINE_INTERFACE_VERSION(SB_(pre_clo_init))
