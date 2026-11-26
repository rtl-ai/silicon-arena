module dot8 (input wire [63:0] a,b, output wire signed [31:0] result);
wire signed [15:0] p[0:7];
wire [18:0] x[0:7];
genvar i;
generate for(i=0;i<8;i=i+1) begin: prod
  assign p[i]=$signed(a[8*i+:8])*$signed(b[8*i+:8]);
  assign x[i]={{3{p[i][15]}},p[i]};
end endgenerate
wire [18:0] s0=x[0]^x[1]^x[2];
wire [18:0] c0=((x[0]&x[1])|(x[0]&x[2])|(x[1]&x[2]))<<1;
wire [18:0] s1=x[3]^x[4]^x[5];
wire [18:0] c1=((x[3]&x[4])|(x[3]&x[5])|(x[4]&x[5]))<<1;
wire [18:0] s2=s0^c0^s1;
wire [18:0] c2=((s0&c0)|(s0&s1)|(c0&s1))<<1;
wire [18:0] s3=c1^x[6]^x[7];
wire [18:0] c3=((c1&x[6])|(c1&x[7])|(x[6]&x[7]))<<1;
wire [18:0] s4=s2^c2^s3;
wire [18:0] c4=((s2&c2)|(s2&s3)|(c2&s3))<<1;
wire [18:0] s5=s4^c4^c3;
wire [18:0] c5=((s4&c4)|(s4&c3)|(c4&c3))<<1;
wire [18:0] total=s5+c5;
assign result={{13{total[18]}},total};
endmodule
