import sys
import subprocess
import lexer

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

# we need to compile the file
s = subprocess.check_call(f"gcc -E -P {input_file} -o {i_file}", shell=True)
print("return code:", s)
if s != 0:
    print("issue compiling file")

# check for flags
flag = ''
if sys.argv[2]:
    flag = sys.argv[2]
print(f"flag given: {flag}")

if flag == '--lex':
    lexer.run_lexer(input_file)





