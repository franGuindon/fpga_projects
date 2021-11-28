`timescale 1ns / 1ps
// single line comment test
/* multiple line
comment test
*/
module TestModule #(parameter N = 10 )(
    input clock,
    input single_input, // single line comment inside module
    input/* multiple line comment inside module */[2:0] array_input,
    output single_output,
    output [N-1:0] array_output,
    output reg single_reg_output,
    output reg [N-1:0] reg_array_output,
    inout single_inout,
    inout [N-1:0] array_inout
);
    

endmodule

module SecondTestModule (
    input clock
);

endmodule