#!/usr/bin/env python3
# ^^^ tell the os how to run it
# finds the right python interpreter 
# enables direct execution
import sys
import subprocess
import lexer
import lexer2
from rply.errors import LexingError
# change for file change
import parser2
import parser3
import parser4
import codegen
import assembly_maker
# ./compiler_driver return_2.c --lex

# we need there to be a given file to compile
n = len(sys.argv)
if n < 2:
    print("missing file to compile")
# get the file name, this is the input file
input_file = sys.argv[1]


# to run the gcc command we need the file name without the extension
base_file = ''
for char in input_file:
    if(char == '.'):
        break
    base_file += char
# setup the i file extension
i_file = base_file + '.i'

# check for flags
# flag = ''
# if sys.argv[2]:
flag = sys.argv[2] if len(sys.argv) > 2 else ''
print(f"flag given: {flag}")

# --- run lexer if lex flag is passed ---
# we need a place to store tokens from the lexer
tokens = []
if flag == '--lex':
    try:
        # tokens = lexer.run_lexer(input_file)
        tokens = lexer2.run_lexer(input_file)
        # print(tokens)
    except (SyntaxError, LexingError) as e:
        print("Lexer Error:", e)
        sys.exit(1)

if flag == '--parse':
    try:
        tokens = lexer2.run_lexer(input_file)
        # change based on file
        parser4.run_parser(tokens)
    except Error as e:
        print("Parser Error:", e)
        sys.exit(1)

if flag == '--codegen':
    try: 
        tokens = lexer2.run_lexer(input_file)
        ast = parser4.run_parser(tokens)
        as_tree = codegen.run_codegen(ast, tokens)
        s_file = assembly_maker.run_assembler(as_tree)
        # print(f"as_tree: {as_tree}")
    except Error as e:
        print("Codegen Error", e)
        sys.exit(1)


# --- compile if lexer succeeded ---

# we need to compile the file
try:
    i_preprocess = subprocess.check_call(f"gcc -E -P {input_file} -o {i_file}", shell=True)
    print("i preprocess return code:", i_preprocess)
    # subprocess.CalledProcessError is an error rasied from "subprocess" failing
    # it will fail when there is a non zero exit code
except subprocess.CalledProcessError:
    print("Error during pre-processing")
    sys.exit(1)

# s_file = base_file + '.s'
# compile the i file
# i_compile = subprocess.check_call(f"gcc -S {i_file} -o {s_file}", shell=True)
# print("i compile return code: ", i_compile)
# if i_compile != 0:
#     print("issue compiling i file")

# assemble and link the assembly file to produce and executable
assemble_link = subprocess.check_call(f"gcc {s_file} -o {base_file}", shell=True)
print("assemble and link return code: ", assemble_link)
if assemble_link != 0:
    print("issue assembling and linking .s file")


# exit with a code of zero if everything passed
sys.exit(0)







