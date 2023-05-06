`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Designer: gary
// Design Name: 1Hz Clock
// Module Name: clk_1hz
// Project Name: Flag Vending Machine
// Target Devices: Xilinx FPGA
// Description: Gives Gary's special sauce a 1Hz clock
//////////////////////////////////////////////////////////////////////////////////

module clk_1hz(input clk, output reg clk_1hz);
    integer count;
    always @(posedge clk) begin
        if(count == 9999999) begin
            count <= 0;
            clk_1hz <= ~clk_1hz;
        end else if (count >= 0) begin
            count <= count + 1;
        end else begin
            count <= 0;
            clk_1hz <= 0;
        end
    end
endmodule
