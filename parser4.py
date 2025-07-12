import sys

class ASTnode:
    pass
########### --- C AST --- ##################
class CASTProgram(ASTnode):
    def __init__(self, function_definition):
        self.function_definition = function_definition

class CASTFunction(ASTnode):
    def __init__(self, name, body):
        self.name = name
        self.body = body

class CASTReturn(ASTnode):
    def __init__(self, statement, expression):
        self.statement = statement
        self.expression = expression

class CASTConstant(ASTnode):
    def __init__(self, type_token, value):
        self.type_token = type_token
        self.value = value
class CASTUnary(ASTnode):
    def __init__(self, operator, exp):
        self.operator = operator
        self.exp = exp
########### --- C AST --- ##################
def peek(tokens, pos):
    return tokens[pos]

def pretty_print_C_AST(node):
    if isinstance(node, CASTProgram):
        print(f"Program (")
        pretty_print_C_AST(node.function_definition)
        print(")")
    elif isinstance(node, CASTFunction):
        print(f"    Function (")
        print(f"        name = {node.name}")
        # print(f"        body = {node.body.statement} (")
        pretty_print_C_AST(node.body)
        print("     )")
    elif isinstance(node, CASTConstant):
        print(f"            {node.type_token}({node.value})")
    elif isinstance(node, CASTReturn):
        print(f"        body = {node.statement}")
        pretty_print_C_AST(node.expression)

def parse_identifier(current_token, pos):
    if current_token[1] != 'MAIN':
        print(f"parse_identifier error on token: {current_token[1]}")
        sys.exit(1)
    # print(current_token.name)
    # we want to increment the pos of the cursor
    pos+=1
    return ('main',pos)

def check_void(current_token, pos):

    if current_token[1] == "VOID":
        print(f"current_token in check_void: {current_token}")
        pos+=1
    return pos

def parse_exp(tokens, pos):
    current_token = peek(tokens, pos)
    
    
    if current_token[1] != 'CONSTANT':
        print(f"unsupported expression: {current_token[1]}")
        sys.exit(1)
    type_token = current_token[1]
    # now we can check if the constant type is an integer
    current_token = peek(tokens, pos)
    # print(f"{current_token.value}")
    if current_token[0].isdigit == False:
        print(f"unsupported constant type: {current_token[0]}")
        sys.exit(1)
    value = current_token[0]
    #print(f"integer: {value}")
    
    # now we need to make sure there is a semi colon
    pos+=1
    current_token = peek(tokens, pos)
    if current_token[1] != 'SEMICOLON':
        print("parse_statement missing semicolon, current token: {current_token[1]}")
        sys.exit(1)
    # print(f"{current_token.name}")

    constant = CASTConstant(type_token, value)
    return (constant, pos)

def unbury(tokens, pos):
    current_token = peek(tokens,pos)
    print(f"in unbury, current_token = {current_token}")
    while current_token[1] == 'OPEN_PAREN':
        pos+=1
        current_token = peek(tokens,pos)
        if current_token[1] != 'OPEN_PAREN':
            break
    return current_token[1]

def parse_exp2(tokens, pos):
    current_token = peek(tokens,pos)
    print(f"parse_exp2, current token: {current_token[1]}")
    # if current token is an int save it
    if current_token[1] == 'CONSTANT':
        constant = current_token[0]
        return CASTConstant(current_token[1],constant)
    # elseif current token is ~ or -
    elif current_token[1] == 'TILDE' or current_token[1] == 'DECREMENT' or current_token[1] == 'NEGATION':
        operator = current_token[0]
        inner_exp = parse_exp2(tokens, pos+1)
        return CASTUnary(operator, inner_exp)
    elif current_token[1] == 'OPEN_PAREN':
        current_token = unbury(tokens, pos)
        inner_exp = parse_exp2(tokens, pos+1)
        return inner_exp
    
 

 
def parse_statement(tokens, pos):
    current_token = peek(tokens, pos)
    print(f"parse_statement: {current_token[1]}")
    if current_token[1] == 'SINGLE_COMMENT' or current_token[1] == current_token[1] == 'MULTI_COMMENT':
        pos+=1
        current_token = peek(tokens, pos)
    # the only statement we currently support is a RETURN
    if current_token[1] != 'RETURN':
        print(f"missing RETURN, {current_token[1]}")
        sys.exit(1)
    # the statement is RETURN
    statement = current_token[1]
    # we have processed the return so we increment the pos
    pos+=1
    expression = parse_exp2(tokens, pos)
    # get past the semicolon
    # expression = operator, inner_exp
    # print(f"expression: {expression}")
    print(f"expression: {expression.operator}, {expression.exp}")
    print("herre")
    tobe_returned =CASTReturn(statement, expression) 
    return tobe_returned, pos 

def parse_function(tokens):
    pos = 0
    ident_name = ''
    body = ''
    # check for int
    current_token = peek(tokens, pos)
    if current_token[1] != 'INT':
        print(f"parse_function error on token: {current_token[1]}")
        sys.exit(1)
    # print(current_token.name)

    # check for identifier
    pos+=1
    current_token = peek(tokens, pos)
    ident_name, pos = parse_identifier(current_token, pos)

    
    current_token = peek(tokens, pos)
    if current_token[1] != 'OPEN_PAREN':
        print("missing open paren, current token: {current_token[1]}")
        sys.exit(1)
    
    # check for void
    pos+=1
    current_token = peek(tokens, pos)
    pos = check_void(current_token, pos)

    # check for close paren
    current_token = peek(tokens,pos)
    print(f"check for close paren, current_token: {current_token[1]}")
    if current_token[1] != 'CLOSE_PAREN':
        print("missing close paren, current token: {current_token[1]}")
        sys.exit(1)
    # print(f"{current_token.name}")

    # check for open brace
    pos+=1
    current_token = peek(tokens, pos)
    if current_token[1] != 'OPEN_BRACE':
        print("missing open brace, current token: {current_token[1]}")
        sys.exit(1)
    # print(f"{current_token.name}")
    

    # ok now we will step into the body
    pos+=1
    current_token = peek(tokens, pos)
    body, pos = parse_statement(tokens, pos)

    # need to check for closing brace, we should be at a
    # semicolon so we increment
    pos+=1
    current_token = peek(tokens, pos)
    # print(f"{current_token.name}")
    if current_token[1] != 'CLOSE_BRACE':
        print(f"missing close brace, current token: {current_token[1]}")
        sys.exit(1)


    return CASTFunction(ident_name, body)
    

def parse_program(tokens):
    print(f"tokens: {tokens}")
    program_node = parse_function(tokens)
    # return a program node
    return CASTProgram(program_node)

def run_parser(tokens):
    # print(tokens)
    # print("parser4.py here")
    program_node = parse_program(tokens)
    # pretty_print_C_AST(program_node)
    return program_node
