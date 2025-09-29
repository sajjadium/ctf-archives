PEGASUS File Format
=====

**P**ortable
**E**xecutable
**G**eneric
**A**rchitecture
**S**upporting
**U**nusual
**S**ystems


```c
/*
An lestring is a length encoded string type. The low 7 bits of each byte hold
data, and the high bit is a continuation bit. When the continuation bit is set,
then there is another byte after this one in the string. An lestring ends with
a byte whose top bit is clear.
*/

// File header at the beginning of every PEGASUS file
struct Pegasus_Header {
	char magic[8] = "\xe4PEGASUS";  // Fixed value to mark the beginning of a PEGASUS file
	char arch[4];                   // Defines the required CPU architecture and version. EARv3: "EAR3"
	uint16_t cmd_count;             // Total number of load commands in this PEGASUS file
	Pegasus_Cmd cmds[ncmds];        // Array of load commands. Each element is variable sized
};

// Start of every PEGASUS load command
struct Pegasus_Cmd {
	uint16_t cmd_size;              // Number of bytes in this load command, including sizeof(Pegasus_Cmd)
	uint16_t cmd_type;              // Selects which specific type of load command this is
};

// Map a segment from the PEGASUS file into memory
// cmd_type = 1
struct Pegasus_Segment: Pegasus_Cmd {
	uint8_t virtual_page;           // Virtual page number where the segment should be mapped
	uint8_t file_page;              // Page index within the file where the segment data is found
	uint8_t present_page_count;     // Number of pages to map from the file
	uint8_t absent_page_count;      // Number of extra RAM pages to map
	EAR_Protection prot;            // Bitmask of memory protections to apply
	lestring name;                  // Name of the segment such as @TEXT
};

// Sets the values of these registers when starting execution
// cmd_type = 2
struct Pegasus_Entrypoint: Pegasus_Cmd {
	uint16_t A0, A1, A2, A3, A4, A5, S0, S1, S2, FP, SP, RA, RD, PC, DPC;
};

// Describes the location and size of the symbol table in this PEGASUS file
// cmd_type = 3
struct Pegasus_SymbolTable: Pegasus_Cmd {
	uint16_t sym_count;             // Total number of symbols in the symbol table
	Pegasus_Symbol syms[sym_count]; // List of symbols in the symbol table
};

// Defines a single symbol's value
struct Pegasus_Symbol {
	uint16_t value;                 // Value of the symbol (usually a virtual address), or 0xFFFF for imported symbols
	lestring name;                  // Name of the symbol, w/o the '@' prefix
};

// Defines a table of relocation entries to apply during load
// cmd_type = 4
struct Pegasus_RelocTable: Pegasus_Cmd {
	uint16_t reloc_count;                    // Total number of relocation entries in the table
	Pegasus_Relocation relocs[reloc_count];  // Array of relocation entries
};

// Describes a single relocation that should be applied during load
struct Pegasus_Relocation {
	uint16_t symbol_index;          // Index into the symbol table to use as the relocation value
	uint16_t vmaddr;                // Virtual memory address to write to
};
```
