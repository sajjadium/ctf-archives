`timescale 1ns / 1ps

module Stackmachine(clk, rst, in, out, err);

input clk;
input rst;
input [3:0] in;
output reg [WORD_SIZE - 1:0] out;
output reg err;

parameter STACK_SIZE = 128,
          WORD_SIZE = 32;

wire [2:0] ins = in[3:1];
wire mod = in[0];

localparam [2:0] SET  = 3'h0;
localparam [2:0] INC  = 3'h1;
localparam [2:0] SWAP = 3'h2;
localparam [2:0] DUP  = 3'h3;
localparam [2:0] ADD  = 3'h4;
localparam [2:0] MUL  = 3'h5;
localparam [2:0] NOP  = 3'h6;
localparam [2:0] DONE = 3'h7;

localparam [WORD_SIZE - 1:0] ERR_OOB = 'hf;
localparam [WORD_SIZE - 1:0] ERR_ZERO = 'he;

`define assert(check, error) \
  if(!(check)) begin \
    err <= 1; \
    out <= error; \
  end 


reg [WORD_SIZE - 1:0] stack [STACK_SIZE - 1:0];
reg [$clog2(STACK_SIZE) - 1:0] sp;

always @(posedge clk) begin
    if(rst == 1) begin
        integer i;
        sp <= 0;
        out <= 0;
        err <= 0;
        for (i=0; i<STACK_SIZE; i=i+1) stack[i] = 0;
    end
    else begin
        if(err == 0 && out == 0) begin
            case(ins)
            SET: begin
                `assert({1'b0, sp} < (STACK_SIZE - 1), ERR_OOB)
                stack[sp] <= {{(WORD_SIZE - 1){1'b0}}, mod};
                sp <= sp + 1;
            end
            INC: begin
                `assert(sp > 0, ERR_OOB)
                if(mod) stack[sp - 1] <= stack[sp - 1] + 1;
                else stack[sp - 1] <= stack[sp - 1] - 1;
            end
            SWAP: begin
                `assert(sp > 1, ERR_OOB)
                stack[sp - 1] <= stack [sp - 2];
                stack[sp - 2] <= stack [sp - 1];
            end
            DUP: begin
                `assert(sp > 0, ERR_OOB)
                `assert({1'b0, sp} < STACK_SIZE - 1, ERR_OOB)
                stack[sp] <= stack[sp - 1];
                sp <= sp + 1;
            end
            ADD: begin
                `assert(sp > 1, ERR_OOB)
                if(mod) stack[sp - 2] <= stack[sp - 2] + stack[sp - 1];
                else stack[sp - 2] <= stack[sp - 2] - stack[sp - 1];
                sp <= sp - 1;
            end
            MUL: begin
                `assert(sp > 1, ERR_OOB)
                stack[sp - 2] <= stack[sp - 2] * stack[sp - 1];
                sp <= sp - 1;
            end
            NOP: ;
            
            DONE: begin
                `assert(sp > 0, ERR_OOB)
                `assert(stack[sp - 1] != 0, ERR_ZERO)
                out <= stack[sp - 1];
            end
            endcase
        end
    end
end



endmodule


