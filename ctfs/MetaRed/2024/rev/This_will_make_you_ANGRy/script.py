import angr
import #Find the library that allows to create symbolic variables

# Load the binary
project = angr.Project('/paht/to/angry binary', auto_load_libs=False) 

# Length of the argument
argument_length = #Complete with the length of the argument  

# Create a symbolic variable of size argument_length for argument, each character is 8 bits
argument = #"library that allows to create symbolic variables".BVS('argument', 8 * argument_length)

# Define the initial state with the symbolic argument
# Add options to remove annoying warnings of angr
initial_state = project.factory.entry_state(args=['./angry', argument],
                                            add_options ={
        angr.options.SYMBOL_FILL_UNCONSTRAINED_MEMORY,
        angr.options.SYMBOL_FILL_UNCONSTRAINED_REGISTERS
    })

# Constrain each byte of the input to be a printable character
for byte in argument.chop(8):
    initial_state.solver.add(byte >= X)  # Replace X with the hex value of first printable character
    initial_state.solver.add(byte <= Y)  # Replace Y with the hex value of last printable character

# Define the success condition
def is_successful(state):
    stdout_output = state. #Find the attribute that contains the output of the binary in Angr
    return b'X' in stdout_output #Replace X with the message that indicates success

# Define the failure condition
def should_abort(state):
    stdout_output = state. #Find the attribute that contains the output of the binary in Angr
    return b'Y!' in stdout_output #Replace Y with the message that indicates failure

# Define the simulation manager
simgr = project.factory.simulation_manager(initial_state)

# Explore the binary looking for a solution
print("Exploring...")
simgr.explore(find=is_successful, avoid=should_abort)

# Check if we found a solution
if simgr.found:
    solution_state = simgr.found[0]
    solution = solution_state.Z(argument, cast_to=bytes) #Replace Z with the evaluation of a symbolic expression.
    print(f"Found the solution: {solution.decode()}")
else:
    print("Could not find the solution.")
