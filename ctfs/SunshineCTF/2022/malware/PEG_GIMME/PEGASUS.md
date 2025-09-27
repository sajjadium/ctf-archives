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
	char magic[8] = "\x7fPEGASUS";  // Fixed value to mark the beginning of a PEGASUS file
	uint32_t arch = '_EAR';         // Defines the CPU architecture this PEGASUS file is built for
	uint16_t cmd_count;             // Total number of load commands in this PEGASUS file
	Pegasus_Cmd cmds[ncmds];        // Array of load commands. Each element is variable sized
};

// Start of every PEGASUS load command
struct Pegasus_Cmd {
	uint16_t cmd_type;              // Selects which specific type of load command this is
	uint16_t cmd_size;              // Number of bytes in this load command, including sizeof(Pegasus_Cmd)
};

// Map a segment from the PEGASUS file into memory
// cmd_type = 1
struct Pegasus_Segment: Pegasus_Cmd {
	lestring name;                  // Name of the segment such as @TEXT
	uint8_t mem_vppn;               // Virtual page number where the segment should be mapped
	uint8_t mem_vpage_count;        // Number of virtual pages to map in this segment region
	uint16_t mem_foff;              // File offset in bytes to the start of the segment data
	uint16_t mem_fsize;             // Number of bytes starting at mem_foff to map
	uint8_t mem_prot;               // Bitmask of memory protections to apply (EAR_PROT_READ = 1, EAR_PROT_WRITE = 2, EAR_PROT_EXECUTE = 4)
};

// During load, call the function at PC.DPC with 6 arguments controlled
// cmd_type = 2
struct Pegasus_Entrypoint: Pegasus_Cmd {
	uint16_t A0, A1, A2, A3, A4, A5, PC, DPC;
};

// Describes the location and size of the symbol table in this PEGASUS file
// cmd_type = 3
struct Pegasus_SymbolTable: Pegasus_Cmd {
	uint16_t sym_count;             // Total number of symbols in the symbol table
	Pegasus_Symbol syms[sym_count]; // List of symbols in the symbol table
};

// Defines a single symbol's value
struct Pegasus_Symbol {
	lestring name;                  // Name of the symbol, w/o the '@' prefix
	uint16_t value;                 // Value of the symbol (usually a virtual address), or 0xFFFF for imported symbols
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
	uint16_t fileoff;               // File offset in bytes to where the relocation value should be written
};
```
