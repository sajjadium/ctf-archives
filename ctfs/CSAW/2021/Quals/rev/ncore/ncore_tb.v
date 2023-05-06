`timescale 1 ns/10 ps  // time-unit = 1 ns, precision = 10 ps

  `define ADD  4'd0
  `define SUB  4'd1
  `define AND  4'd2
  `define OR   4'd3
  `define RES 4'd4
  `define MOVF 4'd5
  `define MOVT 4'd6
  `define ENT  4'd7
  `define EXT  4'd8 
  `define JGT  4'd9
  `define JEQ  4'd10
  `define JMP  4'd11
  `define INC  4'd12
  `define MOVFS 4'd13

module ncore_tb;
  reg [7:0] safe_rom [0:255];
  reg [7:0] ram [0:255];
  reg [31:0] regfile [0:3];
  reg [31:0] key [0:0];
  reg emode;
  wire [3:0] opcode;
  integer pc = 0;
  // assign opcode = ram[pc][3:0];
  reg clk = 0;
  // file descriptors
  int       read_file_descriptor;
  // memory
  logic [7:0] mem [15:0];



  task increment_pc();
    pc = pc + 2;
  endtask

  task load_safeROM();
    $display("loading safe rom, safely...");
    $readmemh("flag.hex",safe_rom);
  endtask

  task load_ram();
    $display("loading user controlled memory...");
    $readmemh("ram.hex",ram);
  endtask

  task open_file();
    $display("Opening file");
    read_file_descriptor=$fopen("flag.txt","rb");
  endtask

  task set_key();
    int tmp;
    // key[0] = 0;
    read_file_descriptor=$fopen("/dev/urandom","rb");
    tmp = $fread(key, read_file_descriptor);
    $readmemh("/dev/urandom",key);
  endtask

  task print_res();
    integer i;
    for( i=0; i<64; i = i + 1) begin
      $write("%h ",ram[255-i]);
    end
    $write("\n");
  endtask

  task init_regs();
    integer i = 0;
    for(i = 0; i<4; i++) begin
      regfile[i] = 32'd0;
    end
  endtask

  always begin
    #5 clk = ~clk;
  end

  always @(posedge clk) begin: inclk
    // $display("PC:%h | OPCODE: %d ADDR: %d",pc,ram[pc][3:0],ram[pc+1]);
    case(ram[pc][3:0]) 
     `ADD: begin
       regfile[ram[pc][5:4]] <=  regfile[ram[pc][7:6]] + regfile[ram[pc+1][1:0]];
       increment_pc();
     end
     `INC: begin
       regfile[ram[pc][5:4]] <=  regfile[ram[pc][5:4]] + 1;
       increment_pc();
     end
     `SUB: begin
       regfile[ram[pc][5:4]] <=  regfile[ram[pc][7:6]] -  regfile[ram[pc+1][1:0]];
       increment_pc();
     end
     `MOVF: begin
       regfile[ram[pc][5:4]] <= ram[ram[pc+1]];
       increment_pc();
     end
     `MOVFS: begin
       if(emode) begin 
        regfile[ram[pc][5:4]] <= safe_rom[ram[pc+1]];
       end
       increment_pc();
     end
     `MOVT: begin
       ram[ram[pc+1]] <= regfile[ram[pc][5:4]][7:0];
       increment_pc();
     end
     `JGT: begin
       pc <= (regfile[ram[pc][5:4]]>regfile[ram[pc][7:6]])?ram[pc+1]:pc+2;
     end
      `JEQ: begin
       pc <= (regfile[ram[pc][5:4]]==regfile[ram[pc][7:6]])?ram[pc+1]:pc+2;
     end
      `JMP: begin
       pc <= ram[pc+1];
     end
      `ENT: begin
        // $display("%d | %d",regfile[0],key[0][13:0]);
       if(key[0][13:0]==regfile[0]) begin
         emode <= 1;
         regfile[3] <= 0;
          $display("ENT");
       end else begin
         regfile[3] <= 1;
       end
       increment_pc();
     end
      `EXT: begin
       emode <= 0;
       increment_pc();
     end
     default: begin
       increment_pc();
     end
    endcase
  end:inclk

   initial 
    begin: initial_block
        // $monitor(,$time,": R0: %d,R1: %d,R2: %d,R3: %d",regfile[0],regfile[1],regfile[2],regfile[3]);
        init_regs();
        emode = 0;
        set_key();
        // $display("key: %d",key[0]);
        load_safeROM();
        load_ram();
        // $display("A %h, B: %h",safe_rom[0],safe_rom[1]);
        #1500000;
        print_res(); 
        $finish;
    end :initial_block



endmodule
