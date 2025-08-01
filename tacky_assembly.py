from os import wait
import sys
import tacky as tacky_ast

offset = 0
tmp_var_dict = {}

########## -- ASSEMBLY AST -- ############
class ASTnode:
    pass

class ASSEMBLYProgram(ASTnode):
    def __init__(self, function_definition):
        self.function_definition = function_definition

class ASSEMBLYFunction(ASTnode):
    def __init__(self, name, instructions):
        self.name = name
        self.instructions = instructions

class ASSEMBLYMov(ASTnode):
    def __init__(self, src, dst):
        self.src = src
        self.dst = dst

class ASSEMBLYAllocateStack(ASTnode):
    def __init__(self, integer):
        self.integer = integer

class ASSEMBLYImm(ASTnode):
    def __init__(self, integer):
        self.integer = integer

class ASSEMBLYReg(ASTnode):
    def __init__(self, reg):
        self.reg = reg

class ASSEMBLYPseudo(ASTnode):
    def __init__(self, identifier):
        self.identifier = identifier

class ASSEMBLYStack(ASTnode):
    def __init__(self, integer):
        self.integer = integer

class ASSEMBLYReturn(ASTnode):
    pass

class ASSEMBLYConstant(ASTnode):
    def __init__(self, value):
        self.value = value

class ASSEMBLYUnary(ASTnode):
    def __init__(self, unary_operand, operand_dst):
        self.unary_operand = unary_operand
        self.operand_dst = operand_dst

########## -- ASSEMBLY AST -- ############

def parse_return(node, instructions):
    instructions.append(ASSEMBLYMov(stack_offset(node.val.identifier), ASSEMBLYReg("AX")))
    instructions.append(ASSEMBLYReturn())

def parse_unary(node, instructions):
    if hasattr(node, 'src') and hasattr(node.src, 'value'):
        # node.dst.identifier
        # stack_num = stack_offset(node.dst.identifier)
        # print(f"stack_num: {stack_num}")
        # print(f"here!!!!!!!!!!!!!!!!!!!!!!!! {node}, {node.operator}")
        if node.operator == "Negate":
            node_src_value = "-"+node.src.value
            instructions.append(ASSEMBLYMov(ASSEMBLYImm(node_src_value), stack_offset(node.dst.identifier)))
        else:
            instructions.append(ASSEMBLYMov(ASSEMBLYImm(node.src.value), stack_offset(node.dst.identifier)))
    else:
        # stack_num = stack_offset(node.src.identifier)
        # print(f"stack_num: {stack_num}")
        instructions.append(ASSEMBLYMov(ASSEMBLYStack(stack_offset(node.src.identifier)), ASSEMBLYStack(stack_offset(node.dst.identifier))))
    if node.operator == "Complement":
        unary_op = "notl"
    else:
        unary_op = "negl"
    instructions.append(ASSEMBLYUnary(unary_op,stack_offset(node.dst.identifier)))


def make_assembly_ast(node, instructions):
    if isinstance(node, tacky_ast.TACKYProgram): 
        func_def = make_assembly_ast(node.function_definition, instructions)
        return ASSEMBLYProgram(func_def)
    if isinstance(node, tacky_ast.TACKYFunction):
        name = node.name
        for item in node.body:
            if isinstance(item, tacky_ast.TACKYUnary):
                parse_unary(item, instructions)
            if isinstance(item, tacky_ast.TACKYReturn):
                parse_return(item, instructions)
                
        return ASSEMBLYFunction(name, instructions)
    


def print_tacky_program(node):
    if isinstance(node, tacky_ast.TACKYProgram):
        print_tacky_program(node.function_definition)
    if isinstance(node, tacky_ast.TACKYFunction):
        print_tacky_program(node.body)
        print(f"FUNCTION name: {node.name}")
        for item in node.body:
            if isinstance(item, tacky_ast.TACKYUnary):
                if hasattr(item, 'src') and hasattr(item.src, 'value'): 
                    print(f"UNARY = operator: {item.operator}, src: {item.src.value}, dst: {item.dst.identifier} var: {item.dst}")
                else:
                    print(f"UNARY = operator: {item.operator}, src: {item.src.identifier}, dst: {item.dst.identifier} var: {item.dst}")

            elif isinstance(item, tacky_ast.TACKYReturn):
                print(f"RETURN = val.identifier: {item.val.identifier}")

def stack_offset(tmp_var):
    # print(f"tmp var: {tmp_var}")
    global offset
    if tmp_var not in tmp_var_dict:
        
        offset = offset - 4
        tmp_var_dict[tmp_var] = offset
        
        
    # print(tmp_var_dict)
    return_value = tmp_var_dict[tmp_var]
    return return_value
    
                
