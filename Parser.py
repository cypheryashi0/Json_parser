import re

def tokenize(json_string):
    # Define a regex for each token type
    token_specification = [
        ('NUMBER',   r'-?\d+(\.\d*)?([eE][+-]?\d+)?'), # Integer or decimal number
        ('STRING',   r'"([^"\\]*(?:\\.[^"\\]*)*)"'),   # Double-quoted string
        ('TRUE',     r'true'),                        # true
        ('FALSE',    r'false'),                       # false
        ('NULL',     r'null'),                        # null
        ('LBRACE',   r'\{'),                          # {
        ('RBRACE',   r'\}'),                          # }
        ('LBRACKET', r'\['),                          # [
        ('RBRACKET', r'\]'),                          # ]
        ('COMMA',    r','),                           # ,
        ('COLON',    r':'),                           # :
        ('WHITESPACE',r'[ \t\n\r]+'),                 # Skip whitespace
    ]
    
    # Combine the token specifications into a regex pattern
    token_regex = '|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in token_specification)
    
    # List to store the matched tokens
    tokens = []
    
    # Create a scanner to find tokens
    for match in re.finditer(token_regex, json_string):
        token_type = match.lastgroup
        token_value = match.group(token_type)
        if token_type == 'WHITESPACE':
            continue  # Skip whitespace tokens
        elif token_type == 'STRING':
            token_value = token_value[1:-1]  # Remove surrounding quotes from strings
        elif token_type == 'NUMBER':
            token_value = float(token_value) if '.' in token_value or 'e' in token_value.lower() else int(token_value)
        elif token_type == 'TRUE':
            token_value = True
        elif token_type == 'FALSE':
            token_value = False
        elif token_type == 'NULL':
            token_value = None
        tokens.append((token_type, token_value))
    
    return tokens

    

def parse_value(tokens):
    token_type, token_value = tokens.pop(0)
    
    if token_type == 'LBRACE':
        return parse_object(tokens)
    elif token_type == 'LBRACKET':
        return parse_array(tokens)
    elif token_type == 'STRING':
        return token_value
    elif token_type == 'NUMBER':
        return token_value
    elif token_type == 'TRUE' or token_type == 'FALSE':
        return token_value
    elif token_type == 'NULL':
        return token_value
    else:
        raise ValueError(f"Unexpected token: {token_type}")


def parse_object(tokens):
    obj = {}
    
    while tokens:
        token_type, token_value = tokens.pop(0)
        
        if token_type == 'RBRACE':  # End of the object
            return obj
        if token_type == 'STRING':  # Found a key
            key = token_value
            if tokens.pop(0)[0] != 'COLON':  # Expect colon after key
                raise ValueError("Expected ':' after key in object")
            obj[key] = parse_value(tokens)
            
            if tokens[0][0] == 'RBRACE':  # End of the object
                tokens.pop(0)
                return obj
            elif tokens[0][0] != 'COMMA':  # Expect comma between pairs
                raise ValueError("Expected ',' between key-value pairs in object")
            tokens.pop(0)  # Skip the comma

def parse_array(tokens):
    arr = []
    
    while tokens:
        if tokens[0][0] == 'RBRACKET':  # End of array
            tokens.pop(0)
            return arr
        arr.append(parse_value(tokens))
        
        if tokens[0][0] == 'RBRACKET':  # End of array
            tokens.pop(0)
            return arr
        elif tokens[0][0] != 'COMMA':  # Expect comma between values
            raise ValueError("Expected ',' between values in array")
        tokens.pop(0)  # Skip the comma

def parse(json_string):
    tokens = tokenize(json_string)
    return parse_value(tokens)

json_string = '{"name": "Alice", "age": 25, "isStudent": false, "courses": ["Math", "Science"], "address": null}'

parsed_data = parse(json_string)
print(parsed_data)

