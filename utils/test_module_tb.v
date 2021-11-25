`timescale 1ns / 1ps

module TestTB;
   `include "../fileread_utils.vh"
   
   reg clock = 1'b0;
   reg single_input = 1'b0;
   reg [2:0] array_input = 3'b0;
   reg port_not_declared = 1'b0;

   wire single_output;
   wire [2:0] array_output;
   wire single_reg_output;
   wire [2:0] reg_array_output;
   wire single_inout;
   wire [2:0] array_inout;

   reg check_single_output;
   reg [2:0] check_array_output;
   reg check_single_reg_output;
   reg [2:0] check_reg_array_output;
   reg check_single_inout;
   reg [2:0] check_array_inout;

   TestModule TM (
      .clock(clock),
      .single_input(single_input),
      .array_input(array_input),

   );
   
   parameter data = "test_module_tb.mem";
   integer data_file;
   integer file_did_not_open;
   integer half_period = 10;

   initial forever #half_period clk = ~clk;
   
   initial begin
      $display("Opening '%s' ...", data);
      data_file = $fopen(data, "r");
      file_did_not_open = (data_file == 0);
      if (file_did_not_open) $finish;
   end
   
   always @ ( negedge clk ) begin
      data_line = get_line_from_file(data_file);
      $sscanf(
         data_line, "%b %b %b %b %b %b %b %b %b",
         single_input, array_input, port_not_declared,
         check_single_output, check_array_output, check_single_reg_output,
         check_reg_array_output, check_single_inout, check_array_inout
      );
      #(2*half_period - 1);
      $display(
         "%h | %b %b | %b %b | %s",
         single_input, array_input, port_not_declared,
         single_output, array_output, single_reg_output, reg_array_output,
         single_reg_output, reg_array_output, single_inout, array_inout,
         check_single_output, check_array_output, check_single_reg_output,
         check_reg_array_output, check_single_inout, check_array_inout, (
            single_output != check_single_output ||
            array_output != check_array_output ||
            single_reg_output != check_single_reg_output ||
            reg_array_output != check_reg_array_output ||
            single_inout != check_single_inout ||
            array_inout != check_array_inout ? "ERROR" : ""
         )
      );
      
      if ($feof(data_file)) begin
         $display("Closing '%s' ...", data);
         $fclose(data_file);
         $finish;
      end
   end
endmodule
