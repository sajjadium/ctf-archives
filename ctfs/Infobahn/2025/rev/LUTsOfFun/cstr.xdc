set_property -dict { PACKAGE_PIN E3 IOSTANDARD LVCMOS33 } [get_ports { ACLK }];

create_clock -add -name ACLK -period 10.000 [get_ports { ACLK }]

set_property -dict { PACKAGE_PIN D9 IOSTANDARD LVCMOS33 } [get_ports { ARESETn }];

set_property -dict { PACKAGE_PIN G13 IOSTANDARD LVCMOS33 } [get_ports { S_WDATA[0] }];
set_property -dict { PACKAGE_PIN B11 IOSTANDARD LVCMOS33 } [get_ports { S_WDATA[1] }];
set_property -dict { PACKAGE_PIN A11 IOSTANDARD LVCMOS33 } [get_ports { S_WDATA[2] }];
set_property -dict { PACKAGE_PIN D12 IOSTANDARD LVCMOS33 } [get_ports { S_WDATA[3] }];
set_property -dict { PACKAGE_PIN D13 IOSTANDARD LVCMOS33 } [get_ports { S_WDATA[4] }];
set_property -dict { PACKAGE_PIN B18 IOSTANDARD LVCMOS33 } [get_ports { S_WDATA[5] }];
set_property -dict { PACKAGE_PIN A18 IOSTANDARD LVCMOS33 } [get_ports { S_WDATA[6] }];
set_property -dict { PACKAGE_PIN K16 IOSTANDARD LVCMOS33 } [get_ports { S_WDATA[7] }];

set_property -dict { PACKAGE_PIN E15 IOSTANDARD LVCMOS33 } [get_ports { S_WDATA[8] }];
set_property -dict { PACKAGE_PIN E16 IOSTANDARD LVCMOS33 } [get_ports { S_WDATA[9] }];
set_property -dict { PACKAGE_PIN D15 IOSTANDARD LVCMOS33 } [get_ports { S_WDATA[10] }];
set_property -dict { PACKAGE_PIN C15 IOSTANDARD LVCMOS33 } [get_ports { S_WDATA[11] }];
set_property -dict { PACKAGE_PIN J17 IOSTANDARD LVCMOS33 } [get_ports { S_WDATA[12] }];
set_property -dict { PACKAGE_PIN J18 IOSTANDARD LVCMOS33 } [get_ports { S_WDATA[13] }];
set_property -dict { PACKAGE_PIN K15 IOSTANDARD LVCMOS33 } [get_ports { S_WDATA[14] }];
set_property -dict { PACKAGE_PIN J15 IOSTANDARD LVCMOS33 } [get_ports { S_WDATA[15] }];

set_property -dict { PACKAGE_PIN U12 IOSTANDARD LVCMOS33 } [get_ports { S_WDATA[16] }];
set_property -dict { PACKAGE_PIN V12 IOSTANDARD LVCMOS33 } [get_ports { S_WDATA[17] }];
set_property -dict { PACKAGE_PIN V10 IOSTANDARD LVCMOS33 } [get_ports { S_WDATA[18] }];
set_property -dict { PACKAGE_PIN V11 IOSTANDARD LVCMOS33 } [get_ports { S_WDATA[19] }];
set_property -dict { PACKAGE_PIN U14 IOSTANDARD LVCMOS33 } [get_ports { S_WDATA[20] }];
set_property -dict { PACKAGE_PIN V14 IOSTANDARD LVCMOS33 } [get_ports { S_WDATA[21] }];
set_property -dict { PACKAGE_PIN T13 IOSTANDARD LVCMOS33 } [get_ports { S_WDATA[22] }];
set_property -dict { PACKAGE_PIN U13 IOSTANDARD LVCMOS33 } [get_ports { S_WDATA[23] }];

set_property -dict { PACKAGE_PIN D4 IOSTANDARD LVCMOS33 } [get_ports { S_WDATA[24] }];
set_property -dict { PACKAGE_PIN D3 IOSTANDARD LVCMOS33 } [get_ports { S_WDATA[25] }];
set_property -dict { PACKAGE_PIN F4 IOSTANDARD LVCMOS33 } [get_ports { S_WDATA[26] }];
set_property -dict { PACKAGE_PIN F3 IOSTANDARD LVCMOS33 } [get_ports { S_WDATA[27] }];
set_property -dict { PACKAGE_PIN E2 IOSTANDARD LVCMOS33 } [get_ports { S_WDATA[28] }];
set_property -dict { PACKAGE_PIN D2 IOSTANDARD LVCMOS33 } [get_ports { S_WDATA[29] }];
set_property -dict { PACKAGE_PIN H2 IOSTANDARD LVCMOS33 } [get_ports { S_WDATA[30] }];
set_property -dict { PACKAGE_PIN G2 IOSTANDARD LVCMOS33 } [get_ports { S_WDATA[31] }];

