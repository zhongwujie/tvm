# Create a new project
create_project example_project ./example_project -part xc7a35tcsg324-1

# Create a new Verilog file
set verilog_file [open "./example_project/top.v" w]
puts $verilog_file "module top(input wire a, input wire b, output wire y);
assign y = a & b;
endmodule"
close $verilog_file

# Add the Verilog file to the project
add_files ./example_project/top.v

# Set the top module
set_property top top [current_fileset]

# Run synthesis
launch_runs synth_1

# Wait for synthesis to complete
wait_on_run synth_1

# Report synthesis status
if {[get_property STATUS [get_runs synth_1]] == "synth_design Complete"} {
    puts "Synthesis completed successfully."
} else {
    puts "Synthesis failed."
}

# Close the project
close_project