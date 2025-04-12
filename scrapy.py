import re

# the 'r' is used for raw string so that we dont escape any characters
# lex_dict = {
#     'identifier' : re.compile(r'[a-zA-Z_]\w*\b'),
#     'constant' : re.compile(r'[0-9]+\b'),
#     'int_keyword' : re.compile(r'int\b'),
#     'void_keyword' : re.compile(r'void\b'),
#     'return_keyword' : re.compile(r'return\b'),
#     'char_keyword' : re.compile(r'char\b'),
#     'open_paren' : re.compile(r'\('),
#     'close_paren' : re.compile(r'\)'),
#     'open_brace' : re.compile(r'{'),
#     'close_brace' : re.compile(r'}'),
#     'semicolon' : re.compile(r';')
# }
# reserved_keywords = [
#      'int',
#      'void',
#      'return',
#      'char',
# ]
                        
# with open("return_2.c", "r") as file:
#         print("\n--- second shot ---\n")
#         for line in file:
#              # for key, value in the dict
#              for token, pattern in lex_dict.items():
#                   # for each match of the pattern in the line
#                   for match in pattern.finditer(line):
#                        if token == 'identifier' and match.group() in reserved_keywords:
#                             # print("keyword:", match.group())
#                             pass
#                        else:
#                             print(match.group())

# make a list instead of dict
# here the order matters, reserver words need to be before 
# identifier so that they match when we compile the pattern
token_specification = [
    ('INT',    r'int\b'),
    ('VOID',   r'void\b'),
    ('RETURN', r'return\b'),
    ('CHAR',   r'char\b'),
    ('IDENTIFIER', r'[a-zA-Z_]\w*\b'),
    ('CONSTANT', r'[0-9]+\b'),
    ('OPEN_PAREN', r'\('),
    ('CLOSE_PAREN', r'\)'),
    ('OPEN_BRACE', r'\{'),
    ('CLOSE_BRACE', r'\}'),
    ('SEMICOLON', r';'),
]

tokens = [
      'INT',
      'VOID',
      'RETURN',
      'CHAR',
      'IDENTIFIER',
      'CONSTANT',
      'OPEN_PAREN',
      'CLOSE_PAREN',
      'OPEN_BRACE',
      'CLOSE_BRACE',
      'SEMICOLON'
]
#  we are going to build a master pattern
pattern_parts = []
# stick or between each pattern
for token, pattern in token_specification:
      part = f'(?P<{token}>{pattern})'
      pattern_parts.append(part)
# print(pattern_parts)
combined_pattern = '|'.join(pattern_parts)
# print("combined parts:\n",combined_pattern)
master_pattern = re.compile(combined_pattern)

with open("return_2.c", "r") as file:
        print("\n--- third shot ---\n")
        for token in file:
              # in each line we find the last item that was matched
              for match in master_pattern.finditer(token):
                    token_type = match.lastgroup
                    token_value = match.group()
                    print(token_type, token_value)

with open("return_2.c", "r") as file:
      print("\n--- fourth shot ---\n")
      carriage_returns = 0
      # python automatically reads a file line by line
      for line in file:
            if line.endswith('\n'):
                  carriage_returns = carriage_returns + 1

print("number of carriage returns: ", carriage_returns)          

with open("return_2.c", "r") as file:
      print("\n--- fifth shot ---\n")
      line_index = 0
      # python automatically reads a file line by line
      for line in file:
            while line_index < len(line):
                  newline = line.split()
                  line_index+=1
            print(line_index)
            print(len(newline), newline)
            line_index = 0

with open("return_2.c", "r") as file:
      print("\n--- sixth shot ---\n")
      arr_index = 0
      for line in file:
            newline = line.split()
            for token in newline:
                  for match in master_pattern.finditer(token):
                        token_type = match.lastgroup
                        token_value = match.group()
                        if token_type not in tokens:
                              print("--- error token not found ---")
                        print(token_type, token_value)
                        
            print(len(newline), newline)
print("\n")

with open("return_2.c", "r") as file:
      print("\n--- seventh shot ---\n")
      arr_index = 0
      for line in file:
            newline = line.split()
            for token in newline:
                  match = master_pattern.match(token)
                  if match is not None:
                        token_type = match.lastgroup
                        token_value = match.group()
                        print(token_type, token_value)
                  else:
                        print("--- error token not found ---", token)

with open("return_2.c", "r") as file:
      print("\n--- 9th shot ---\n")
      index = 0
      newline = ''
      for line in file:
            while index < len(line):
                  newline += line[index]
                  if line[index] == ' ':
                        print(newline[:index])
                  index+=1
            print(newline)
            index = 0
            newline = ''

# with open("return_2.c", "r") as file:
#       print("\n--- 10th shot ---\n")
#       index = 0
#       for line in file:
#         while index < len(line):
#             if line[index] == " ":
#                 index+=1
#             token = line[:index]
#             print(token)
#             if line[token] == " ":
                
#             # match = master_pattern.match(token)
#             # if match is not None:
#             #       print(match.lastgroup, match.group())
#             # print(line[index], end="")
#             index+=1
#         # token = ''
#         index = 0

with open("return_2.c", "r") as file:
      
    print("\n--- 11th shot ---\n")
    index = 0
    for line in file:
        while index < len(line):
            while index < len(line) and line[index] in " \t\n":
                  index+= 1
            if index >= len(line):
                  break
            substring = line[index:]
            print("index: ",index)
            print("sub string:", substring)
            match = master_pattern.match(substring)
            if match is not None:
                print(match.lastgroup, match.group())
                index += len(match.group())
            else:
                  print("no match found")
                  break


        index = 0          

with open("return_2.c", "r") as file:
    print("\n--- 12th shot ---\n")
    index = 0
    for line in file:
        while index < len(line):
            while index < len(line) and line[index] in " \t\n":
                index+=1
            if index >= len(line):
                break
            substring = line[index:]
            match = master_pattern.match(substring)
            if match is not None:
                print(match.lastgroup, match.group())
                index+= len(match.group())
            else:
                print("no match found")
                break
        index = 0


        