import random
import string

class CodeGenerator:
    def __init__(self):
        self.current_length = 2 
        self.round_counter = 0  

    def generate_code(self) -> str:
        
        if self.round_counter % 4 == 0:
            self.current_length += 1
        
        self.round_counter += 1
            
        chars = string.ascii_uppercase + string.digits
        return ''.join(random.choices(chars, k=self.current_length))

    def generate_answers(self, code: str) -> list[str]:

        #num_options = 2 + self.round_counter % 4 if self.round_counter % 4 else 6
        num_options = random.randint(3, 5)  
        options = set()
        options.add(code) 
        
        while len(options) < num_options:
            fake_code = list(code)
            idx = random.randint(0, len(code) - 1)
            char_pool = string.ascii_uppercase + string.digits
            fake_code[idx] = random.choice(char_pool)
            options.add("".join(fake_code))
            
        options_list = list(options)
        random.shuffle(options_list)
        return options_list