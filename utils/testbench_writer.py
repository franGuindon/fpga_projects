from argparse_utils import args
import re

def tokenize(string):
    return re.findall(r'\S+|\n', string)

def main():
    with open(args.src) as file_obj:
        file_data = file_obj.read()
    
    file_data = tokenize(file_data)
    print(file_data)

if __name__ == '__main__':
    main()