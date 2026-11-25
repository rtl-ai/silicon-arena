module gradient_accumulator (
    input wire clk, reset, clear, enable,
    input wire signed [7:0] activation,
    input wire signed [7:0] gradient,
    output reg signed [31:0] total
);
    wire signed [15:0] product = activation * gradient;
    wire signed [31:0] extended = {{16{product[15]}}, product};
    // Exact two's complement modular accumulator. Reset/clear takes priority.
    always @(posedge clk) begin
        if (reset || clear) total <= 32'sd0;
        else if (enable) total <= total + extended;
    end
endmodule
