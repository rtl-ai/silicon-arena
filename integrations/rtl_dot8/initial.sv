module dot8 (
    input wire [63:0] a,
    input wire [63:0] b,
    output reg signed [31:0] result
);
    // EVOLVE-BLOCK-START
    integer i;
    reg signed [7:0] lhs, rhs;
    reg signed [15:0] product;
    always @* begin
        result = 0;
        for (i=0; i<8; i=i+1) begin
            lhs = a[i*8 +: 8];
            rhs = b[i*8 +: 8];
            product = lhs * rhs;
            result = result + {{16{product[15]}}, product};
        end
    end
    // EVOLVE-BLOCK-END
endmodule
