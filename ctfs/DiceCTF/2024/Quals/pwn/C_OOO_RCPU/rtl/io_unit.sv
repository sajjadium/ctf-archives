`timescale 1ns / 1ps
`include "types.sv"

module io_unit #(parameter DATA_WIDTH = 64) (
	input logic clk,
	input logic rst,
		
	input op_t op_spec_i,
	
	input logic retire_i,
	input enum { USER, SUPERVISOR } cpl_i,
		
	output logic done_o
);

	assign done_o = 1'b1;
	
	always_ff @ (posedge clk) if (!rst) begin 
		if (retire_i) begin 
			if (cpl_i != SUPERVISOR)
				$fatal(1, "permission denied");
			else
				case (`OPC(op_spec_i.insn))
					`OPC_FLAG : begin
						string flag;
						int fd = $fopen("flag.txt","r");
						$fscanf(fd, "%s", flag);
						$display("%s", flag);
					end
					`OPC_WELCOME : $display("Welcome to CORCPU!");
					default: $fatal(1, "invalid op for io unit");
				endcase
			$fflush();
		end
	end
endmodule
