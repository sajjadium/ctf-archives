import sys
from keyword import iskeyword
from keyword import issoftkeyword
from os import environ


print(
    '''

     ..                                       .          ..       ..               .x+=:.
  :**888H: `: .xH""              .uef^"      @88>  x .d88"  x .d88"               z`    ^%
 X   `8888k XX888              :d88E         %8P    5888R    5888R                   .   <k
'8hx  48888 ?8888          .   `888E          .     '888R    '888R        .u       .@8Ned8"
'8888 '8888 `8888     .udR88N   888E .z8k   .@88u    888R     888R     ud8888.   .@^%8888"
 %888>'8888  8888    <888'888k  888E~?888L ''888E`   888R     888R   :888'8888. x88:  `)8b.
   "8 '888"  8888    9888 'Y"   888E  888E   888E    888R     888R   d888 '88%" 8888N=*8888
  .-` X*"    8888    9888       888E  888E   888E    888R     888R   8888.+"     %8"    R88
    .xhx.    8888    9888       888E  888E   888E    888R     888R   8888L        @8Wou 9%
  .H88888h.~`8888.>  ?8888u../  888E  888E   888&   .888B .  .888B . '8888c. .+ .888888P`
 .~  `%88!` '888*~    "8888P'  m888N= 888>   R888"  ^*888%   ^*888%   "88888%   `   ^"F
       `"     ""        "P'     `Y"   888     ""      "%       "%       "YP'
                                     J88"
                                     @%
                                   :"

'''
)


def retreat():
    print('Better be a late learner than an ignorant..')


def conquer():
    print('Ten soldiers wisely led will beat a hundred without a head..')
    print(environ['FLAG'])


function = input('What would a wise polemarch do? [retreat / conquer] ')

if not function.isidentifier():
    sys.exit(f'Invalid identifier: {function!r}')
elif iskeyword(function) or issoftkeyword(function):
    sys.exit(f'Reserved identifier: {function!r}')
elif function == 'conquer':
    sys.exit('Option [conquer] is temporarily unavailable!')

try:
    global_variables = {
        '__builtins__': {},
        'retreat': retreat,
        'conquer': conquer,
    }

    eval(f'{function}()', global_variables)
except NameError:
    sys.exit(f'Option [{function}] is not available!')
