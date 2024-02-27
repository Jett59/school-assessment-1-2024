def tokenize(text: str):
    # Separates the operators from the operands, where operands are strings of alphanumeric characters (possibly including '.'s) and anything else is considered an operator.
    # All operators (which include parentheses) are single character sequences, while operands are as long as possible before hitting an operator.
    tokens = []
    current_operand = ""
    for character in text:
        if character == ' ':
            continue
        if character.isalnum() or character == '.':
            current_operand += character
        else:
            if current_operand:
                tokens.append(current_operand)
                current_operand = ""
            tokens.append(character)
    if current_operand:
        tokens.append(current_operand)
    return tokens

def valid_number(text:str):
    # A valid number is a sequence of digits, optionally followed by a decimal point and more digits.
    # The number can also be preceded by a '-' sign.
    if text[0] == '-':
        text = text[1:]
    decimal_point_count = 0
    for character in text:
        if character == '.':
            decimal_point_count += 1
            if decimal_point_count > 1:
                return False
        elif not character.isdigit():
            return False
    return True

def evaluate_expression(tokens: list[str], variables: dict[str, float]):
    # Replace variable names with their values:
    for i, token in enumerate(tokens):
        if token[0].isalpha():
            if token in variables:
                tokens[i] = str(variables[token])
            else:
                raise ValueError(f"Undefined variable {token}")
        elif not valid_number(token):
            raise ValueError(f"Invalid token {token}")

    # Sort out negative numbers.
    # A negative number can be identified by the fact that there will be a '-' operator with no number to its left.
    # We just check that the next token is a number, and if so place the - into the number and remove the operator.
    i = 0
    while i < len(tokens):
        token = tokens[i]
        if token == '-':
            if i == 0 or not valid_number(tokens[i-1]):
                if i == len(tokens) - 1:
                    raise ValueError("Invalid expression")
                if valid_number(tokens[i+1]):
                    tokens[i+1] = '-' + tokens[i+1]
                    del tokens[i]
                    i -= 1
                else:
                    raise ValueError("Invalid expression")
        i += 1

    # First evaluate parentheses, then ^, then * and /, then + and -.

    # Find the open parenthesis.
    i = 0
    while i < len(tokens):
        token = tokens[i]
        if token == '(':
            # Then find the matching closing one.
            depth = 1
            opening_index = i
            closing_index = None
            for j, token in enumerate(tokens[opening_index+1:]):
                if token == '(':
                    depth += 1
                elif token == ')':
                    depth -= 1
                    if depth == 0:
                        closing_index = j + opening_index + 1
                        break
            if closing_index is None:
                print(tokens)
                raise ValueError("Unclosed parenthesis")
            # replace the entire expression with the evaluated result.
            value = evaluate_expression(tokens[opening_index+1:closing_index], variables)
            del tokens[opening_index:closing_index + 1]
            tokens.insert(opening_index, str(value))
            # Conveniently, i now points to the replaced value. This means we can just continue as before.
        i += 1

    # Find a^b and replace it with the computed result.
    i = 1 # Don't check 1 because we need a token before and after.
          # If there was an operator at index 0 or len(tokens)-1, then it will still be there at the end of this function and the code will detect a syntax error.
    while i < len(tokens) - 1:
        token = tokens[i]
        if token == '^':
            left = float(tokens[i-1])
            right = float(tokens[i+1])
            del tokens[i-1:i+2]
            tokens.insert(i-1, str(left ** right))
            i -= 2
        i += 1

    # Find * and / and replace them with the computed result.
    i = 1
    while i < len(tokens) - 1:
        token = tokens[i]
        if token == '*':
            left = float(tokens[i-1])
            right = float(tokens[i+1])
            del tokens[i-1:i+2]
            tokens.insert(i-1, str(left * right))
            i -= 2
        elif token == '/':
            left = float(tokens[i-1])
            right = float(tokens[i+1])
            del tokens[i-1:i+2]
            if right == 0:
                raise ValueError("Division by zero")
            tokens.insert(i-1, str(left / right))
            i -= 2
        i += 1
    
    # Same for + and -.
    i = 1
    while i < len(tokens) - 1:
        token = tokens[i]
        if token == '+':
            left = float(tokens[i-1])
            right = float(tokens[i+1])
            del tokens[i-1:i+2]
            tokens.insert(i-1, str(left + right))
            i -= 2
        elif token == '-':
            left = float(tokens[i-1])
            right = float(tokens[i+1])
            del tokens[i-1:i+2]
            tokens.insert(i-1, str(left - right))
            i -= 2
        i += 1

    # If we have a single token left, it's the result.
    if len(tokens) == 1:
        return float(tokens[0])
    else:
        raise ValueError("Invalid expression")

def check_variable_name(variable_name: str):
    # Variables must start with an alphabetic character and only contain alphanumeric characters.
    if not variable_name[0].isalpha():
        raise ValueError("Invalid variable name")
    for character in variable_name:
        if not character.isalnum():
            raise ValueError("Invalid variable name")

variables = {}

while True:
    try:
        command = input(">")
        command_tokens = tokenize(command)
        if len(command_tokens) == 0:
            continue
        if len(command_tokens) >= 2 and command_tokens[1] == '=':
            variable_name = command_tokens[0]
            check_variable_name(variable_name)
            expression = command_tokens[2:]
            value = evaluate_expression(expression, variables)
            variables[variable_name] = value
            print(round(value, 2))
        else:
            value = evaluate_expression(command_tokens, variables)
            print(round(value, 2))
    except ValueError as e:
        print(e)
