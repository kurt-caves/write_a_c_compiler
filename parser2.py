import sys

class ASTnode:
    pass

class Program(ASTnode):
    def __init__(self, function_definition):
        self.function_definition = function_definition
    def children(self):
        return [self.function_definition]

class Identifier:
    pass
class Statement:
    pass
class Exp:
    pass

class MainIdentifier(Identifier):
    def __init__(self, name):
        self.name = name
    def children(self):
        return [self.name]

class ConstantExp(Exp):
    def __init__(self, type_exp, value):
        self.type_exp = type_exp
        self. value = value
    def children(self):
        return [self.number]

class ReturnStatement(Statement):
    def __init__(self, name, expression):
        self.name = name
        self.expression = expression
    def children(self):
        return [self.name, self.expression]

class Function_Definition(Program):
    # this is considered the Function constructor
    # a Function has:   
        # name: Identifier
        # body: Statement
    def __init__(self, name: Identifier, body: Statement):
        self.name = name
        self.body = body
    def children(self):
        return [self.name, self.body]

def parse_exp(tokens, pos):
    current_token = peek(tokens, pos)
    print(f"{current_token.name}")
    # all we currently support are Constant expressions
    if current_token.name != 'CONSTANT':
        print(f"unsupported expression: {current_token.name}")
        sys.exit(1)
    type_exp = current_token.name
    # the only type of Constant we support currently is an int
    if current_token.value.isdigit == False:
        print(f"unsupported constant type: {current_token.value}")
        sys.exit(1)
    # we need to check that there is a semicolon at the end of the exp
    # pos+=1 
    current_token = peek(tokens, pos)
    #print(f"{current_token.name}")
    
    return ConstantExp(current_token.name, current_token.value), pos
    

def parse_return(tokens, pos):
    current_token = peek(tokens, pos)
    print(f"{current_token.name}")
    # we should have a return statement here
    # and we want to return that return stmt
    if current_token.name != 'RETURN':
        print(f"missing RETURN, {current_token.name}")
        sys.exit(1)
    ret_stmt = current_token.name
    
    # now we need to parse the expression
    pos+=1
    expression, pos = parse_exp(tokens, pos)
    returned_body = ReturnStatement(ret_stmt, expression)

    return returned_body, pos


def parse_statement(tokens, pos):
    current_token = peek(tokens, pos)
    # need to check if we have a return statement
    body = parse_return(tokens, pos)

    # inside the return statement is the constant(2)
    # body = parse_exp()

    return body 

def parse_identifier(tokens, pos):
    current_token = peek(tokens, pos)
    #print(f"here {current_token.name}")
    if current_token.name != 'MAIN':
        print(f"parse_identifier error on token: {current_token.name}")
        sys.exit(1)
    return MainIdentifier(current_token.name)

def parse_program(tokens):
    func_def = parse_function(tokens)
    return Program(func_def)

def parse_function(tokens):
    # keep track where we are in the tokens
    pos = 0
    ident_name = ''
    body = ''
    # check for INT
    current_token = peek(tokens, pos)
    if current_token.name != 'INT':
        print(f"parse_function error on token: {current_token.name}")
        sys.exit(1)
    print(current_token.name)

    # step into next token, check if its main
    pos+=1
    current_token = peek(tokens,pos)
    ident_name = parse_identifier(tokens, pos)
    #print(ident_name)
    print(f"{current_token.name}")

    # check for open paren
    pos+=1
    current_token = peek(tokens, pos)
    if current_token.name != 'OPEN_PAREN':
        print("missing open paren, current token: {current_token.name}")
        sys.exit(1)
    print(f"{current_token.name}")

    # check for void
    pos+=1
    current_token = peek(tokens, pos)
    if current_token.name != 'VOID':
        print("missing void, current token: {current_token.name}")
        sys.exit(1)
    print(f"{current_token.name}")

    # check for close paren
    pos+=1
    current_token = peek(tokens,pos)
    if current_token.name != 'CLOSE_PAREN':
        print("missing close paren, current token: {current_token.name}")
        sys.exit(1)
    print(f"{current_token.name}")

    # check for open brace
    pos+=1
    current_token = peek(tokens, pos)
    if current_token.name != 'OPEN_BRACE':
        print("missing open brace, current token: {current_token.name}")
        sys.exit(1)
    print(f"{current_token.name}")

    # step into statement non terminal
    pos+=1 
    current_token = peek(tokens, pos)
    body,pos = parse_statement(tokens, pos)

    # temp
    pos+=1

    # check for closing brace
    pos+=1
    current_token = peek(tokens, pos)
    print(f"{current_token.name}")
    if current_token.name != 'CLOSE_BRACE':
        print("missing close brace, current token: {current_token.name}")
        sys.exit(1)


    return Function_Definition(ident_name, body)


def peek(tokens, pos):
    return tokens[pos]

def pretty_print(node):
    # non terminal
    if isinstance(node,Program) and not isinstance(node, Function_Definition):
        print(f"Program (")
        pretty_print(node.function_definition)
        print(")")
    # non terminal
    elif isinstance(node,Function_Definition):
        print(f"    Function (")
        pretty_print(node.name)
        pretty_print(node.body)
        print(" )")
    # terminal
    elif isinstance(node, MainIdentifier):
        print(f"        name {node.name}") 
    elif isinstance(node, ReturnStatement):
        print(f"        body {node.name} (")
        pretty_print(node.expression)
        print("     )")
    elif isinstance(node, ConstantExp):
        print(f"            {node.type_exp}({node.value})")

def run_parser(tokens):
    print(tokens)
    program_node = parse_program(tokens)

    print("--- Pretty Print 2 ---")
    pretty_print(program_node)
    return program_node
