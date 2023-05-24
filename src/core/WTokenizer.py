class WTokenizer():
    KEYWORDS = ["skip", "if", "while", "fi", "do", "then", "else", ":=", ">", ";", "od", "+", "-", "*", "=", "¬", "∧", "∨"]
    
    def __init__(self):
        pass

    def tokenize(self, code):
        code = code.strip()
        
        code = code.replace("\n", " ")
        for _ in range(10):
            code = code.replace("  ", " ")
        code = code.strip()
        code = code.lower()
        
        
        tokens = []
        EXTENSION = 10
        code = list(code + " " * EXTENSION)


        i = -1
        for _ in range(10000):
            i += 1
            if i > len(code) - EXTENSION:
                break
            
            cont = False
            for keyword in self.KEYWORDS:
                if "".join(code[i:i+len(keyword)]) == keyword:
                    tokens.append(keyword)
                    i += len(keyword) - 1
                    cont = True
                    break
            if cont:
                continue
            
            if code[i] == " ":
                continue
            
            word = ""
            for j in range(1000):
                char = code[i+j]
                if char in [" ", ";", ">", "=", ":", "+", "-", "*", "¬", "∧", "∨"]:
                    break
                word += char
            i += j
            tokens.append(word)

        return tokens