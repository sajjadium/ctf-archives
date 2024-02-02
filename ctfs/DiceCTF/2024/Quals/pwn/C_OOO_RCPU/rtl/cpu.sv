`timescale 1ns / 1ps

module cpu_entry;
	localparam DATA_WIDTH = 64;
	localparam FETCH_WIDTH = 64;
	
	bit clk;
	logic rst;

	logic dmem_rd_en;
	logic imem_rd_en;
	logic dmem_wr_en;

	logic [DATA_WIDTH - 1:0] dmem_addr;
	logic [DATA_WIDTH - 1:0] imem_addr;

	logic [$clog2(FETCH_WIDTH / 8) - 1:0] dmem_wr_size;
	logic [FETCH_WIDTH - 1:0] dmem_wr_data;
	
	logic dmem_busy;
	logic imem_busy;
	
	logic dmem_rdy;
	logic imem_rdy;

	logic [FETCH_WIDTH - 1:0] dmem_rd_data;
	logic [31:0] imem_rd_data;

	cache_behavioural #(
		.DATA_WIDTH ( DATA_WIDTH ),
		.FETCH_WIDTH ( FETCH_WIDTH )
	) cache (
		.clk ( clk ),
		.rst ( rst ),
		
		.dmem_rd_en_i ( dmem_rd_en ),
		.imem_rd_en_i ( imem_rd_en ),
		.dmem_wr_en_i ( dmem_wr_en ),
		
		.dmem_addr_i ( dmem_addr ),
		.imem_addr_i ( imem_addr ),
		
		.dmem_wr_size_i ( dmem_wr_size ),
		.dmem_wr_data_i ( dmem_wr_data ),
		
		.dmem_busy_o ( dmem_busy ),
		.imem_busy_o ( imem_busy ),
		
		.dmem_rdy_o ( dmem_rdy ),
		.imem_rdy_o ( imem_rdy ),
		
		.dmem_rd_data_o ( dmem_rd_data ),
		.imem_rd_data_o ( imem_rd_data )
	);
	
	core #(
		.MULTI_ISSUE ( 3 ) 
	) core (
		.clk ( clk ),
		.rst ( rst ),
		.max_instructions_i ( ~(16'b0) ),
		
		.dmem_rd_en_o ( dmem_rd_en ),
		.imem_rd_en_o ( imem_rd_en ),
		.dmem_wr_en_o ( dmem_wr_en ),
		
		.dmem_addr_o ( dmem_addr ),
		.imem_addr_o ( imem_addr ),
		
		.dmem_wr_size_o ( dmem_wr_size ),
		.dmem_wr_data_o ( dmem_wr_data ),
		
		.dmem_busy_i ( dmem_busy ),
		.imem_busy_i ( imem_busy ),
		
		.dmem_rdy_i ( dmem_rdy ),
		.imem_rdy_i ( imem_rdy ),
		
		.dmem_rd_data_i ( dmem_rd_data ),
		.imem_rd_data_i ( imem_rd_data ),
		
		.done_o ( )
	);
	
	initial begin
		clk = 0;
		forever
			#5 clk = ~clk;
	end
	
	int c;
	initial begin
		for (int i = 0; i < 64'h10000; i++)
			cache.imem[i] = 0;
		
		$readmemh("/tmp/user_rom.rom", cache.imem, 0, 4096);
		$readmemh("system_rom.rom", cache.imem, 16384);
		$display("loaded roms"); $fflush();
		clk = 0;
		rst = 1;
		
		#1;
		clk = 1;
		#1;
		clk = 0;
		rst = 0;
		#1;
		
		clk = 0;
		forever #5 clk = ~clk;
	end
endmodule : cpu_entry
