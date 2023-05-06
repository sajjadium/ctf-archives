module top();
    reg eo3,nF3;
    wire [11:0] D1q7APfd;
    wire [7:0] Dy,HZ4cC8Gwm7YlmW,XIzbggF,XvqVFhCAiK8ZU,eCzsnH;
    wire n35s92a4h;
    string flag;
    integer z;

    initial forever begin
        eo3 = 0; #5;
        eo3 = 1; #5;
    end
    
    initial begin
        #1;
        flag = "maple{testflag}";
        for (z=0; z< flag.len(); z++)
            TSdB.fgS[z+140] = flag[z];
        nF3 = 1;
        #10;
        nF3 = 0;
        #500000;
        if (TSdB.fgS[135] == 2)
            $display("You are winner!");
        else
            $display("Try again.");
        $finish();
    end

    ioJ xft(eo3,nF3,
        D1q7APfd,Dy,
        HZ4cC8Gwm7YlmW,XIzbggF,n35s92a4h,
        XvqVFhCAiK8ZU,eCzsnH);
    
    WsR #(8,8,"data.txt") TSdB(eo3,XvqVFhCAiK8ZU,HZ4cC8Gwm7YlmW,n35s92a4h,XIzbggF,eCzsnH);
    WsR #(12,8,"prog.txt") njg4YL52AkHJ(eo3,Dy,8'b0,1'b0,12'b0,D1q7APfd);
endmodule

module WsR(eo3,OaPYNLCWZ,FTkstjTLci,rIefx,eqJ,zhRu);
  parameter V2akbDl5qY = 32; 
  parameter ulTe71D35n = 4;
  parameter Yj4Y6kAS = "data.txt";

  input eo3;
  input [ulTe71D35n-1:0] OaPYNLCWZ, FTkstjTLci;
  input rIefx;
  input [V2akbDl5qY-1:0] eqJ;
  output logic [V2akbDl5qY-1:0] zhRu;

  reg [V2akbDl5qY-1:0] fgS [2**ulTe71D35n-1:0];

  initial $readmemh(Yj4Y6kAS, fgS);

  always @ (posedge eo3) begin
    if (rIefx)
      fgS[FTkstjTLci] <= eqJ;
    zhRu <= fgS[OaPYNLCWZ];
  end 
endmodule

