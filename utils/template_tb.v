`timescale 1ns / 1ps

module TestTB;
    `include "../fileread_utils.vh"

    parameter data = ".mem";
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
            data_line, "",
        );
        #(2*half_period - 1);
        $display(
            "",
        );
        
        if ($feof(data_file)) begin
            $display("Closing '%s' ...", data);
            $fclose(data_file);
            $finish;
        end
    end
endmodule