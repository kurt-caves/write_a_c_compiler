import sys
from codegen import ASProgram, ASFunction, ASMov, ASRet, ASImm

def run_assembler(as_tree):
    print(f"inside run_assembler {as_tree}")