set_property -dict { PACKAGE_PIN F5 IOSTANDARD LVCMOS33 } [get_ports { S_WSTRB[0] }];
set_property -dict { PACKAGE_PIN D8 IOSTANDARD LVCMOS33 } [get_ports { S_WSTRB[1] }];
set_property -dict { PACKAGE_PIN C7 IOSTANDARD LVCMOS33 } [get_ports { S_WSTRB[2] }];
set_property -dict { PACKAGE_PIN E7 IOSTANDARD LVCMOS33 } [get_ports { S_WSTRB[3] }];

set_property -dict { PACKAGE_PIN V15 IOSTANDARD LVCMOS33 } [get_ports { S_RDATA[0] }];
set_property -dict { PACKAGE_PIN U16 IOSTANDARD LVCMOS33 } [get_ports { S_RDATA[1] }];
set_property -dict { PACKAGE_PIN P14 IOSTANDARD LVCMOS33 } [get_ports { S_RDATA[2] }];
set_property -dict { PACKAGE_PIN T11 IOSTANDARD LVCMOS33 } [get_ports { S_RDATA[3] }];
set_property -dict { PACKAGE_PIN R12 IOSTANDARD LVCMOS33 } [get_ports { S_RDATA[4] }];
set_property -dict { PACKAGE_PIN T14 IOSTANDARD LVCMOS33 } [get_ports { S_RDATA[5] }];
set_property -dict { PACKAGE_PIN T15 IOSTANDARD LVCMOS33 } [get_ports { S_RDATA[6] }];
set_property -dict { PACKAGE_PIN T16 IOSTANDARD LVCMOS33 } [get_ports { S_RDATA[7] }];
set_property -dict { PACKAGE_PIN N15 IOSTANDARD LVCMOS33 } [get_ports { S_RDATA[8] }];
set_property -dict { PACKAGE_PIN M16 IOSTANDARD LVCMOS33 } [get_ports { S_RDATA[9] }];
set_property -dict { PACKAGE_PIN V17 IOSTANDARD LVCMOS33 } [get_ports { S_RDATA[10] }];
set_property -dict { PACKAGE_PIN U18 IOSTANDARD LVCMOS33 } [get_ports { S_RDATA[11] }];
set_property -dict { PACKAGE_PIN R17 IOSTANDARD LVCMOS33 } [get_ports { S_RDATA[12] }];
set_property -dict { PACKAGE_PIN P17 IOSTANDARD LVCMOS33 } [get_ports { S_RDATA[13] }];

set_property -dict { PACKAGE_PIN U11 IOSTANDARD LVCMOS33 } [get_ports { S_RDATA[14] }];
set_property -dict { PACKAGE_PIN V16 IOSTANDARD LVCMOS33 } [get_ports { S_RDATA[15] }];
set_property -dict { PACKAGE_PIN M13 IOSTANDARD LVCMOS33 } [get_ports { S_RDATA[16] }];
set_property -dict { PACKAGE_PIN R10 IOSTANDARD LVCMOS33 } [get_ports { S_RDATA[17] }];
set_property -dict { PACKAGE_PIN R11 IOSTANDARD LVCMOS33 } [get_ports { S_RDATA[18] }];
set_property -dict { PACKAGE_PIN R13 IOSTANDARD LVCMOS33 } [get_ports { S_RDATA[19] }];
set_property -dict { PACKAGE_PIN R15 IOSTANDARD LVCMOS33 } [get_ports { S_RDATA[20] }];
set_property -dict { PACKAGE_PIN P15 IOSTANDARD LVCMOS33 } [get_ports { S_RDATA[21] }];
set_property -dict { PACKAGE_PIN R16 IOSTANDARD LVCMOS33 } [get_ports { S_RDATA[22] }];
set_property -dict { PACKAGE_PIN N16 IOSTANDARD LVCMOS33 } [get_ports { S_RDATA[23] }];
set_property -dict { PACKAGE_PIN N14 IOSTANDARD LVCMOS33 } [get_ports { S_RDATA[24] }];
set_property -dict { PACKAGE_PIN U17 IOSTANDARD LVCMOS33 } [get_ports { S_RDATA[25] }];
set_property -dict { PACKAGE_PIN T18 IOSTANDARD LVCMOS33 } [get_ports { S_RDATA[26] }];
set_property -dict { PACKAGE_PIN R18 IOSTANDARD LVCMOS33 } [get_ports { S_RDATA[27] }];
set_property -dict { PACKAGE_PIN P18 IOSTANDARD LVCMOS33 } [get_ports { S_RDATA[28] }];
set_property -dict { PACKAGE_PIN N17 IOSTANDARD LVCMOS33 } [get_ports { S_RDATA[29] }];

