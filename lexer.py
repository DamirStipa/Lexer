from collections import Counter
import ply.lex as lex

# List of token names.
tokens = [
 # OPERATORS #
    'PLUS' ,        # +
    'MINUS' ,       # -
    'MULTIPLY',     # *
    'DIVIDE',       # /
    'MODULO',       # %

    'NOT',          # ~
    'EQUALS',       # =

 # COMPARATORS #
    'LT',           # <
    'GT',           # >
    'LTE',          # <=
    'GTE',          # >=
    'DOUBLEEQUAL',  # ==
    'NE',           # !=
    'AND',          # &
    'OR' ,          # |    

  # BRACKETS #
    'LPAREN',       # (
    'RPAREN',       # )
    'LBRACE',       # [
    'RBRACE',       # ]
    'BLOCKSTART',   # {
    'BLOCKEND',     # }
    'WHITESPACE',   # ' ' 

  # DATA TYPES#
    'INTEGER',      # int
    'FLOAT',       # dbl

    'COMMENT',  #--

  #Identifier for reserved words
    'ID'

]

#Regular expressions

t_PLUS    = r'\+'
t_MINUS   = r'-'
t_MULTIPLY   = r'\*'
t_DIVIDE  = r'/'
t_MODULO = r'%'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_LBRACE = r'\['
t_RBRACE = r'\]'
t_BLOCKSTART = r'\{'
t_BLOCKEND = r'\}'
t_NOT = r'\~'
t_EQUALS = r'\='
t_GT = r'\>'
t_LT = r'\<'
t_LTE = r'\<\='
t_GTE = r'\>\='
t_DOUBLEEQUAL = r'\=\='
t_NE = r'\!\='
t_AND = r'\&'
t_OR = r'\|'
t_COMMENT = r'\#.*'           
t_ID = r'[a-zA-Z_][a-zA-Z_0-9]*'

reserved_words = {
    'if' : 'IF',
    'then' : 'THEN',
    'else' : 'ELSE',
    'while' : 'WHILE',
    'for' : 'FOR'
}

tokens = tokens + list(reserved_words.values())

#Rules for INTEGER, WHITESPACE and FLOAT tokens
def t_INTEGER(t):
    r'(?<!\.)\d+(?!\.)(?![0-9])'
    t.value = int(t.value)    
    return t

def t_WHITESPACE(t):
    r'\s+'
    return t

def t_FLOAT(t):
    r'\d+(.\d{1,})'
    t.value = float(t.value)
    return t       

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

#Rules for reserved words
def t_IF(t):
    r'\bif\b'
    t.type = reserved_words.get(t.value, 'IF')
    return t

def t_FOR(t):
    r'\bfor\b'
    t.type = reserved_words.get(t.value, 'FOR')
    return t

def t_ELSE(t):
    r'\belse\b'
    t.type = reserved_words.get(t.value, 'ELSE')
    return t

def t_WHILE(t):
    r'\bwhile\b'
    t.type = reserved_words.get(t.value, 'WHILE')
    return t

#Building the lexer
lexer = lex.lex()

#Testing data
data = '''
[25.5 / (3 * 40) + {300 - 20} -16.5]
a = b + c
{(300 - 250 )<(400 - 500 )}
20 & 30 | 50
if(i > 5 ) while() for() else
'''
split_data = data.split("\n")
split_data.remove("")
split_data.remove("")

# Loop through list containing input lines and tokenize them
line_count=0
identifiers_count=0
identifiers = []
operators_count=0
operators = []
separators_count=0
separators = []
reserved_count=0
reserved = []
constants_count=0
constants = []
comments_count=0
comments = []

for line in split_data:
    print("\nLine " + str(line_count+1) + ":  " + str(line)) #Printing out the line 

    lexer.input(line) #Giving the line to the lexer
    line_count+=1

    output = []
    # Getting tokenized expressions
    for tok in lexer:
        output.append(tok)

    #Iterating over lines
    for item in output:
        item = str(item)
        x = item.split("en(")
        y = x[1].split(",")     
        
        if y[0] == 'BLOCKSTART' or y[0] =='LPAREN' or y[0] =='RPAREN' or y[0] =='LBRACE' or y[0] =='RBRACE' or y[0] =='BLOCKEND' or y[0] == 'WHITESPACE':
            separators_count += 1
            separators.append(y[1].strip("''"))
            print(str(y[1]) + ", separator"  )
        elif y[0] == "PLUS" or y[0] =="MINUS" or y[0] =="MULTIPLY" or y[0] =="DIVIDE" or y[0] =="MODULO" or y[0] =="NOT" or y[0] =="EQUALS" or y[0] =="LT" or y[0] =="LTE" or y[0] =="GT" or y[0] =="GTE" or y[0] =="DOUBLEEQUAL" or y[0] =="NE" or y[0] =="AND" or y[0] =="OR":
            operators_count += 1
            operators.append(y[1].strip("''"))
            print(str(y[1]) + ", operator")
        elif y[0] == "COMMENT":
            comments_count +=1
            comments.append(y[1].strip("''"))
            print(str(y[1]) + ", komentar")
        elif y[0] == "INTEGER" or y[0] =="FLOAT":
            constants_count += 1
            constants.append(y[1].strip("''"))
            print(str(y[1]) + ", konstanta")
        elif y[0] == "IF" or y[0] == "FOR" or y[0] == "ELSE" or y[0] == "WHILE":
            reserved_count += 1
            reserved.append(y[1].strip("''"))
            print(str(y[1]) + ", kljucna rijec")
        elif y[0] == "ID":
            identifiers_count += 1
            identifiers.append(y[1].strip("''"))
            print(str(y[1]) + ", identifikator")


#Formatting output
iden = str(Counter(identifiers)).split("Counter")
oper = str(Counter(operators)).split("Counter")
sepa = str(Counter(separators)).split("Counter")
cons = str(Counter(constants)).split("Counter")
comm = str(Counter(comments)).split("Counter")
res = str(Counter(reserved)).split("Counter")


print("\nIdentifikatori: [" + str(identifiers_count) + "]: " + str(iden[1].strip("(){}")))
print("Kljucne rijeci [" + str(reserved_count) + "] " + str(res[1].strip("(){}")))
print("Separatori: [" + str(separators_count) + "]: " + str(sepa[1].strip("(){}")))
print("Operatori: [" + str(operators_count) + "]: " + str(oper[1].strip("(){}")))
print("Konstante: [" + str(constants_count) + "] " + str(cons[1].strip("(){}")))
print("Komentari: [" + str(comments_count) + "] " + str(comm[1].strip("(){}")) + "\n")