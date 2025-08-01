#!/usr/bin/env python3
import re
import sys


# --- Core Functions ---
# re.compile(pattern)
# compiles a regex pattern for reuse
# best when using the same pattern multiple times, token spec loop

# re.match(pattern, text)
# tries to match from the start of the string
# use when scanning at the current position in the source

# re.search(pattern, text)
# finds first match anywhere in the string
# not really used

# re.findall(pattern, text)
# returns all non-overlapping matches

# re.finditer(pattern, text)
# yields Match objects for all matches
# used with a master pattern to tokenize a loop

# re.fullmatch(pattern,text)
# succeeds only if the whole string matches
# not really needed in a lexer

# --- Match Object Methods ---
# returned by functions like re.match() and re.finditer()

# .group()
# the matched string

# .groups()
# tuple of all captured subgroups

# .start()/.end()
# start/end index of match

# .lastgroup()
# with master pattern: name of the named group that matched

# .span()
# Tuple(start,end) of match position

# --- Advanced Tools ---
# re.Scanner()
# special lexer like engine in re that lets you define 
# pattern-action pairs

# re.VERBOSE 
# lets you write multiline regexs with comments

# Re.IGNORECASE, re.MULTILINE
# flags you can pass to modify regex behavior

def run_lexer(input_file):
    token_spec = [
            ('OPEN_PAREN', r'\('),
            ('CLOSE_PAREN', r'\)'),
            ('SEMICOLON', r';'),
            ('INT', r'int\b'),
            ('MAIN', r'main\b'),
            ('VOID',   r'void\b'),
            ('RETURN', r'return\b'),
            ('CHAR',   r'char\b'),          
            ('CONSTANT', r'[0-9]+\b'),      
            ('OPEN_BRACE', r'\{'),
            ('CLOSE_BRACE', r'\}'),
            ('IF', r'if\b'),
            ('LT', r'<'),
            ('GT', r'>'),
            ('IDENTIFIER', r'[a-zA-Z_]\w*\b'),
            ('SINGLE_COMMENT', r'//.*'),
            ('MULTI_COMMENT', r'/\*[\s\S]*?\*/'),
            ('TILDE', r'~'),
            ('DECREMENT', r'--'),
            ('NEGATION', r'-'),
            ('SHEBANG', r'!'),
            ('ADD', r'\+'),
            ('MULT', r'\*'),
            ('DIV', r'\/'),
            ('REMAINDER', r'\%')
    ]

    with open(input_file) as file:
        code = file.read()
    # print(code)
    
    tokens = []
    pos = 0
    matched = False
    # we loop through the code while pos is less than code
    while pos < len(code):

        matched = False
        # if we see a space move forward a char
        # and we skip to next cycle of loop
        # where we will have advanced the pos and started at the
        # top of the while loop again
        if code[pos].isspace():
            pos+=1
            continue

        # we iter through the list of tokens for each token and
        # its pattern
        for token, pattern in token_spec:
            # a match is checked at the current position onwards
            # when it comes to a word boundry it will stop and check 
            # for a match
            match = re.match(pattern, code[pos:]) 
            if match:
                pattern_match = len(match.group())
                tokens.append((match.group(), token))
                # we want to continue forward in the string
                # so we move forward by each token or pattern length
                pos+=pattern_match
                # when we fall out of the for loop which we will
                # with the break we want to make sure we dont print
                # a lexical error
                matched = True
                break
        if matched == False:
            print(f"lexical error: {code[pos:]}")
            sys.exit(1)
        #pos+=1

    # print(f"tokens: {tokens}")

    # for token, pattern in token_spec:
    #     # print(f"token: {token}, pattern: {pattern}")
    #     regex = re.compile(pattern)
    #     # match = re.matchc()
        


    return tokens
