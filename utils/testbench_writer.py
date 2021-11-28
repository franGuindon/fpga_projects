from os import stat
from argparse_utils import args
import re

def tokenize_words_and_newlines(string):
    return re.findall(r'\S+|\n', string)

def tokenize_pattern_from_string(string: str, pattern: str):
    space_padded_pattern = f' {pattern} '.join(string.split(pattern))
    tokenized_string = space_padded_pattern.strip(' ').split(' ')
    return tokenized_string

def tokenize_single_pattern_from_tokens(tokens: list[str], pattern: str):
    return [
        parsed_token
        for token in tokens
        for parsed_token in tokenize_pattern_from_string(token, pattern)
    ]

def tokenize_patterns_from_tokens(tokens: list[str], *patterns):
    for pattern in patterns:
        tokens = tokenize_single_pattern_from_tokens(tokens, pattern)
    return tokens

def tokenize(string):
    tokens = tokenize_words_and_newlines(string)
    comment_delimiters = ('//', '/*', '*/')
    parameter_delimiters = ('#')
    port_delimiters = ('(',')',',')
    statement_delimiters = (';')
    vector_delimiters = ('[',']',':')
    tokens = tokenize_patterns_from_tokens(
        tokens,
        *comment_delimiters,
        *parameter_delimiters,
        *port_delimiters,
        *statement_delimiters,
        *vector_delimiters
    )
    return tokens

def parse_statements_from_delimiters(token_list, delimiters = ('','')):
    start_delimiter, stop_delimiter = delimiters
    statements = []
    parsing_statement = []
    remaining_tokens = []
    list_to_add_token = remaining_tokens
    
    for token in token_list:
        
        if token == start_delimiter:
            list_to_add_token = parsing_statement
        
        list_to_add_token.append(token)
        
        if token == stop_delimiter:
            list_to_add_token = remaining_tokens
            statements.append(parsing_statement)
            parsing_statement = []

    statements = [statement for statement in statements if statement != []]
    
    return statements, remaining_tokens

def get_ports_from_port_statement(port_statement, direction='input'):
    directions = ['input', 'output', 'inout']
    directions.remove(direction)
    remaining_directions = directions
    ports = []
    parsing_port = []
    remaining_tokens = []
    list_to_add_token = remaining_tokens

    for token in port_statement:

        if token == direction:
            list_to_add_token = parsing_port
            continue
        
        if token in [',',')']:
            ports.append(parsing_port)
            parsing_port = []
            continue
        
        if token in remaining_directions:
            list_to_add_token = remaining_tokens
        
        list_to_add_token.append(token)
    
    ports = [port for port in ports if port != []]

    return ports

def parse_tokens(token_list):
    class Namespace:
        pass
    parsed_tokens = Namespace()
    p = parsed_tokens

    p.single_line_comments, token_list = parse_statements_from_delimiters(
        token_list, delimiters=('//','\n')
    )

    token_list = [token for token in token_list if token != '\n']

    p.multiple_line_comments, token_list = parse_statements_from_delimiters(
        token_list, delimiters=('/*','*/')
    )

    p.modules, p.nonmodule_statements = parse_statements_from_delimiters(
        token_list, delimiters=('module','endmodule')
    )

    module_of_interest = p.modules[0]

    module_declaration, p.module_body = parse_statements_from_delimiters(
        module_of_interest, delimiters=('module',';')
    )

    module_declaration = module_declaration[0]

    p.parameter_statement, module_declaration = parse_statements_from_delimiters(
        module_declaration, delimiters=('#',')')
    )

    port_statement, p.module_declaration = parse_statements_from_delimiters(
        module_declaration, delimiters=('(',')')
    )


    p.port_statement = port_statement[0]

    p.inputs_from_port_statement = get_ports_from_port_statement(
        p.port_statement, direction='input'
    )

    p.outputs_from_port_statement = get_ports_from_port_statement(
        p.port_statement, direction='output'
    )

    p.inouts_from_port_statement = get_ports_from_port_statement(
        p.port_statement, direction='inout'
    )

    return parsed_tokens

def main():
    with open(args.src) as file_obj:
        file_data = file_obj.read()
    
    token_list = tokenize(file_data)
    parsed_tokens = parse_tokens(token_list)

    print(parsed_tokens.inouts_from_port_statement)

if __name__ == '__main__':
    main()