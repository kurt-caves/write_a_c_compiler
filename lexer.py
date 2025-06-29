# https://joshsharp.com.au/blog/rpython-rply-interpreter-1.html

from rply import LexerGenerator

lg = LexerGenerator()
# '\b' is a word boundary anchor
# r'char\b' will only match 'char'
# characters that must be escaped:  
    # . ^ $ * + ? { } [ ] \ | ( )
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
lg.add('IF', r'if\b')
lg.add('LT', r'<')
lg.add('GT', r'>')
lg.add('PLUS', r'\+')
lg.ignore(r'\s+')
# match exactly one character except newline
# when the lexer sees a character that did not fit my other
# tokens it will be an error token
lg.add('ERROR', r'.')
lexer = lg.build()

def run_lexer(input_file):
    with open(input_file,"r") as file:
        # .read() reads all the text from an open file and :makes
        # a string out of it
        code = file.read()
    
    # other attributes of the token object:
        # .name -> token type name 
        # .value -> actual text matched
        # .source_pos -> line/column info
        # .getsourcepos() -> 
            # lineno -> line number
            # colno -> column number
    tokens = []
    # Run the lexer
    for token in lexer.lex(code):
        if token.name == 'ERROR':
            pos = token.getsourcepos()
            raise SyntaxError(
                    f"Illegal character '{token.value}' at line {pos.lineno}, column {pos.colno}"
                    )
        # print(f"token name: {token.name}, token value: {token.value}")
        tokens.append(token)

    return tokens
        
        