module ioJ(eo3,nF3,
        D1q7APfd,Dy,
        HZ4cC8Gwm7YlmW,eCzsnH,n35s92a4h,
        XvqVFhCAiK8ZU,XIzbggF);

    input eo3, nF3;
    input [11:0] D1q7APfd;
    input [7:0] XIzbggF;
    output logic [7:0] Dy;
    output wire [7:0] HZ4cC8Gwm7YlmW,XvqVFhCAiK8ZU,eCzsnH;
    output logic n35s92a4h;

    wire [7:0] wgb7SWQCojbM0z,t14sshQ2kVxklOx;

    logic XTy0gvT0Bt1zmDLV008,EyZChyzXuhgMsgovFC;
    logic [2:0] QD2p2rf6jj5o9,ZamHFiK7It0a;
    logic [2:0] b4ivvC;

    wire [3:0] rSRUKV;
    wire [7:0] HySaIQf,BGtF9jPA,eRl31tlw1,yPs51RDPPUv,ulW9ociVdXXbW;
    logic C2y,R7O7txm93M,d6FZwCaz4mM,BXNS,WsNZ9Zbv;
    logic [7:0] nYKQupS;

    typedef enum {EKQMvI6y,jiZAPV,CSdThODUs,zAdA} LpZvRPGZ;
    LpZvRPGZ nWFEYy;

    enum {vJwNE,VEIImw4} nvuDF;

    wBlFnCyLj AI(eo3,nF3,
                d6FZwCaz4mM,
                yPs51RDPPUv,
                b4ivvC,lMwuHWy,
                XTy0gvT0Bt1zmDLV008,EyZChyzXuhgMsgovFC,
                QD2p2rf6jj5o9,ZamHFiK7It0a,
                eRl31tlw1,ulW9ociVdXXbW,
                wgb7SWQCojbM0z,t14sshQ2kVxklOx);

    assign rSRUKV = D1q7APfd[11:8];
    assign HySaIQf = D1q7APfd[7:0];
    assign BGtF9jPA = C2y == 0 ? HySaIQf : yPs51RDPPUv;
    assign HZ4cC8Gwm7YlmW = t14sshQ2kVxklOx;
    assign XvqVFhCAiK8ZU = wgb7SWQCojbM0z;
    assign eRl31tlw1 = R7O7txm93M == 1 ? HySaIQf : XIzbggF;
    
    assign eCzsnH = wgb7SWQCojbM0z;
    assign ulW9ociVdXXbW = Dy + 1;
    
    always_comb begin
        d6FZwCaz4mM = 1'b0;
        XTy0gvT0Bt1zmDLV008 = 1'b0;
        EyZChyzXuhgMsgovFC = 1'b0;
        QD2p2rf6jj5o9 = 3'b0;
        ZamHFiK7It0a = 3'b0;
        nWFEYy = CSdThODUs;
        C2y = 1'b0;
        R7O7txm93M = 1'b1;
        n35s92a4h = 1'b0;
        WsNZ9Zbv = 1'b0;
        if (nvuDF == VEIImw4) begin
        casez(rSRUKV)
            4'b0???: begin
                    if (rSRUKV != 7) begin
                        d6FZwCaz4mM = 1'b1;
                        b4ivvC = rSRUKV[2:0];
                        XTy0gvT0Bt1zmDLV008 = 1'b1;
                        QD2p2rf6jj5o9 = 3'd3;
                        WsNZ9Zbv = 1'b1;
                    end else begin
                        XTy0gvT0Bt1zmDLV008 = 1'b1;
                        QD2p2rf6jj5o9 = 3'd4;
                        end
                    end
            4'd8: begin
                    nWFEYy = jiZAPV;
                    C2y = 1'b0;
                    end
            4'd9: begin
                    nWFEYy = jiZAPV;
                    EyZChyzXuhgMsgovFC = 1'b1;
                    ZamHFiK7It0a = 3'd0;
                    C2y = 1'b0;
                    end
            4'd10: begin
                    nWFEYy = jiZAPV;
                    EyZChyzXuhgMsgovFC = 1'b1;
                    ZamHFiK7It0a = 3'd4;
                    C2y = 1'b1;
                    end
            4'd11: begin
                    C2y = 1'b0;
                    if(BXNS)
                        nWFEYy = jiZAPV;
                    else
                        nWFEYy = CSdThODUs;
                    end
            4'd12: begin
                    d6FZwCaz4mM = 1'b0;
                    XTy0gvT0Bt1zmDLV008 = 1'b1;
                    QD2p2rf6jj5o9 = 3'b0;
                    end
            4'd13: begin
                    QD2p2rf6jj5o9 = 3'd1;
                    d6FZwCaz4mM = 1'b0;
                    R7O7txm93M = 1'b0;
                    XTy0gvT0Bt1zmDLV008 = 1'b1;
                    end
            4'd14: begin
                    n35s92a4h = 1'b1;
                    QD2p2rf6jj5o9 = 3'd2;
                    XTy0gvT0Bt1zmDLV008 = 1'b1;
            end
            4'd15: nWFEYy = zAdA;
        endcase
        end
    end

    
    always_comb begin
        case(nWFEYy)
            EKQMvI6y: nYKQupS = 8'b0;
            jiZAPV: nYKQupS = BGtF9jPA;
            CSdThODUs: nYKQupS = Dy + 1;
            zAdA: nYKQupS = Dy;
            default: nYKQupS = 8'bz;
        endcase
    end

    always_ff @(posedge eo3) begin
        if (nF3) begin
            Dy <= 8'b0;
        end
        else begin
            if (nvuDF == VEIImw4)
                Dy <= nYKQupS;
            if (WsNZ9Zbv == 1)
                BXNS = lMwuHWy;
        end
    end

    always_ff @(posedge eo3) begin
        if (nF3)
            nvuDF <= vJwNE;
        else begin
            case(nvuDF)
                vJwNE: nvuDF <= VEIImw4;
                VEIImw4: nvuDF <= vJwNE;
            endcase
        end
    end
endmodule

