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

def parse_statements(token_list, start_delimiters, stop_delimiters, sep_delimiters=[]):
    sep_delimiters = [*sep_delimiters, *stop_delimiters]

    parsed_statements = []
    statement_buffer = []
    remaining_tokens = []
    list_to_add_token = remaining_tokens

    for token in token_list:

        if token in start_delimiters:
            list_to_add_token = statement_buffer

        list_to_add_token.append(token)

        if token in sep_delimiters:
            parsed_statements.append(statement_buffer)
            statement_buffer = []
            list_to_add_token = statement_buffer

        if token in stop_delimiters:
            list_to_add_token = remaining_tokens

    parsed_statements = [
        statement for statement in parsed_statements
        if statement != [] and statement[0] not in sep_delimiters
    ]

    return parsed_statements, remaining_tokens

class TokenParser:

    def __init__(s, token_list):
        s.token_list = token_list
        s.parse_comments()
        s.parse_modules()
        s.parse_module_sections()
        s.parse_ports()

    def parse_comments(s):
        s.single_line_comments, s.token_list = parse_statements(
            s.token_list,
            start_delimiters = ['//'],
            stop_delimiters = ['\n']
        )
        s.multiple_line_comments, s.token_list = parse_statements(
            s.token_list,
            start_delimiters = ['/*'],
            stop_delimiters = ['*/']
        )
        s.token_list = [token for token in s.token_list if token != '\n']

    def parse_modules(s):
        s.modules, s.nonmodule_statements = parse_statements(
            s.token_list,
            start_delimiters = ['module'],
            stop_delimiters = ['endmodule']
        )
        s.module_of_interest = s.modules[0]
        
    def parse_module_sections(s):
        s.module_declaration, s.module_body = parse_statements(
            s.module_of_interest,
            start_delimiters = ['module'],
            stop_delimiters = [';']
        )
        s.module_declaration = s.module_declaration[0]
        s.parameter_statement, s.module_declaration = parse_statements(
            s.module_declaration,
            start_delimiters = ['#'],
            stop_delimiters = [')']
        )
        s.port_statement, s.module_declaration = parse_statements(
            s.module_declaration,
            start_delimiters = ['('],
            stop_delimiters = [')']
        )
        s.port_statement = s.port_statement[0]

    def parse_parameters(s):
        get_parameters_from_parameter_statement(

        )

    def parse_ports(s):
        s.inputs_from_port_statement, _ = parse_statements(
            s.port_statement,
            start_delimiters = ['input'],
            stop_delimiters = ['inout', 'output',')'],
            sep_delimiters = [',']
        )

        s.outputs_from_port_statement, _ = parse_statements(
            s.port_statement,
            start_delimiters = ['output'],
            stop_delimiters = ['input', 'inout',')'],
            sep_delimiters = [',']
        )

        s.inouts_from_port_statement, _ = parse_statements(
            s.port_statement,
            start_delimiters = ['inout'],
            stop_delimiters = ['input', 'output',')'],
            sep_delimiters = [',']
        )

def main():
    with open(args.src) as file_obj:
        file_data = file_obj.read()
    
    token_list = tokenize(file_data)
    parsed_tokens = TokenParser(token_list)

if __name__ == '__main__':
    main()