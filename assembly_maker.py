import sys
from codegen import ASProgram, ASFunction, ASMov, ASRet, ASImm
from codegen import pretty_print_AS_AST

def write_x86(node, text):
    if isinstance(node, ASProgram):
        write_x86(node.function_definition, text)
        return text
    elif isinstance(node, ASFunction):
        text.append(f"  .globl {node.name}\n")
        text.append(f"{node.name}:\n")
        write_x86(node.instructions[0], text)
        write_x86(node.instructions[1], text)
    elif isinstance(node, ASMov):
        text.append(f"  movl    ${node.src.value}, %eax\n")
    elif isinstance(node, ASRet):
        text.append(f"  ret\n")


def write_arm_assembly(node, text):
    if isinstance(node, ASProgram):
        write_arm_assembly(node.function_definition, text)
        return text
    elif isinstance(node, ASFunction):
        text.append(f"       .globl  _{node.name}\n")
        text.append(f"       .p2align   2\n")
        text.append(f"_{node.name}:                ; @{node.name}\n")
        text.append(f"       .cfi_startproc\n")
        write_arm_assembly(node.instructions[0], text)
        write_arm_assembly(node.instructions[1], text)
    elif isinstance(node, ASMov):
        text.append(f"       mov w0, #{node.src.value}\n")
    elif isinstance(node, ASRet):
        text.append(f"       ret\n")

def print_x86(text, output_file):
    print("print_x86")
    with open(output_file,"w")as file:
        for line in text:
            file.write(line)
    return output_file

        
def print_arm_assembly(text, output_file):
    with open(output_file,"w")as file:
        for line in text:
            file.write(line)
        file.write(f"       .cfi_endproc\n")
        file.write(f"                               ;End function")
    return output_file

def run_assembler(as_tree):
    pretty_print_AS_AST(as_tree)
    print(f"inside run_assembler {as_tree}")
    output_file = 'return_2.s'
    text = []
    text = write_arm_assembly(as_tree,text)
    written_file = print_arm_assembly(text, output_file)
    # text = write_x86(as_tree,text)
    # written_file = print_x86(text, output_file)
    return written_file
