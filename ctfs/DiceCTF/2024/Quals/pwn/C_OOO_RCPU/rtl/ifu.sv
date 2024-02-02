`timescale 1ns / 1ps
`include "types.sv"

module ifu #(parameter DATA_WIDTH = 64, MULTI_ISSUE = 3) (
	input logic clk,
	input logic rst,

	input logic [$clog2(MULTI_ISSUE):0] poll_cnt_i,

	input logic bcast_pc_rdy_i,
	input logic [DATA_WIDTH-1:0] bcast_branch_pc_i,

	output logic [$clog2(MULTI_ISSUE):0] rdy_cnt_o,
	output op_t fetch_insns_o[MULTI_ISSUE],
	output e_functional_unit fetch_rs_o [MULTI_ISSUE],

	output logic [DATA_WIDTH - 1:0] imem_load_addr_o,
	output logic imem_load_en_o,
	input logic [31:0] imem_load_insn_i,
	input logic imem_load_busy_i,
	input logic imem_load_rdy_i
);
	logic [DATA_WIDTH - 1:0] insn_load_pc;
	logic branch_in_pipeline;

	logic full;
	logic queue_reset;
	
	logic [31:0] fetch_insns_undecoded [MULTI_ISSUE];
	
	genvar i;
	generate;
		for (i = 0; i < MULTI_ISSUE; i++) begin
			instruction_decoder decoder (
				.instruction ( fetch_insns_undecoded[i] ),
				.op ( fetch_insns_o[i] ),
				.rs_id ( fetch_rs_o[i] )
			);
		end
	endgenerate;

	synchronous_fifo #(
		.DEPTH ( 8 ), 
		.DATA_WIDTH ( 32 ),
		.MULTI_POP ( MULTI_ISSUE )
	) queue (
		.clk ( clk ),
		.rst ( queue_reset ), // clear queue on branch

		.push ( imem_load_rdy_i ),
		.poll_cnt ( poll_cnt_i ),

		.data_in ( imem_load_insn_i ),
		.data_out ( fetch_insns_undecoded ),
		
		.ready_cnt ( rdy_cnt_o ),
		.full ( full )
	);

	assign queue_reset = rst || bcast_pc_rdy_i;

	assign imem_load_addr_o = insn_load_pc;
    assign imem_load_en_o = !((branch_in_pipeline) || full) && !imem_load_busy_i;
	
	always_ff @(posedge clk) if (rst) begin
		branch_in_pipeline <= 0;
		insn_load_pc <= 'b0;
	end

	always_ff @(posedge clk) if (!rst) begin
		if (imem_load_rdy_i) begin
			if (`OPC(imem_load_insn_i) == `OPC_BRANCH || `OPC(imem_load_insn_i) == `OPC_JAL || `OPC(imem_load_insn_i) == `OPC_JALR || `OPC(imem_load_insn_i) == `OPC_ECALL|| `OPC(imem_load_insn_i) == `OPC_ERET)
				branch_in_pipeline <= 1;
			else
				insn_load_pc <= insn_load_pc + 'h4;
		end
		
		if (bcast_pc_rdy_i) begin
			assert (!imem_load_rdy_i);
			branch_in_pipeline <= 0;
			insn_load_pc <= bcast_branch_pc_i;
		end
			
	end
endmodule : ifu