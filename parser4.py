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
    def __init__(self, value):
        self.value = value
class CASTUnary(ASTnode):
    def __init__(self, operator, exp):
        self.operator = operator
        self.exp = exp
########### --- C AST --- ##################
def peek(tokens, pos):
    return tokens[pos]

# def pretty_print_C_AST(node):
#     if isinstance(node, CASTProgram):
#         print(f"Program (")
#         pretty_print_C_AST(node.function_definition)
#         print(")")
#     elif isinstance(node, CASTFunction):
#         print(f"    Function (")
#         print(f"        name = {node.name}")
#         # print(f"        body = {node.body.statement} (")
#         pretty_print_C_AST(node.body)
#         print("     )")
#     elif isinstance(node, CASTConstant):
#         print(f"            {node.type_token}({node.value})")
#     elif isinstance(node, CASTReturn):
#         print(f"        body = {node.statement}")
#         pretty_print_C_AST(node.expression)

def new_pretty_print_C_AST(node):
    if isinstance(node, CASTProgram):
        print(f"Program (")
        new_pretty_print_C_AST(node.function_definition)
        print(")")
    elif isinstance(node, CASTFunction):
        print(f"    Function (")
        print(f"        name = {node.name}")
        # print(f"        body = {node.body.statement} (")
        new_pretty_print_C_AST(node.body)
        print("     )")
    elif isinstance(node, CASTReturn):
        print(f"        body = ({node.statement}")
        new_pretty_print_C_AST(node.expression)
        print("                 )")
    elif isinstance(node, CASTUnary):
        
        if node.operator == '~' or node.operator == '!':
            print(f"               Unary(Complement: {node.operator},")
        else:
            print(f"               Unary(Negate: {node.operator},") 
        new_pretty_print_C_AST(node.exp)
        print("                     )")
    elif isinstance(node, CASTConstant):
        print(f"                Constant  ({node.value})")


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
    # print(f"parse_exp2, current token: {current_token[1]}")
    # if current token is an int save it
    if current_token[1] == 'CONSTANT':
        constant = CASTConstant(current_token[0])
        return (constant, pos+1)
    # elseif current token is ~ or -
    elif (
            current_token[1] == 'TILDE' 
            or current_token[1] == 'DECREMENT' 
            or current_token[1] == 'NEGATION' 
            or current_token[1] == 'SHEBANG'
        ):
        operator = current_token[0]
        inner_exp, new_pos = parse_exp2(tokens, pos+1)
        unary = CASTUnary(operator, inner_exp)
        return (unary, new_pos)
        # return CASTUnary(operator, inner_exp)
    elif current_token[1] == 'OPEN_PAREN':
        current_token = unbury(tokens, pos)
        inner_exp, new_pos = parse_exp2(tokens, pos+1)
        return (inner_exp, new_pos)
        # return inner_exp
    
 

 
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

    # we need to parse what is after the return and get the position
    # after the expression as well
    print(f"first pos: {pos}")
    expression, pos = parse_exp2(tokens, pos)
    print(f"second pos: {pos}")
    

    # print(f"expression: {expression}")
    # print(f"expresion.exp: {expression.exp}")
    # print(f"expression.operator: {expression.operator}")
    # print(f"expression.exp.operator: {expression.exp.operator}")
    # print(f"expresion.exp.exp.value: {expression.exp.exp.value}")

    # the current token should be the constant
    # we next need to check for the semicolon
    # after incrementing pos
    # pos+=1
    current_token = peek(tokens, pos)
    print(f"parse statement current_token {current_token}")
    
    # if we have something like this `return -(~2)` we will return from parse expression and
    # be at a close paren so we advance and grab the current token again
    if current_token[1] == 'CLOSE_PAREN':
        print("here")
        pos+=1
    current_token = peek(tokens, pos)

    if current_token[1] != 'SEMICOLON':
        print(f"parse_statement missing semicolon, current token: {current_token[1]}")
        sys.exit(1)

    tobe_returned = CASTReturn(statement, expression)
    print(f"tobe_returned: {tobe_returned}")
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
    print(f"body!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!: {body}")
    print(f"return: {body.expression}")


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
    new_pretty_print_C_AST(program_node)
    # print(f"""
    #       program,
    #       function_definition: {program_node.function_definition},
    #       function: {program_node.function_definition.name},
    #       epxression: {program_node.function_definition.expression}
    #
    # """)

    return program_node