def print_assembly(node):
    if isinstance(node, ASSEMBLYProgram):
        print(f"Assembly Program ( {node.function_definition}")
        print_assembly(node.function_definition)
        print(")")
    elif isinstance(node, ASSEMBLYFunction):
        print("     Function")
        print(f"        name: {node.name}")
        print(f"        instructions: ")
        print()
        counter = 0
        for item in node.instructions:
            if isinstance(item, ASSEMBLYMov):
                if isinstance(item.src, ASSEMBLYImm):
                    print(f"            Mov(Imm({item.src.integer}), {item.dst})")
                elif isinstance(item.dst, ASSEMBLYReg):
                    print(f"            Mov(Stack({item.src}), Reg({item.dst.reg}))")
                else:
                    # print(f"src: {item.src}, dst: {item.dst}")
                    print(f"            Mov(Stack({item.src.integer}), Stack({item.dst.integer}))")
            elif isinstance(item, ASSEMBLYUnary):
                print(f"            Unary( {item.unary_operand}, Stack({item.operand_dst}))")
            elif isinstance(item, ASSEMBLYReturn):
                print(f"            Ret")
            counter+=1
        # print(f"len: {counter}")

def second_pass(node, instructions):
    # print(f"second_pass: {node}")
    if isinstance(node, ASSEMBLYProgram):
        func_def = second_pass(node.function_definition, instructions)
        return ASSEMBLYProgram(func_def)
    if isinstance(node, ASSEMBLYFunction):
        # insert ASSEMBLYAllocateStack at front of list
        node.instructions.insert(0,ASSEMBLYAllocateStack(offset))
        counter = 0
        func_name = node.name
        for item in node.instructions:
            if isinstance(item, ASSEMBLYMov) and isinstance(item.src, ASSEMBLYStack) and isinstance(item.dst, ASSEMBLYStack):
                # print(f"src: {item.src}, dst: {item.dst}, counter: {counter}, item: {item}")
                node.instructions[counter] = ASSEMBLYMov(f"{item.src.integer}(%rbp)", "%r10d")
                node.instructions.insert(counter+1,ASSEMBLYMov("%r10d", f"{item.dst.integer}(%rbp)"))
            counter+=1
        return ASSEMBLYFunction(func_name, instructions)
        

def print_secondpass(node):
    if isinstance(node, ASSEMBLYProgram):
        print(f"Assembly Program ( {node.function_definition}")
        print_secondpass(node.function_definition)
        print(")")
    elif isinstance(node, ASSEMBLYFunction):
        print("     Function")
        print(f"        name: {node.name}")
        print(f"        instructions:")
        print()
        counter = 0
        for item in node.instructions:
            if isinstance(item, ASSEMBLYMov):
                print(f"{item.src}, {item.dst}")
            else:
                print(item)
            counter+=1
        # print(f"len: {counter}")

def assembly_gen(node, text):
    if isinstance(node, ASSEMBLYProgram):
        assembly_gen(node.function_definition, text)
        text.append(".section .note.GNU-stack,\"\",@progbits\n")
    if isinstance(node, ASSEMBLYFunction):
        text.append(f"  .globl {node.name}\n")
        text.append(f"{node.name}:\n")
        text.append("   pushq   %rbp\n")
        text.append("   movq    %rsp, %rbp\n")
        for item in node.instructions:
            # print(item)
            if isinstance(item, ASSEMBLYAllocateStack):
                text.append(f"  subq ${abs(item.integer)}, %rsp\n")
            elif isinstance(item, ASSEMBLYMov):
                if isinstance(item.src, ASSEMBLYImm):
                    text.append(f"  movl    ${item.src.integer}, {item.dst}(%rbp)\n")
                elif isinstance(item.dst, ASSEMBLYReg):
                    text.append(f"  movl    {item.src}(%rbp), %eax\n")
                else:
                    text.append(f"  movl    {item.src}, {item.dst}\n")
            elif isinstance(item, ASSEMBLYUnary):
                text.append(f"  {item.unary_operand}    {item.operand_dst}(%rbp)\n")
            elif isinstance(item, ASSEMBLYReturn):
                text.append(f"  movq    %rbp, %rsp\n")
                text.append(f"  popq    %rbp\n")
                text.append(f"  ret\n")

    return text

def run_tacky_assembly(node):
    # print_tacky_program(node)
    instructions = []
    assembly_ast = make_assembly_ast(node, instructions)
    # print_assembly(assembly_ast)
    secondpass_ast = second_pass(assembly_ast, instructions)
    # print_secondpass(secondpass_ast)
    assembly_list = []
    assembly_text = assembly_gen(secondpass_ast, assembly_list)
    print("assembly text:\n" + "".join(assembly_text))