module wBlFnCyLj(eo3,nF3,
                d6FZwCaz4mM,
                WnBJU6Eefj,
                b4ivvC,f,
                XTy0gvT0Bt1zmDLV008,EyZChyzXuhgMsgovFC,
                QD2p2rf6jj5o9,ZamHFiK7It0a,
                eRl31tlw1,ulW9ociVdXXbW,
                wgb7SWQCojbM0z,t14sshQ2kVxklOx);
    input eo3,nF3,d6FZwCaz4mM,XTy0gvT0Bt1zmDLV008,EyZChyzXuhgMsgovFC;
    input [7:0] eRl31tlw1,ulW9ociVdXXbW;
    input [2:0] QD2p2rf6jj5o9,ZamHFiK7It0a;
    output logic [7:0] WnBJU6Eefj,wgb7SWQCojbM0z,t14sshQ2kVxklOx;
    input [2:0] b4ivvC;
    output wire f;
    
    wire [7:0] QU6cTlk, yceR1D2,ZuqqtM7t, HgY3ljXJn, CMFdSku6Yj7;

    assign QU6cTlk = d6FZwCaz4mM == 0 ? eRl31tlw1 : yceR1D2;
    assign wgb7SWQCojbM0z = ZuqqtM7t;
    assign t14sshQ2kVxklOx = HgY3ljXJn;

    Ol8vW #(10) sIctJNEm0A(.eo3(eo3),.nF3(nF3),
                        .QU6cTlk(QU6cTlk),
                        .Jpup6gEow(ZuqqtM7t),.nFOoEI7Dnl(HgY3ljXJn),
                        .QV(QD2p2rf6jj5o9),.pb(XTy0gvT0Bt1zmDLV008));

    Ol8vW #(10) ek6j3imqGFx6(.eo3(eo3),.nF3(nF3),
                            .QU6cTlk(ulW9ociVdXXbW),
                            .Jpup6gEow(WnBJU6Eefj),.nFOoEI7Dnl(CMFdSku6Yj7),
                            .QV(ZamHFiK7It0a),.pb(EyZChyzXuhgMsgovFC));

    Ltc Ltc(ZuqqtM7t,HgY3ljXJn,b4ivvC,yceR1D2,f);




endmodule

module Ol8vW(eo3,nF3,QU6cTlk,Jpup6gEow,nFOoEI7Dnl,QV,pb);
    input eo3,nF3,pb;
    
    input [7:0] QU6cTlk;
    output [7:0] Jpup6gEow,nFOoEI7Dnl;
    input [2:0] QV;

    parameter WXifi4fqUy9NY = 16;
    logic [7:0] fgS [2**WXifi4fqUy9NY-1:0];
    logic [WXifi4fqUy9NY-1:0] gPrDVGD;


    always_ff @(posedge eo3) begin
        if (nF3 == 1) begin
            gPrDVGD <= 0;
        end else if (pb ==1) begin
            case (QV)
                3'd0: begin
                        fgS[gPrDVGD+1] <= QU6cTlk;
                        gPrDVGD <= gPrDVGD + 1;
                end
                3'd1: fgS[gPrDVGD]<=QU6cTlk;
                3'd2: gPrDVGD <= gPrDVGD - 2;
                3'd3: begin 
                        gPrDVGD <= gPrDVGD - 1; 
                        fgS[gPrDVGD-1] <= QU6cTlk;
                end
                3'd4: gPrDVGD <= gPrDVGD - 1;
            endcase
        end
    end

    assign {Jpup6gEow,nFOoEI7Dnl} = {fgS[gPrDVGD],fgS[gPrDVGD-1]};

endmodule

module Ltc(Z,o,QV,mtc,f);
    input [7:0] Z,o;
    output logic [7:0] mtc;
    input [2:0] QV;
    output f;

    assign f = mtc == 0 ? 1'b1 : 1'b0;

    always_comb begin
        case (QV)
            3'd0: mtc = Z + o;
            3'd1: mtc = Z - o;
            3'd2: mtc = Z ^ o;
            3'd3: mtc = Z & o;
            3'd4: mtc = Z | o;
            3'd5: mtc = Z << o;
            3'd6: mtc = Z >> o;
            default: mtc = 8'bz;
        endcase
    end
endmodule

