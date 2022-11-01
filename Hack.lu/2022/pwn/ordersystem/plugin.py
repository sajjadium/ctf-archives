'''
This file handles plugins. They can be added to a server instance and
allow for modified behavior such as advanced sorting, server info, remote
access and much more. Due to performance reasons and size constraints, plugins
are pure python bytecode. co_onsts will be pre set by the plugin
handler and supply the plugin with the important values. co_names can be freely
choosen by plugin authors.
'''

from os import path
from types import CodeType

def plugin_log(msg,filename='./log',raw=False):
    mode = 'ab' if raw else 'a'

    with open(filename,mode) as logfile:
        logfile.write(msg)

def execute_plugin(pname,entries):
    plugin_path = path.join('./plugins/',path.basename(pname.rstrip(' ')))

    data = open(plugin_path,'rb').read()

    # the plugin may specify custom names to use as variable storage through
    # the use of ; e.g <bytecode>;name;name1..

    if b';' in data:
        names = [x.decode() for x in data.split(b';')[1:]]
        code = data[:data.index(b';')]
    else:
        code = data
        names = []

    assert len(data) != 0 , "cannot execute empty bytecode"
    assert len(data) % 2 == 0 , "bytecode not correctly aligned"

    # give the plugin some useful data, starting with all saved entries

    consts = []
    for k in entries:
        consts.append(k)


    # in the future we plan to implement more useful functions for plugins to use

    consts.append(plugin_log)

    plugin = CodeType(
        0,                  # co_argcount
        0,                  # co_posonlyargcount
        0,                  # co_kwonlyargcount
        0,                  # co_nlocals
        256,                # co_stacksize
        0,                  # co_flags
        code,               # co_code
        tuple(consts),      # co_consts
        tuple(names),       # co_names
        (),                 # co_varnames
        f'plugin_{pname}',  # co_filename
        f'plugin_{pname}',  # co_name
        0,                  # co_firstlineno
        b'',                # co_linetable
        (),                 # co_freevars
        ()                  # co_cellvars   
    )
    exec(plugin)