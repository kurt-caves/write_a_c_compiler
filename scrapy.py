
import re, sys
from rply import LexerGenerator

lg = LexerGenerator()
lg.add('INT', r'int\b')
lg.add('MAIN', r'main\b')
lg.add('VOID',   r'void\b')
lg.add('RETURN', r'return\b')
lg.add('CHAR',   r'char\b')
lg.add('IDENTIFIER', r'[a-zA-Z_]\w*\b')
lg.add('CONSTANT', r'[0-9]+\b')
lg.add('OPEN_PAREN', r'\(')
lg.add('CLOSE_PAREN', r'\)')
lg.add('OPEN_BRACE', r'\{')
lg.add('CLOSE_BRACE', r'\}')
lg.add('SEMICOLON', r';')
lg.ignore(r'\s+')
lexer = lg.build()


with open("return_2.c","r") as file:
    # .read() reads all the text from an open file and makes
    # a string out of it
    code = file.read()
    # print(type(code))
    # print(code)

    # .lex() Takes a string of source code 
    # and returns a generator of Token objects
    # converts string to tokens
    for token in lexer.lex(code):

        # other attributes of the token object:
        # .name -> token type name 
        # .value -> actual text matched
        # .source_pos -> line/column info
        # .getsourcepos() -> 
            # lineno -> line number
            # colno -> column number
        print(
                f"token name: {token.name}," 
                "token.value: {token.value}," 
                "token pos: {token.source_pos}"
            )

        
        

    # for name, pattern in token_specification:
    #     print(f"{name}, {pattern}")
# import re, sys
# token_specification = [
#     ('INT',    r'int\b'),
#    ('MAIN',     r'main\b'),
#     ('VOID',   r'void\b'),
#     ('RETURN', r'return\b'),
#     ('CHAR',   r'char\b'),
#     ('IDENTIFIER', r'[a-zA-Z_]\w*\b'),
#     ('CONSTANT', r'[0-9]+\b'),
#     ('OPEN_PAREN', r'\('),
#     ('CLOSE_PAREN', r'\)'),
#     ('OPEN_BRACE', r'\{'),
#     ('CLOSE_BRACE', r'\}'),
#     ('SEMICOLON', r';'),
# ]
# #  we are going to build a master pattern
# pattern_parts = []
# # stick or between each pattern
# for token, pattern in token_specification:
#       part = f'(?P<{token}>{pattern})'
#       pattern_parts.append(part)
# # print(pattern_parts)
# combined_pattern = '|'.join(pattern_parts)
# # print("combined parts:\n",combined_pattern)
# master_pattern = re.compile(combined_pattern)
# def run_lexer(input_file):
#     print("\n--- lexer ---\n")
#     with open(input_file, "r") as file:
#         index = 0
#         line_number = 1
#         brace_depth = 0
#         # for each line that ends with '\n'
#         for line in file:
#             # our index is used to keep track of current start of
#             # a possible matchcd %:p:hcd %:p:h
#             while index < len(line):
#                 # if the character at the current index is a 
#                 # space, tab or newline we increment as to remove
#                 # them from our current string
#                 while index < len(line) and line[index] in " \t\n":
#                     index+=1
#                 # we dont want to go over the length of the line
#                 # and get an out of bounds error
#                 if index >= len(line):
#                     break
#                 # if we have:
#                 #   int main(void) {
#                 # our first substring will be int main(void) {
#                 # the second substring will be main(void) {
#                 substring = line[index:]
#                 # match() will match from the start of the string up
#                 # to the end of the substring
#                 match = master_pattern.match(substring)
#                 if match is not None:
#                     print(match.lastgroup, match.group())
#                     # if we have a match we need to update our index
#                     # to start at the next space or word
#                     if match.lastgroup == "OPEN_BRACE":
#                         brace_depth+=1 
#                     if match.lastgroup == "CLOSE_BRACE":
#                         brace_depth-=1
#                     if match.lastgroup == "IDENTIFIER" and brace_depth == 0:
#                         print("Error ident outside brace depth")
#                         # sys.exit(1)
#                     index+= len(match.group())
#                 else:
#                     print("no match found on line: ", line_number, substring)
#                     break
#             line_number+=1
#             # clear out the index for the word

        
