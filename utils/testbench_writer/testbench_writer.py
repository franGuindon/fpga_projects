from os import path
from argparse_utils import args
from tokenize_utils import tokenize
from tokenparse_utils import TokenParser

def main():
    with open(args.src) as src_obj:
        src_data = src_obj.read()
    
    with open('template_tb.v') as template_obj:
        template_data = template_obj.read()

    token_list = tokenize(src_data)
    parsed_tokens = TokenParser(token_list)

    print(args.output_dir)

if __name__ == '__main__':
    main()