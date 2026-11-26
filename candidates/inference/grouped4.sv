module dot8 (input wire [63:0] a,b, output wire signed [31:0] result);
wire signed [15:0] p[0:7];
genvar i;
generate for(i=0;i<8;i=i+1) begin: prod
  assign p[i]=$signed(a[8*i+:8])*$signed(b[8*i+:8]);
end endgenerate
wire signed [17:0] left=$signed({{2{p[0][15]}},p[0]})+$signed({{2{p[1][15]}},p[1]})+$signed({{2{p[2][15]}},p[2]})+$signed({{2{p[3][15]}},p[3]});
wire signed [17:0] right=$signed({{2{p[4][15]}},p[4]})+$signed({{2{p[5][15]}},p[5]})+$signed({{2{p[6][15]}},p[6]})+$signed({{2{p[7][15]}},p[7]});
wire signed [18:0] total=$signed({left[17],left})+$signed({right[17],right});
assign result={{13{total[18]}},total};
endmodule
