module dot8 (
    input wire [63:0] a,
    input wire [63:0] b,
    output wire signed [31:0] result
);
    wire signed [15:0] p [0:7];

    generate
        genvar i;
        for (i = 0; i < 8; i = i + 1) begin : mults
            assign p[i] = $signed(a[i*8 +: 8]) * $signed(b[i*8 +: 8]);
        end
    endgenerate

    wire signed [16:0] s1_0 = p[0] + p[1];
    wire signed [16:0] s1_1 = p[2] + p[3];
    wire signed [16:0] s1_2 = p[4] + p[5];
    wire signed [16:0] s1_3 = p[6] + p[7];

    wire signed [17:0] s2_0 = s1_0 + s1_1;
    wire signed [17:0] s2_1 = s1_2 + s1_3;

    wire signed [18:0] s3_0 = s2_0 + s2_1;

    assign result = s3_0;
endmodule
