module dot_tb;
    reg [63:0] a=0,b=0;
    wire signed [31:0] result;
    integer n,i,av, bv, expected,seed=73;
    dot8 dut(a,b,result);
    initial begin
        for (n=0;n<1000;n=n+1) begin
            expected=0;
            for (i=0;i<8;i=i+1) begin
                av=($random(seed)&255)-128; bv=($random(seed)&255)-128;
                a[i*8+:8]=av; b[i*8+:8]=bv; expected=expected+av*bv;
            end
            #1;
            if (result !== expected) $fatal(1,"dot expected=%0d got=%0d",expected,result);
        end
        a={8{8'h80}}; b={8{8'h80}}; #1;
        if (result!==32'sd131072) $fatal(1,"positive bound");
        a={8{8'h80}}; b={8{8'h7f}}; #1;
        if (result!==-32'sd130048) $fatal(1,"negative bound");
        $display("PASS inference: 1000 vectors + bounds"); $finish;
    end
endmodule