set_property -dict { PACKAGE_PIN G1 IOSTANDARD LVCMOS33 } [get_ports { S_RDATA[30] }];
set_property -dict { PACKAGE_PIN H1 IOSTANDARD LVCMOS33 } [get_ports { S_RDATA[31] }];

set_property -dict { PACKAGE_PIN D5 IOSTANDARD LVCMOS33 } [get_ports { S_AWADDR[0] }];
set_property -dict { PACKAGE_PIN B7 IOSTANDARD LVCMOS33 } [get_ports { S_AWADDR[1] }];
set_property -dict { PACKAGE_PIN B6 IOSTANDARD LVCMOS33 } [get_ports { S_AWADDR[2] }];
set_property -dict { PACKAGE_PIN E6 IOSTANDARD LVCMOS33 } [get_ports { S_AWADDR[3] }];
set_property -dict { PACKAGE_PIN E5 IOSTANDARD LVCMOS33 } [get_ports { S_AWADDR[4] }];

set_property -dict { PACKAGE_PIN A4 IOSTANDARD LVCMOS33 } [get_ports { S_ARADDR[0] }];
set_property -dict { PACKAGE_PIN A3 IOSTANDARD LVCMOS33 } [get_ports { S_ARADDR[1] }];
set_property -dict { PACKAGE_PIN L18 IOSTANDARD LVCMOS33 } [get_ports { S_ARADDR[2] }];
set_property -dict { PACKAGE_PIN M18 IOSTANDARD LVCMOS33 } [get_ports { S_ARADDR[3] }];
set_property -dict { PACKAGE_PIN C1 IOSTANDARD LVCMOS33 } [get_ports { S_ARADDR[4] }];

set_property -dict { PACKAGE_PIN A8 IOSTANDARD LVCMOS33 } [get_ports { S_AWVALID }];
set_property -dict { PACKAGE_PIN C11 IOSTANDARD LVCMOS33 } [get_ports { S_WVALID }];
set_property -dict { PACKAGE_PIN C10 IOSTANDARD LVCMOS33 } [get_ports { S_BREADY }];
set_property -dict { PACKAGE_PIN A10 IOSTANDARD LVCMOS33 } [get_ports { S_ARVALID }];
set_property -dict { PACKAGE_PIN F1 IOSTANDARD LVCMOS33 }  [get_ports { S_RREADY }];

set_property -dict { PACKAGE_PIN H5 IOSTANDARD LVCMOS33 } [get_ports { S_AWREADY }];
set_property -dict { PACKAGE_PIN J5 IOSTANDARD LVCMOS33 } [get_ports { S_WREADY }];
set_property -dict { PACKAGE_PIN T9 IOSTANDARD LVCMOS33 } [get_ports { S_BVALID }];
set_property -dict { PACKAGE_PIN T10 IOSTANDARD LVCMOS33 } [get_ports { S_ARREADY }];

set_property -dict { PACKAGE_PIN G6 IOSTANDARD LVCMOS33 } [get_ports { S_BRESP[1] }];
set_property -dict { PACKAGE_PIN F6 IOSTANDARD LVCMOS33 } [get_ports { S_BRESP[0] }];
set_property -dict { PACKAGE_PIN G3 IOSTANDARD LVCMOS33 } [get_ports { S_RRESP[1] }];
set_property -dict { PACKAGE_PIN J4 IOSTANDARD LVCMOS33 } [get_ports { S_RRESP[0] }];
set_property -dict { PACKAGE_PIN G4 IOSTANDARD LVCMOS33 } [get_ports { S_RVALID }];
