import string
import random

class PasswordGenerator:
    def __init__(self):
        pass
    def generate(self, min=8, max=64, alpha=True, numeric=True, symbols=True, uppercase=True, lowercase=True):
        chars = ''
        if alpha:
            if lowercase:
                chars += string.ascii_lowercase
            if uppercase:
                chars += string.ascii_uppercase
        chars += (string.digits if numeric else '')
        chars += (string.punctuation if symbols else '')
        if len(chars) < 1:
            return 'No password for you'
        len_pass = random.randint(min, max)
        password = ''.join([random.choice(chars) for i in range(len_pass)])
        return password
    def difficulty(self, password):
        status = 0
        levels = ('No rank', 'Weak','Normal','Good', 'Better', 'Excellent')
        if len(password) >= 8:
            status+=1
        for i in string.ascii_lowercase:
            if password.find(i) != -1:
                status += 1
                break
        for i in string.ascii_uppercase:
            if password.find(i) != -1:
                status += 1
                break
        for i in string.digits:
            if password.find(i) != -1:
                status += 1
                break
        for i in string.punctuation:
            if password.find(i) != -1:
                status += 1
                break
        
        return levels[status]

pass_gen = PasswordGenerator()
print(pass_gen.generate(numeric=False))
print(pass_gen.difficulty('alakio12345'))