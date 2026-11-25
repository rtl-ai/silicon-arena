module gradient_tb;
    reg clk=0, reset=1, clear=0, enable=0;
    reg signed [7:0] activation=0, gradient=0;
    wire signed [31:0] total;
    integer expected=0, i, seed=42, av, gv;
    gradient_accumulator dut(clk, reset, clear, enable, activation, gradient, total);
    always #5 clk=~clk;
    task check;
        input integer want;
        begin if (total !== want) $fatal(1,"gradient expected=%0d got=%0d",want,total); end
    endtask
    initial begin
        @(negedge clk); check(0); reset=0;
        for (i=0;i<1000;i=i+1) begin
            av=($random(seed)&255)-128; gv=($random(seed)&255)-128;
            activation=av; gradient=gv; enable=(i%3!=0); clear=(i%31==0);
            if (clear) expected=0;
            else if (enable) expected=expected+av*gv;
            @(negedge clk); check(expected);
        end
        $display("PASS training: 1000 cycles"); $finish;
    end
endmodule
