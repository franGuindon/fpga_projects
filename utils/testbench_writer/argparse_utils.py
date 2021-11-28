import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    'src', type=str,
    help = 'Verilog source file containing module to generate testbench for'
)
parser.add_argument(
    '-o', '--output-dir' type=str,
    help = 'Output directory to save generated testbench files'
)
args = parser.parse_args()