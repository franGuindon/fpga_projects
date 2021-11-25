`timescale 1ns / 1ps

module TestModule (
    input clock,
    input single_input,
    input [2:0] array_input,
    output single_output,
    output [2:0] array_output,
    output reg single_reg_output,
    output reg [2:0] reg_array_output,
    inout single_inout,
    inout [2:0] array_inout,
    port_not_declared
);
    input port_not_declared;

endmodule