// Copyright (C) 2022? 2023? hxp. License expires after HXP CTF 2022
//
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with this program.  If not, see <https://www.gnu.org/licenses/>.

#ifndef hypersecure_EXIT_CODES_H
#define hypersecure_EXIT_CODES_H

enum hypersecure_EXITCODE {
	hypersecure_EXITCODE_VMEXIT_INVALID = -1,
	hypersecure_EXITCODE_VMEXIT_BUSY = -2,
	hypersecure_EXITCODE_VMEXIT_EXCP_0 = 0x40,
	hypersecure_EXITCODE_VMEXIT_EXCP_1,
	hypersecure_EXITCODE_VMEXIT_EXCP_2,
	hypersecure_EXITCODE_VMEXIT_EXCP_3,
	hypersecure_EXITCODE_VMEXIT_EXCP_4,
	hypersecure_EXITCODE_VMEXIT_EXCP_5,
	hypersecure_EXITCODE_VMEXIT_EXCP_6,
	hypersecure_EXITCODE_VMEXIT_EXCP_7,
	hypersecure_EXITCODE_VMEXIT_EXCP_8,
	hypersecure_EXITCODE_VMEXIT_EXCP_9,
	hypersecure_EXITCODE_VMEXIT_EXCP_10,
	hypersecure_EXITCODE_VMEXIT_EXCP_11,
	hypersecure_EXITCODE_VMEXIT_EXCP_12,
	hypersecure_EXITCODE_VMEXIT_EXCP_13,
	hypersecure_EXITCODE_VMEXIT_EXCP_14,
	hypersecure_EXITCODE_VMEXIT_EXCP_15,

	hypersecure_EXITCODE_VMEXIT_RDTSC = 0x6E,
	hypersecure_EXITCODE_VMEXIT_HLT = 0x78,
	hypersecure_EXITCODE_VMEXIT_VMMCALL = 0x81,
	hypersecure_EXITCODE_VMEXIT_RDTSCP = 0x87,
	hypersecure_EXITCODE_VMEXIT_CPUID = 0x72,

	hypersecure_EXITCODE_VMEXIT_SHUTDOWN = 0x7f,

	hypersecure_EXITCODE_VMEXIT_NPF = 0x400,
};

static inline const char *translate_hypersecure_exitcode_to_str(const enum hypersecure_EXITCODE exitcode) {
#define p(X) \
	case X: \
		return #X

	switch (exitcode) {
	p(hypersecure_EXITCODE_VMEXIT_INVALID);
	p(hypersecure_EXITCODE_VMEXIT_BUSY);
	p(hypersecure_EXITCODE_VMEXIT_SHUTDOWN);
	p(hypersecure_EXITCODE_VMEXIT_EXCP_0);
	p(hypersecure_EXITCODE_VMEXIT_EXCP_1);
	p(hypersecure_EXITCODE_VMEXIT_EXCP_2);
	p(hypersecure_EXITCODE_VMEXIT_EXCP_3);
	p(hypersecure_EXITCODE_VMEXIT_EXCP_4);
	p(hypersecure_EXITCODE_VMEXIT_EXCP_5);
	p(hypersecure_EXITCODE_VMEXIT_EXCP_6);
	p(hypersecure_EXITCODE_VMEXIT_EXCP_7);
	p(hypersecure_EXITCODE_VMEXIT_EXCP_8);
	p(hypersecure_EXITCODE_VMEXIT_EXCP_9);
	p(hypersecure_EXITCODE_VMEXIT_EXCP_10);
	p(hypersecure_EXITCODE_VMEXIT_EXCP_11);
	p(hypersecure_EXITCODE_VMEXIT_EXCP_12);
	p(hypersecure_EXITCODE_VMEXIT_EXCP_13);
	p(hypersecure_EXITCODE_VMEXIT_EXCP_14);
	p(hypersecure_EXITCODE_VMEXIT_EXCP_15);
	p(hypersecure_EXITCODE_VMEXIT_HLT);
	p(hypersecure_EXITCODE_VMEXIT_VMMCALL);
	p(hypersecure_EXITCODE_VMEXIT_RDTSC);
	p(hypersecure_EXITCODE_VMEXIT_RDTSCP);
	p(hypersecure_EXITCODE_VMEXIT_CPUID);
	p(hypersecure_EXITCODE_VMEXIT_NPF);
	default:
		return "unkown";
	};

#undef p
}

enum hypersecure_EXCEPTION {
#define p(X) hypersecure_EXCEPTION_ ## X
	p(DE) = 0U, // Divide by zero
	p(DB),      // Debug
	p(NMI),     // Non-maskable interrupt
	p(BP),      // Breakpoint
	p(OF),      // Overflow
	p(BR),      // Bound Range Exceeded
	p(UD),      // Invalid opcode
	p(NM),      // Device not available
	p(DF),      // Double fault
	p(CSO),     // Coprocessor segment overrun
	p(TS),      // Invalid TSS
	p(NP),      // Segment Not Present
	p(SS),      // Stack Segment Overflow
	p(GP),      // General-protection Fault
	p(PF),      // Page Fault
	p(MF) = 0x10U, // x86 floating-point exception
	p(AC), // Alignment check
	p(MC), // Machine check
	p(XF), // SIMD floating-point exception
	p(VE), // Virtualization exception
	p(SX) = 0x1FU, // Security exception
#undef p
};

static inline const char *translate_hypersecure_exception_number_to_str(const enum hypersecure_EXCEPTION excp) {
#define p(X) \
	case hypersecure_EXCEPTION_ ## X: \
		return #X " exception"
	switch(excp) {
	p(DE);
	p(DB);
	p(NMI);
	p(BP);
	p(OF);
	p(BR);
	p(UD);
	p(NM);
	p(DF);
	p(CSO);
	p(TS);
	p(NP);
	p(SS);
	p(GP);
	p(PF);
	p(MF);
	p(AC);
	p(MC);
	p(XF);
	p(VE);
	p(SX);
	default:
		return "unknown";
	}
#undef p
}

#endif // hypersecure_EXIT_CODES_H
