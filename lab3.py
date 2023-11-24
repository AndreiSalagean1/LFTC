import re

# Define token types
TOKEN_IDENTIFIER = 'IDENTIFIER'
TOKEN_INTCONST = 'INTCONST'
TOKEN_CHARCONST = 'CHARCONST'
TOKEN_STRINGCONST = 'STRINGCONST'
TOKEN_OPERATOR = 'OPERATOR'
TOKEN_SEPARATOR = 'SEPARATOR'
TOKEN_RESERVED_WORD = 'RESERVEDWORD'

# Define a regular expression pattern for matching the different token types
token_patterns = [
    (TOKEN_IDENTIFIER, r'[A-Za-z_][A-Za-z_0-9]*'),
    (TOKEN_INTCONST, r'[+-]?[1-9][0-9]*|0'),
    (TOKEN_CHARCONST, r"'[A-Za-z0-9]+'"),
    (TOKEN_STRINGCONST, r'"[A-Za-z0-9]+"'),
    (TOKEN_OPERATOR, r'[\+\-\*/%:=<><=>=]'),
    (TOKEN_SEPARATOR, r'[\[\]{},:; ]'),
    (TOKEN_RESERVED_WORD, r'VAR|BOOLEAN|CHAR|INTEGER|REAL|ARRAY|OF|PROGRAM|READ|THEN|WHILE|WRITE|ENDIF|ENDWHILE|BEGIN|END')
]

# Create a Symbol Table instance
class SortedST:
    def __init__(self):
        self.table = []
        self.token_count = 0

    def insert(self, key, value):
        existing_entry = self.searchKey(key)
        if existing_entry is not None:
            return existing_entry[0]
        self.token_count += 1
        self.table.append((self.token_count, key, value))
        self.table.sort(key=lambda item: item[1])
        return self.token_count

    def searchKey(self, key):
        for entry in self.table:
            if entry[1] == key:
                return entry
        return None

    def delete(self, key):
        for i, entry in enumerate(self.table):
            if entry[1] == key:
                del self.table[i]
                return

    def size(self):
        return len(self.table)

    def keys(self):
        return [entry[1] for entry in self.table]

# Define a function to tokenize a program
def tokenize_program(program):
    tokens = []
    line_number = 1
    for line in program.split('\n'):
        line_tokens = tokenize_line(line, line_number)
        tokens.extend(line_tokens)
        line_number += 1
    return tokens

# Define a function to tokenize a single line of code
def tokenize_line(line, line_number):
    tokens = []
    position = 0
    while position < len(line):
        match = None
        for token_type, pattern in token_patterns:
            regex = re.compile(pattern)
            match = regex.match(line, position)
            if match:
                value = match.group(0)
                if token_type == TOKEN_IDENTIFIER and value in get_reserved_words():
                    token_type = TOKEN_RESERVED_WORD
                tokens.append((token_type, value, line_number))
                position = match.end()
                break
        if not match:
            # If no match is found, there is a lexical error
            print(f"Lexical error at line {line_number}: '{line[position]}'")
            position += 1
    return tokens

# Define a function to get a list of reserved words
def get_reserved_words():
    return ["VAR", "BOOLEAN", "CHAR", "INTEGER", "REAL","AND" , "ELSE" , "IF" , "ARRAY", "OF", "PROGRAM", "READ", "THEN", "WHILE", "WRITE", "ENDIF", "ENDWHILE", "BEGIN", "END"]

if __name__ == '__main__':
    program = """
    VAR
a: INTEGER;
b:CHAR;
c:REAL;
BEGIN
 READ a;
 READ (b);
 READ #c;
 IF a >= b AND a >= c THEN 
 WRITE a;
 ELSE IF b >= a AND b >= c THEN 
 WRITE b;
 ELSE 
 WRITE c;
 ENDIF;
END
    """

    st = SortedST()
    tokens = tokenize_program(program)

    pif = []

    for token_type, token_value, line_number in tokens:
        if token_type == TOKEN_IDENTIFIER or token_type == TOKEN_INTCONST or token_type == TOKEN_CHARCONST or token_type == TOKEN_STRINGCONST :
            st_pos = st.insert(token_value, line_number)
            pif.append((token_value, st_pos))

    # Output the Symbol Table
    with open("ST.out", "w") as st_out:
        for entry in st.table:
            st_out.write(f"{entry[0]} - {entry[1]} (defined at line {entry[2]})\n")

    # Output the Program Internal Form (PIF)
    with open("PIF.out", "w") as pif_out:
        for token_value, st_pos in pif:
            pif_out.write(f"Token: {token_value}, ST_pos: {st_pos}\n")
