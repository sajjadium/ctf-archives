An ARM and a leg
This challenge is compiled for the ARM architecture because why not

The app tries to read something from somewhere

The structure of the app is the following (pseudocode):

var param1 = SOME_CONSTANT
var param2old = ...
var param3old = ...
var param2 = encode(param2old)
var param3 = encode(param3old)
functionName(param1, param2, param3)
encode is not a system function, it's something done by the binary

Flag format: TFCCTF{functionName_param1constant_param1value_param2old_param2_param3old_param3}

Note that the first parameter is a number, but also a constant relevant to the function. You should write the constant's value in base 10 (get it from MSDN)

You do not need to run the program. Everything can be done by analysing the binary

Example based on the notes above (not actual code in the app)
Based on the statements above, if the function is called like this:

SIZE_T
Encode(SIZE_T n)
{
return n ^ 123;
}

VirtualAlloc(NULL, Encode(0x1000), MEM_RESERVE, PAGE_READWRITE);
...and the compiled call is

VirtualAlloc(0, 4219, 0x00002000, 0x04)
...then the flag would be: TFCCTF{VirtualAlloc_NULL_0_4096_4219_MEM_RESERVE_8192_PAGE_READWRITE_4}
