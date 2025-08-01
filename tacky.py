import sys
import parser4 as c_ast

class ASTnode:
    pass
########### --- TACKY AST --- ##################

class TACKYProgram(ASTnode):
    def __init__(self, function_definition):
        self.function_definition = function_definition

class TACKYFunction(ASTnode):
    def __init__(self, name,body):
        self.name = name
        self.body = body

class TACKYReturn(ASTnode):
    def __init__(self, val):
        self.val = val

class TACKYConstant(ASTnode):
    def __init__(self, value):
        self.value = value

class TACKYUnary(ASTnode):
    def __init__(self, operator, src, dst):
        self.operator = operator
        self.src = src
        self.dst = dst

class TACKYVar(ASTnode):
    def __init__(self, identifier):
        self.identifier = identifier


########### --- TACKY AST --- ##################
tmp_counter = -1
def make_temp():
    global tmp_counter
    tmp_counter+=1
    return f"tmp.{tmp_counter}"
def convert_unop(node):
    if node.operator == "~" or node.operator == '!':
        return "Complement"
    else:
        return "Negate"

def emit_tacky_expr(node, instructions):
    global tmp_counter
    if isinstance(node, c_ast.CASTConstant):
        return TACKYConstant(node.value)
    elif isinstance(node, c_ast.CASTUnary):
        # we have an operator like ~ or - 
        if node.operator:
            # a node.expression will be either a Unary or constant 
            # so we want to recur on them
            src = emit_tacky_expr(node.exp, instructions)
            # create a temp variable name 
            dst_name = make_temp()
            # wrap the variable dst inside a TACKYVar
            dst = TACKYVar(dst_name)
            # get wether the operator is a complement or negate 
            tacky_op = convert_unop(node)
            # append the operator, the src and the variable to the instructions list
            instructions.append(TACKYUnary(tacky_op, src, dst))
            return dst

def emit_tacky_return(instructions): 
    # we append the return node to the end of the instructions list 
    ident = f"tmp.{tmp_counter}"
    instructions.append(TACKYReturn(TACKYVar(ident)))
            

def parse_program(node, instructions):
    if isinstance(node, c_ast.CASTProgram):
        func_def = parse_program(node.function_definition, instructions)
        return TACKYProgram(func_def)
    elif isinstance(node, c_ast.CASTFunction):
        body = parse_program(node.body, instructions)
        name = node.name
        return TACKYFunction(name, body)
    elif isinstance(node, c_ast.CASTReturn):
        # instructions are a mutable list that can be passed around and edited
        # and this list is updated everywhere
        emit_tacky_expr(node.expression, instructions)
        emit_tacky_return(instructions)
        # changes from return TACKYReturn(expression)
        return instructions
        # return return_exp



def print_tacky5(node):
    if isinstance(node, TACKYProgram):
        print(f"Program (")
        print_tacky5(node.function_definition)
        print(")")
########## -- TACKY AST -- ############
    elif isinstance(node, TACKYFunction):
        print(f"    Function ( ")
        for item in node.body:
            if isinstance(item, TACKYUnary):
                if hasattr(item, 'src') and hasattr(item.src, 'value'):
                   print(f"        {item}({item.operator}, {item.src} ({item.src.value}), {item.dst}({item.dst.identifier}))")
                else:
                    print(f"        {item}({item.operator}, {item.dst}({item.src.identifier}), {item.dst}({item.dst.identifier}))")
            elif isinstance(item, TACKYReturn):
                print(f"        {item}({item.val}({item.val.identifier}))")



 
    
def c_ast_to_tacky(node):
    if isinstance(node, c_ast.CASTProgram):
        # print(f"castprogram: {node}")
        instructions = []
        something = parse_program(node, instructions)
        # print_tacky5(something)
        return something


def run_tacky(c_ast_node):
    # print(f"here c_ast: {c_ast}")
    tacky_ast = c_ast_to_tacky(c_ast_node)
    return tacky_ast
