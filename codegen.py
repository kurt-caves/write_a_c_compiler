import sys
from parser4 import CASTProgram, CASTFunction, CASTReturn, CASTFunction, CASTConstant


class ASTnode:
    pass
########### --- Assembly AST ---##############
class ASProgram(ASTnode):
    def __init__(self, function_definition):
        self.function_definition = function_definition

class ASFunction(ASTnode):
    def __init__(self, name, instructions):
        self.name = name
        self.instructions = instructions

class ASMov(ASTnode):
    def __init__(self, src, dst):
        self.src = src
        self.dst = dst

class ASRet(ASTnode):
    pass

class ASImm(ASTnode):
    def __init__(self, value):
        self.value = value

class Register(ASTnode):
    pass
########### --- Assembly AST --- ##############

def pretty_print_AS_AST(node): 

    # print(f"print_ASTree: {node}")
    if isinstance(node, ASProgram):
        print(f"Assembly Program (");
        pretty_print_AS_AST(node.function_definition)
    elif isinstance(node, ASFunction):
        print(f"    Assembly Function (")
        print(f"        name = {node.name}")
        print(f"        instructions (")
        pretty_print_AS_AST(node.instructions[0])
        pretty_print_AS_AST(node.instructions[1])
        print("         )")
        print("     )")
    elif isinstance(node, ASMov):
        print(f"            Mov (")
        print(f"                src = {node.src.value}")
        print(f"                dst = {node.dst}")
        print("             )")
    elif isinstance(node, ASRet):
        print(f"            Ret ()")


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

def compile_ASProgram(node):
    # print(f"here: {node}")
    asprogram_node = compile_ASFunction(node.function_definition)
    return ASProgram(asprogram_node)


def unpack_CASTConstant(node):
    # here we get the node constant from CASTConstant
    # make a ASImm node and return it
    # print(f"unpack_CASTConstant: {node}")
    return ASImm(node.value)

def unpack_CASTReturn(node):
    # print(f"unpack_CASTReturn {node}")
    # we have a CASTReturn node which contains a statement
    # and an expression
    # the statement is RETURN in this case
    # the expression is "CONSTANT 2"

    # we have made the ASProgram node and the ASFunction Node
    # now we need to make the ASMov node and the ASRet node
    
    # we need to make the source, the dst
    # src will be 2 in this case and dst will be null at this point

    # but we need to return the ASMov and ASRet together

    # 1st we need the value
    src = unpack_CASTConstant(node.expression)
    # print(f"src: {src.value}")
    # 2nd we need a dst
    dst = ''
    mov_node = ASMov(src, dst)


    # 3rd we need a ASRet node
    ret_node = ASRet()

    # then we return the mov and ret nodes as one thing
    return mov_node, ret_node

    
def compile_ASFunction(node):
    # name = node.name
    # instructions = unpack_CASTReturn(node.body)
    # print("compile_ASFunction here")
    # print("--- what CASTFunction has: ---")
    # print(f"name: {node.name}, body: {node.body}")
    # the name comes from the CASTFunction node
    name = node.name
    # print(f"compile_ASFunction name: {name}")
    # instructions will be the CASTFunction body
    # its coming back as a tuple
    instructions = unpack_CASTReturn(node.body)

    # now that we have returned from unpack CASTReturn lets
    # see what is in instructions
    # print(f"instructions: {instructions}")

    # accesing both nodes:
    # print(f"ASMov: {instructions[0]}, ASRet: {instructions[1]}")

    # we should be able to get src and dst from instructions[0]
    # which is src then its a ASImm node which holds the value 
    # print(f"ASMov src {instructions[0].src.value}, ASMov dst: {instructions[0].dst}")

    return ASFunction(name,instructions)

def compile_ASTree(ast_node):
    print(f"compile_ASTree ast_node: {ast_node}")
    print("here")
    if isinstance(ast_node, CASTProgram):
        print("here")
        AS_node = compile_ASProgram(ast_node)
    return AS_node   


def run_codegen(ast, tokens):
    # program_node = parse_program(tokens)
    print(f"this is the AST!!!! {ast}")
    ASTree = compile_ASTree(ast)
    pretty_print_C_AST(ast)
    print()
    print("--------- Assembly Tree -----------")
    pretty_print_AS_AST(ASTree)
    return ASTree
