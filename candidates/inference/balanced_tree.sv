// Research candidate: range-bounded balanced adder tree.
// Not a ranked PPBA improvement until independent formal and physical checks.
module dot8 (
    input wire [63:0] a,
    input wire [63:0] b,
    output wire signed [31:0] result
);
    wire signed [15:0] p [0:7];
    wire signed [16:0] pair [0:3];
    wire signed [17:0] quad [0:1];
    wire signed [18:0] sum8;
    genvar i;
    generate
        for (i=0; i<8; i=i+1) begin : products
            wire signed [7:0] lhs = a[i*8+:8];
            wire signed [7:0] rhs = b[i*8+:8];
            assign p[i] = lhs * rhs;
        end
        for (i=0; i<4; i=i+1) begin : pairs
            assign pair[i] = $signed({p[2*i][15],p[2*i]}) +
                             $signed({p[2*i+1][15],p[2*i+1]});
        end
        for (i=0; i<2; i=i+1) begin : quads
            assign quad[i] = $signed({pair[2*i][16],pair[2*i]}) +
                             $signed({pair[2*i+1][16],pair[2*i+1]});
        end
    endgenerate
    assign sum8 = $signed({quad[0][17],quad[0]}) +
                  $signed({quad[1][17],quad[1]});
    assign result = {{13{sum8[18]}},sum8};
endmodule
