`ifndef _FILEREAD_UTILS_VH_
`define _FILEREAD_UTILS_VH_

parameter MAX_CHARS = 100;
reg [MAX_CHARS*8-1:0] data_line;

function automatic [MAX_CHARS*8-1:0] get_line_from_file;
   input integer file;
   integer scan_file;
   reg [MAX_CHARS*8-1:0] buffer;
   integer k;
   integer comment_begins_line; 		    
   begin
      scan_file = $fgets(buffer, file);
      while (is_line_comment(buffer) || is_line_whitespace(buffer))
	      scan_file = $fgets(buffer, file);
      get_line_from_file = buffer;
   end
endfunction

function automatic is_line_comment;
   input [MAX_CHARS*8-1:0] line;
   integer k;
   integer comment_begins_line;
   begin
      is_line_comment = 0;
      for (k = (MAX_CHARS-1)*8; k >= 0; k = k - 8) begin
	      comment_begins_line = (
            (line[k-16 +: 8] == "/") &&
			   (line[k-8 +: 8] == "/") &&
			   (line[k +: 8] == 0)
         );
	   if (comment_begins_line)
	      is_line_comment = 1;
      end
   end
endfunction

function automatic is_line_whitespace;
   input [MAX_CHARS*8-1:0] line;
   integer k;
   integer character_is_whitespace;
   integer line_is_null;
   begin
      is_line_whitespace = 1;
      for (k = (MAX_CHARS-1)*8; k >= 0; k = k - 8) begin
	      character_is_whitespace = (
            (line[k +: 8] == 0) ||
				(line[k +: 8] == " ") ||
				(line[k +: 8] == "\t") ||
				(line[k +: 8] == "\n")
         );
	      if (!character_is_whitespace)
	         is_line_whitespace = 0;
      end
      line_is_null = (line[0 +: 8] == 0);
      if (line_is_null)
	      is_line_whitespace = 0;
   end
endfunction

`endif // _FILEREAD_UTILS_VH_