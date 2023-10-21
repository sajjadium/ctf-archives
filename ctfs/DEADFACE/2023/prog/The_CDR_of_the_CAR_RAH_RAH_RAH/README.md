TheZeal0t prog

Created by: TheZeal0t

The LISP programming language (which stands for “Lots of Insane and Stupid Parentheses”) was used as an early form of list processing. There was even a “LISP COMPUTER” where the assembly language was LISP!

LISP was famous (infamous?) for its numerous parentheses. Miss one, and the whole program fails!

LISP had among its data types “atoms” (single items) and “lists” (multiple items), formatted like this:

(apple tomato (grape bear (banana)) ((President Trump),(President Obama)))

Two of LISP’s most famous functions were car (which returns the first item in a list), and cdr (which returns all but the first item in a list). They could be used, together with recursion, to perform loops. In fact, early LISP had no native looping structure other than recursion.

Attached to this challenge is a flat list of words. To obtain the flag, create a program in Python that calls emulated car and cdr functions (already provided for you) to produce the correct list. The list has to be grouped into a list of atoms and lists such that the program, as described by the Lytton, IN High School Basketball Cheerleaders, produces the correct list. Use their cheer to lay out the function calls in a series of nested calls…

The cheer goes like this:

The CDR (1) of the CAR!
The CDR of the CAR!
The CAR of the CDR of the CDR  of the CAR!
The CAR of the CDR of the CDR of the CAR (12)!

Hence, the first CDR (1) is the outermost call, and the CAR (12) is the innermost call. The single parameter is the complete list of words in the wordlist, grouped appropriately to produce the output list.

(1)                 (12)
cdr(car(cdr(car...  car(('fish', ('vermin','blatant',('ascent'...))))

Here is the input wordlist as a flat list, without grouping, as well as the expected output and instructions for submitting your answer to obtain the flag.
