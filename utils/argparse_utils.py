import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    'src', type=str,
    help = 'Verilog source file containing module'\
        ' to generate testbench for'
)
args = parser.parse_args()