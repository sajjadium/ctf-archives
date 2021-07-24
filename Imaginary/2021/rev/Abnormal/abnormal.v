module nora(out, in);
    output [1:0] out;
    input [2:0] in;

    nor n1(w1, in[0], in[1]);
    nor n2(w2, in[0], w1);
    nor n3(w3, in[1], w1);
    nor n4(w4, w2, w3);
    nor n5(w5, w4, w4);
    nor n6(w6, w5, in[2]);
    nor n7(w7, w5, w6);
    nor n8(w8, in[2], w6);
    nor n9(w9, w7, w8);
    nor n10(out[0], w9, w9);
    nor n11(w10, in[0], in[0]);
    nor n12(w11, in[1], in[1]);
    nor n13(w12, w10, w11);
    nor n14(w13, in[2], in[2]);
    nor n15(w14, w11, w13);
    nor n16(w15, w12, w14);
    nor n17(w16, w10, w13);
    nor n18(w17, w15, w15);
    nor n19(w18, w17, w16);
    nor n20(out[1], w18, w18);
endmodule

module norb(out, in);
    output [16:0] out;
    input [32:0] in;

    nora n1({w1, out[0]}, {in[32], in[16], in[0]});
    nora n2({w2, out[1]}, {w1, in[1], in[17]});
    nora n3({w3, out[2]}, {w2, in[18], in[2]});
    nora n4({w4, out[3]}, {w3, in[3], in[19]});
    nora n5({w5, out[4]}, {w4, in[20], in[4]});
    nora n6({w6, out[5]}, {w5, in[5], in[21]});
    nora n7({w7, out[6]}, {w6, in[22], in[6]});
    nora n8({w8, out[7]}, {w7, in[7], in[23]});
    nora n9({w9, out[8]}, {w8, in[24], in[8]});
    nora n10({w10, out[9]}, {w9, in[9], in[25]});
    nora n11({w11, out[10]}, {w10, in[26], in[10]});
    nora n12({w12, out[11]}, {w11, in[11], in[27]});
    nora n13({w13, out[12]}, {w12, in[28], in[12]});
    nora n14({w14, out[13]}, {w13, in[13], in[29]});
    nora n15({w15, out[14]}, {w14, in[30], in[14]});
    nora n16({out[16], out[15]}, {w15, in[15], in[31]});
endmodule

module norc(out, in);
    output [256:0] out;
    input [512:0] in;

    norb n1({w1, out[15:0]}, {in[512], in[271:256], in[15:0]});
    norb n2({w2, out[31:16]}, {w1, in[31:16], in[287:272]});
    norb n3({w3, out[47:32]}, {w2, in[303:288], in[47:32]});
    norb n4({w4, out[63:48]}, {w3, in[63:48], in[319:304]});
    norb n5({w5, out[79:64]}, {w4, in[335:320], in[79:64]});
    norb n6({w6, out[95:80]}, {w5, in[95:80], in[351:336]});
    norb n7({w7, out[111:96]}, {w6, in[367:352], in[111:96]});
    norb n8({w8, out[127:112]}, {w7, in[127:112], in[383:368]});
    norb n9({w9, out[143:128]}, {w8, in[399:384], in[143:128]});
    norb n10({w10, out[159:144]}, {w9, in[159:144], in[415:400]});
    norb n11({w11, out[175:160]}, {w10, in[431:416], in[175:160]});
    norb n12({w12, out[191:176]}, {w11, in[191:176], in[447:432]});
    norb n13({w13, out[207:192]}, {w12, in[463:448], in[207:192]});
    norb n14({w14, out[223:208]}, {w12, in[223:208], in[479:464]});
    norb n15({w15, out[239:224]}, {w14, in[495:480], in[239:224]});
    norb n16({out[256], out[255:240]}, {w15, in[255:240], in[511:496]});
endmodule

module abnormal(out, in);
    output [255:0] out;
    input [255:0] in;

    wire [255:0] w1, w2, w3, w4, w5, w6;

    norc n1({c1, w1}, {257'h1a86f06e4e492e2c1ea6f4d5726e6d36bec57cf31472b986a675d3bc8e5d22b81, in});
    norc n2({c1, w2}, 513'h1a5e20394c934fd1198b1517d57e730cd225ccfa064ff42db76c19f3b7c0da91a6bf077b696cc4b22c0e56f4d3e6e150e386d6f04479ac502600e01fcdc29f5e4);
    nor n3 [255:0] (w3, w1, w2);
    nor n4 [255:0] (w4, w1, w3);
    nor n5 [255:0] (w5, w2, w3);
    nor n6 [255:0] (w6, w4, w5);
    nor n7 [255:0] (out, w6, w6);
endmodule

module main;
    wire [255:0] flag = 256'h696374667b00000000000000000000000000000000000000000000000000007d;
    wire [255:0] wrong;

    abnormal flagchecker(wrong, flag);
    initial begin
        #50;
        if (wrong) begin
            $display("Incorrect flag...");
            $finish;
        end
        $display("Correct!");
    end
endmodule