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

#ifndef hypersecure_DEBUG_H
#define hypersecure_DEBUG_H

#include "hypersecure.h"

void hypersecure_log_msg(const char *format, ...);

void hypersecure_dump_vmcb(struct hypersecure_vmcb *vmcb);

void hypersecure_run_tests(struct hypersecure_context *ctx);

void hypersecure_dump_regs(const struct hypersecure_vm_state *state);

#endif // hypersecure_DEBUG_H
