#    debug.py: companion debug tool for hardskull
#
#    Copyright (C) 2021 theKidOfArcrania
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import gdb

#################################
#
# Usage: This contains two commands for dumping the stack and
# any heap objects. This has dependency on gef :P sorry...
#
# Add this file by running `source debug.py`.
#
# Note: ddo/ds might break horrendously in some cases, namingly:
# 1) if you hook on certain runtime functions that the dumpObj function calls
# 2) if you are in `target record` mode.
#
# ddo <expr_with_no_spaces>   -- dumps a heap object at the address specified
#                                by the expression
# ds [<expr_with_no_spaces>]  -- dumps the current stack pointed to by $rbp
#                                or optionally whatever expression is given
#
#

t_voidp = gdb.lookup_type('void').pointer()
t_voidpp = t_voidp.pointer()


@register_command
class DumpStack(GenericCommand):
    ""
    _cmdline_ = "dump-stack"
    _syntax_  = ""
    _aliases_ = ["ds",]

    @only_if_gdb_running
    def do_invoke(self, argv):
        fra = gdb.selected_frame()
        if len(argv) > 0:
            stack = gdb.parse_and_eval(argv[0]).cast(t_voidpp)
        else:
            stack = fra.read_register('rbp').cast(t_voidpp)

        try:
            for ptr in range(100):
                val = stack[ptr]
                addr = int(stack + ptr)
                print(f'\x1b[33m{addr:016x}\x1b[m')
                dump_value(val)
        except gdb.MemoryError:
            print('\x1b[31m<EndOfMemory>\x1b[m')


class DumpObject(GenericCommand):
    ""
    _cmdline_ = "dump-object"
    _syntax_  = "<value>"

    @only_if_gdb_running
    def do_invoke(self, argv):
        if len(argv) == 0:
            print('Need value to dump')
            return
        dump_value(gdb.parse_and_eval(argv[0]))


def dump_value(val):
    info = lookup_address(int(val))
    if info.is_in_text_segment():
        print(str(val.cast(t_voidp)))
    elif info.valid:
        # TODO: better dump object
        gdb.execute(f'call (void)dumpObject({int(val)})')
    else:
        print(str(val))

DumpStack()
DumpObject()
gdb.execute('alias ds = dump-stack')
gdb.execute('alias ddo = dump-object')
