import sys
# other attributes of the token object:
        # .name -> token type name 
        # .value -> actual text matched
        # .source_pos -> line/column info
        # .getsourcepos() -> 
            # lineno -> line number
            # colno -> column number

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
    def __init__(self, number):
        self.number = number
    def children(self):
        return [self.number]

class ReturnStatement(Statement):
    def __init__(self, expression: Exp):
        self.expression = expression
    def children(self):
        return [self.expression]

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


def parse_program(tokens):
    func_def = parse_function(tokens)
    # print(f"func_def fieldtype1: {func_def.name}")
    # print(f"func_def fieltype2: {func_def.body}")
    return Program(func_def)

def parse_function(tokens):
    position = 0
    ident_name = ''

    # check for INT as the start of the function
    current_token = peek(tokens, position)
    if current_token.name != 'INT':
        print(f"parse_function error on token: {current_token.name}")
        sys.exit(1)
    print(current_token.name)
    
    # step into next token check if its main
    position += 1
    current_token = peek(tokens, position)
    identifier_name = parse_identifier(tokens, position)
    print(f"type identifier_name: {type(identifier_name)}")


    print(f"ident name: {ident_name}")

    # check for open parent 
    position += 1
    current_token = peek(tokens, position)
    if current_token.name != 'OPEN_PAREN':
        print("missing open paren, current token: {current_token.name}")
        sys.exit(1)
    print(current_token.name)

    # check for void
    position += 1
    current_token = peek(tokens, position)
    if current_token.name != 'VOID':
        print("missing void, current token: {current_token.name}")
        sys.exit(1)
    print(current_token.name)

    # check for close paren
    position += 1
    current_token = peek(tokens, position)
    if current_token.name != 'CLOSE_PAREN':
        print("missing close paren, current token: {current_token.name}")
        sys.exit(1)
    print(current_token.name)

    # check for open brace:
    position += 1
    current_token = peek(tokens, position)
    if current_token.name != 'OPEN_BRACE':
        print("missing open brace, current token: {current_token.name}")
        sys.exit(1)
    print(current_token.name)
    
    # hand off to check statement
    position += 1
    stmt_node, position = parse_statement(tokens, position)
    print(f"type of stmt_node: {type(stmt_node)}")
    print(f"stmt_node expression: {stmt_node.expression}")
    current_token = peek(tokens, position)
    print(f"Here is the current token: {current_token.name}")

    # now we check for closing brace
    position += 1
    current_token = peek(tokens, position)
    if current_token.name != 'CLOSE_BRACE':
        print("missing close brace, current token: {current_token.name}")
        sys.exit(1)
    print(current_token.name)

    # now we are going to return the function_def node which is the stmt_node
    return Function_Definition(identifier_name, stmt_node) 


def parse_int(token):
    if token.value.isdigit() == False:
        print("parse_int failure")
    
    return True


def parse_exp(tokens, position):

    # the only current exp we support are ints
    # so we pass off the token to pare_int
    current_token = peek(tokens, position)
    if not parse_int(current_token):
        print("parse_exp exp error, current token: {current_token.name}")
        sys.exit(1)
    # now we create an exp_node
    # change to value 06/23
    exp_node = ConstantExp(current_token.value)
    print(f"current_token: {current_token.name}")
    print(f"current_token value: {current_token.value}")
    
    # we return the position and the exp_node to the parse_statement function
    # there should be a semicolon after and expression
    return position, exp_node

def parse_statement(tokens, position):
    current_token = peek(tokens, position)

    # the only current statement we support is RETURN
    if current_token.name != 'RETURN':
         print("parse_statement missing return statement, current token: {current_token.name}")
    
    stmt_node = ReturnStatement(current_token.name)
    position, exp_node = parse_exp(tokens, position + 1)
    # print(f"current exp_node: {exp_node.name}")
    new_node = 
    stmt_node = ReturnStatement(exp_node)

    # now we need to check for a semicolon
    position+=1
    current_token = peek(tokens, position)
    if current_token.name != 'SEMICOLON':
        print("parse_statement missing semicolon, current token: {current_token.name}")
        sys.exit(1)

    return stmt_node, position
 

def parse_identifier(tokens, position):
    current_token = peek(tokens, position)
    if current_token.name != 'MAIN':
        print(f"parse_identifier error on token: {current_token.name}")
        sys.exit(1)
    return MainIdentifier(current_token.name)


def peek(tokens, position):
    return tokens[position]

def pretty_print(node):
    #print(f"program node. func def: {node.function_definition}")
    if isinstance(node, Program) and not isinstance(node, Function_Definition):
        pretty_print(node.function_definition)
    elif isinstance(node, Function_Definition):
        name = node.name.name
        print(f"Func Def:   {name}")
        pretty_print(node.body)
    elif isinstance(node, ReturnStatement):
        value = node.expression.number
        print(f"ReturnStm    {value};")
    elif isinstance(node, ConstantExp):
        print(f"ConstantExp        {node.expression}")
    elif isinstance(node, MainIdentifier):
        print(f"MainIdentifier       {node.name}")
    elif isinstance(node, Identifier):
        print("Ident")

def pretty_print2(node):
    if isinstance(node, Program) and not isinstance(node, Function_Definition):
        print(f"Program {node}")
        pretty_print2(node.function_definition)
    elif isinstance(node, Function_Definition):
        print(f"    Function {node}")
        print(f"        {node.name.name}")
        # print(f"        {node.body.expression}")
        pretty_print2(node.body)
    elif isinstance(node, ConstantExp):
        print("here")
        print(f"        {node.number}")
    elif isinstance(node, ReturnStatement):
        print(f"        {node.expression.number}")
    elif isinstance(node, ConstantExp):
        print(f"            {node.number}")




def run_parser(tokens):
    print(tokens)
    program_node = parse_program(tokens)
    # print(f"program_node.children: {program_node.children}")
    # print(f"type of program_node: {program_node}")
    #
    # func_def = program_node.function_definition
    # print(f"func_def.name: {func_def.name}")
    #
    # stmt = func_def.body
    # ident = func_def.name
    # print(f"stmt: {stmt.expression}")
    # print(f"ident: {ident.name}")
    #
    # print("--- Starting Pretty Print ---")
    # pretty_print(program_node)
    #
    print("--- Pretty Print 2 ---")
    pretty_print2(program_node)
