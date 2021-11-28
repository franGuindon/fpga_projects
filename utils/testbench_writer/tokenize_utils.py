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