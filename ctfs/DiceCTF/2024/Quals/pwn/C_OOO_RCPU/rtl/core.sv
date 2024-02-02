`include "types.sv"

module core #(parameter DATA_WIDTH = 64, FETCH_WIDTH = 64, MULTI_ISSUE = 2) (
	input logic clk,
	input logic rst,

	input logic [15:0] max_instructions_i,
	output logic done_o,

	input logic dmem_busy_i,
	input logic imem_busy_i,

	input logic dmem_rdy_i,
	input logic imem_rdy_i,

	input logic [FETCH_WIDTH - 1:0] dmem_rd_data_i,
	input logic [31:0] imem_rd_data_i,

	output logic dmem_rd_en_o,
	output logic imem_rd_en_o,
	output logic dmem_wr_en_o,

	output logic [DATA_WIDTH - 1:0] dmem_addr_o,
	output logic [DATA_WIDTH - 1:0] imem_addr_o,

	output logic [$clog2(FETCH_WIDTH / 8) - 1:0] dmem_wr_size_o,
	output logic [FETCH_WIDTH - 1:0] dmem_wr_data_o
);
	logic [15:0]             issued_instruction_cnt;
		
	logic [$clog2(MULTI_ISSUE):0] fetch_queue_size;
	e_functional_unit             fetch_queue_units[MULTI_ISSUE];
	op_t       fetch_queue_ops[MULTI_ISSUE];
	e_instruction_format          fetch_queue_fmt[MULTI_ISSUE];
	logic [4:0]                   fetch_queue_rd[MULTI_ISSUE];
	logic [4:0]                   fetch_queue_rs1[MULTI_ISSUE];
	logic [4:0]                   fetch_queue_rs2[MULTI_ISSUE];	

	logic                    issue_en [MULTI_ISSUE];
	logic [$clog2(MULTI_ISSUE):0] issue_cnt;
	op_t  issue_op[MULTI_ISSUE];

	logic                    issue_mark_virtual[MULTI_ISSUE];
	logic                    issue_has_rd[MULTI_ISSUE];
	logic [4:0]				 issue_rd [MULTI_ISSUE];
	e_functional_unit        issue_unit[MULTI_ISSUE];
	logic [4:0]				 issue_rs1[MULTI_ISSUE];
	logic [4:0]				 issue_rs2[MULTI_ISSUE];	
	register                 issue_read1_value[MULTI_ISSUE];
	register                 issue_read2_value[MULTI_ISSUE];

	e_functional_unit        retire_rs;
	logic                    retire_en;
	logic                    bcast_valid;
	logic [DATA_WIDTH - 1:0] bcast_value;

	logic [`FU_CNT - 1:0]  retirement_ready;
	logic [`FU_CNT - 1:0]  station_busy;
	logic [DATA_WIDTH - 1:0] unit_results [`FU_CNT];

	logic                    alu_rop1;
	logic                    alu_rop2;
	logic                    alu_done;
	op_t  alu_curr_op;
	logic [63:0]             alu_op1;
	logic [63:0]             alu_op2;
	logic [63:0]             alu_result;
	
	logic                    lsu_rop1;
	logic                    lsu_rop2;
	logic                    lsu_done;
	logic                    lsu_retirement_ready;
	logic                    lsu_retire_en;
	op_t  lsu_curr_op;
	logic [63:0]             lsu_addr;
	logic [63:0]             lsu_store_data;
	logic [63:0]             lsu_result;
	
	logic                    bu_rop1;
	logic                    bu_rop2;
	logic                    bu_done, bu_rd_done, bu_pc_done;
	op_t  bu_curr_op;
	logic [63:0]             bu_op1;
	logic [63:0]             bu_op2;
	logic [63:0]             bu_result, bu_pc_result;
	
	logic                    pu_rop1;
	logic                    pu_rop2;
	logic                    pu_done;
	op_t  pu_curr_op;
	logic [63:0]             pu_op1;
	logic [63:0]             pu_op2;
	logic [63:0]             pu_result;
	enum { USER, SUPERVISOR } cpl;
	
	logic                    iou_rop1;
	logic                    iou_rop2;
	logic                    iou_done;
	op_t  iou_curr_op;
	logic [63:0]             iou_op1;
	logic [63:0]             iou_op2;
	logic [63:0]             iou_result;
	
	ifu #(
		.DATA_WIDTH ( DATA_WIDTH ), 
		.MULTI_ISSUE ( MULTI_ISSUE )
	) ifu (
		.clk ( clk ),
		.rst ( rst ),

		.poll_cnt_i ( issue_cnt ),

		.bcast_pc_rdy_i ( bcast_valid && retire_rs == BU && bu_pc_done ),
		.bcast_branch_pc_i ( bu_pc_result ),

		.rdy_cnt_o ( fetch_queue_size ),
		.fetch_insns_o ( fetch_queue_ops ),
		.fetch_rs_o ( fetch_queue_units ),

		.imem_load_addr_o ( imem_addr_o ),
		.imem_load_en_o ( imem_rd_en_o ),
		.imem_load_insn_i ( imem_rd_data_i ),
		.imem_load_busy_i ( imem_busy_i ),
		.imem_load_rdy_i ( imem_rdy_i )
	);

	issue_arbiter #(
		.DATA_WIDTH ( DATA_WIDTH ),
		.FETCH_WIDTH ( FETCH_WIDTH ),
		.MULTI_ISSUE ( MULTI_ISSUE )
	) issue_arbiter (
		.clk ( clk ),
		.rst ( rst ),
		
		.stall_i ( issued_instruction_cnt >= max_instructions_i ),
		
		.bcast_valid_i ( bcast_valid ),
		.bcast_value_i ( bcast_value ),
		.bcast_rs_i ( retire_rs ),
		
		.units_busy_i ( station_busy ),
		
		.queue_rdy_cnt_i ( fetch_queue_size ),
		.queue_rd_i ( fetch_queue_rd ),
		.queue_rs1_i ( fetch_queue_rs1 ),
		.queue_rs2_i ( fetch_queue_rs2 ),
		.queue_insn_fmt_i ( fetch_queue_fmt ),
		.queue_stations_i ( fetch_queue_units ),
		
		.issue_en_o ( issue_en ),
		.issue_cnt_o ( issue_cnt )
	);
	
	register_file #(
		.DATA_WIDTH ( DATA_WIDTH ),
		.MULTI_ISSUE ( MULTI_ISSUE )
	) rf (
		.clk ( clk ),
		.rst ( rst ),

		.issue_wr_en_i ( issue_mark_virtual ),
		.issue_dst_i ( issue_rd ),
		.issue_rs_i ( issue_unit ),

		.bcast_valid_i ( bcast_valid ),
		.bcast_rs_i ( retire_rs ),
		.bcast_value_i ( bcast_value ),

		.read_reg1_i ( issue_rs1 ),
		.read_reg2_i ( issue_rs2 ),

		.read_value1_o ( issue_read1_value ),
		.read_value2_o ( issue_read2_value )
	);

	Retirement_Arbiter #(DATA_WIDTH) ra (
		.retirement_ready_i ( retirement_ready ),
		.unit_result_i ( unit_results ),

		.unit_retire_o ( retire_rs ),
		.retire_en_o ( retire_en ),
		.bcast_valid_o ( bcast_valid ),
		.bcast_value_o ( bcast_value )
	);

	`define RESERVATION_STATION(MODULE_NAME, ID, UNIT_DONE, CURR_OP, R_OPER1, R_OPER2, OPER1, OPER2) \
		logic issue_en_``ID;	\
		op_t issue_op_spec_``ID;\
		register issue_read1_value_``ID, issue_read2_value_``ID; \
		always_comb begin \
			issue_read1_value_``ID = '{ default: 'X }; \
			issue_read2_value_``ID = '{ default: 'X }; \
			issue_en_``ID = 1'b0; \
			issue_op_spec_``ID = '{encoding: e_instruction_format'('X), default: 'X}; \
			\
			for (int i = 0; i < MULTI_ISSUE; i++) \
				if (issue_en[i] && issue_unit[i] == ID) begin \
					issue_en_``ID = 1'b1; \
					issue_op_spec_``ID = issue_op[i]; \
					issue_read1_value_``ID = issue_read1_value[i]; \
					issue_read2_value_``ID = issue_read2_value[i]; \
				end \
		end \
		reservation_station	#(DATA_WIDTH, ID) MODULE_NAME (                                          \
			.clk ( clk ),                                                                            \
			.rst ( rst ),                                                                            \
                                                                                                     \
			.read1_value_i ( issue_read1_value_``ID ),                                                    \
			.read2_value_i ( issue_read2_value_``ID ),                                                    \
                                                                                                     \
			.busy_o ( station_busy[ID] ),                                                            \
                                                                                                     \
			.issue_en_i ( issue_en_``ID ),                                              \
			.issue_op_i ( issue_op_spec_``ID ),                                                                \
                                                                                                     \
			.unit_done_i ( UNIT_DONE ),                                                              \
                                                                                                     \
			.resolved_op1_o ( R_OPER1 ),                                                             \
			.resolved_op2_o ( R_OPER2 ),                                                             \
                                                                                                     \
			.bcast_en_i ( bcast_valid ),                                                             \
			.bcast_data_i ( bcast_value ),                                                           \
			.bcast_rs_i ( retire_rs ),                                                               \
                                                                                                     \
			.retire_i ( retire_en && retire_rs == ID ),                                              \
			.retirement_ready_o ( retirement_ready[ID] ),                                            \
                                                                                                     \
			.current_op_o ( CURR_OP ),                                                               \
                                                                                                     \
			.op1_value_o ( OPER1 ),                                                                  \
			.op2_value_o ( OPER2 )                                                                   \
		);
	
	`RESERVATION_STATION(alu_rs, ALU, alu_done, alu_curr_op, alu_rop1, alu_rop2, alu_op1, alu_op2)
	alu alu (
		.lhs ( alu_op1 ),
		.rhs ( alu_op2 ),

		.lhs_valid ( alu_rop1 ),
		.rhs_valid ( alu_rop2 ),

		.op_spec ( alu_curr_op ),

		.result ( alu_result ),
		.result_valid ( alu_done )
	);

	`RESERVATION_STATION(lsu_rs, LSU, lsu_done, lsu_curr_op, lsu_rop1, lsu_rop2, lsu_addr, lsu_store_data)
	lsu #(DATA_WIDTH, FETCH_WIDTH) lsu (
		.clk ( clk ),
		.rst ( rst ),

		.addr_i ( lsu_addr ),
		.addr_valid_i ( lsu_rop1 ),

		.store_data_i ( lsu_store_data ),
		.store_data_valid_i ( lsu_rop2 ),

		.op_spec_i ( lsu_curr_op ),

		.result_o ( lsu_result ),
		.done_o ( lsu_done ),

		.dmem_busy_i ( dmem_busy_i ),
		.dmem_rdy_i ( dmem_rdy_i ),

		.dmem_rd_en_o ( dmem_rd_en_o ),
		.dmem_wr_en_o ( dmem_wr_en_o ),

		.dmem_addr_o ( dmem_addr_o ),

		.dmem_wr_size_o ( dmem_wr_size_o ),
		.dmem_wr_data_o ( dmem_wr_data_o ),
		.dmem_rd_data_i ( dmem_rd_data_i )
	);

	`RESERVATION_STATION(bu_rs, BU, bu_done, bu_curr_op, bu_rop1, bu_rop2, bu_op1, bu_op2)
	bu bu (
		.clk ( clk ),
		.lhs ( bu_op1 ),
		.rhs ( bu_op2 ),

		.lhs_valid ( bu_rop1 ),
		.rhs_valid ( bu_rop2 ),
		
		.retire ( retire_en && retire_rs == BU ),

		.op_spec ( bu_curr_op ),

		.pc ( imem_addr_o ),
		.cpl_i ( cpl ),

		.result_rd ( bu_result ),
		.result_pc ( bu_pc_result ),
		.result_rd_valid ( bu_rd_done ),
		.result_pc_valid ( bu_pc_done ),
		.done_o ( bu_done )
	);


	`RESERVATION_STATION(pu_rs, PU, pu_done, pu_curr_op, pu_rop1, pu_rop2, pu_op1, pu_op2)
	privilege_unit #(
		.DATA_WIDTH ( DATA_WIDTH )
	) pu (
		.clk ( clk ),
		.rst ( rst ),
		
		.lhs ( pu_op1 ),
		.lhs_valid ( pu_rop1 ),
		
		.op_valid_i ( station_busy[PU] ),
		.retire_i ( retire_en && retire_rs == PU ),
		.op_spec_i ( pu_curr_op ),
		.curr_fetch_pc_i ( imem_addr_o ),
		.done_o ( pu_done ),
		
		.cpl_o ( cpl )
	);
	
	`RESERVATION_STATION(iou_rs, IOU, iou_done, iou_curr_op, iou_rop1, iou_rop2, iou_op1, iou_op2)
	io_unit #(
		.DATA_WIDTH ( DATA_WIDTH )
	) iou (
		.clk ( clk ),
		.rst ( rst ),
		
		.retire_i ( retire_en && retire_rs == IOU ),
		.op_spec_i ( iou_curr_op ),
		.done_o ( iou_done ),
		
		.cpl_i ( cpl )
	);
	
	
	assign done_o = issued_instruction_cnt >= max_instructions_i && station_busy == 'b0;

	assign unit_results[LSU] = lsu_result;
	assign unit_results[ALU] = alu_result;
	assign unit_results[BU]  = bu_result;
	assign unit_results[PU]  = pu_result;
	assign unit_results[IOU]  = iou_result;
	
	assign issue_op = fetch_queue_ops;
	assign issue_unit = fetch_queue_units;
	assign issue_rd = fetch_queue_rd;
	
	assign issue_rs1 = fetch_queue_rs1;
	assign issue_rs2 = fetch_queue_rs2;	
	
	always_comb begin		
		for (int i = 0; i < MULTI_ISSUE; i++) begin
			fetch_queue_fmt[i] = fetch_queue_ops[i].encoding;
			fetch_queue_rd[i] = `RD(fetch_queue_ops[i].insn);
			issue_has_rd[i] = has_rd(fetch_queue_ops[i].encoding);
			issue_mark_virtual[i] = issue_has_rd[i] && issue_en[i];
		
			fetch_queue_rs1[i] = `RS1(issue_op[i].insn);
			fetch_queue_rs2[i] = `RS2(issue_op[i].insn);
		end
	end

	always_ff @ (posedge clk)
		if (rst) issued_instruction_cnt <= 0;
		else issued_instruction_cnt <= issued_instruction_cnt + issue_cnt;
endmodule : core