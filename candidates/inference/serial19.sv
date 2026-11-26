module dot8 (input wire [63:0] a,b, output wire signed [31:0] result);
wire signed [15:0] p[0:7];
genvar i;
generate for(i=0;i<8;i=i+1) begin: prod
  assign p[i]=$signed(a[8*i+:8])*$signed(b[8*i+:8]);
end endgenerate
wire signed [18:0] s[0:8];
assign s[0]=19'sd0;
generate for(i=0;i<8;i=i+1) begin: sum
  assign s[i+1]=s[i]+$signed({{3{p[i][15]}},p[i]});
end endgenerate
assign result={{13{s[8][18]}},s[8]};
endmodule
