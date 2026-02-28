#!/usr/bin/env python
import sys
class Assembler(object):
    def __init__(self, parser, symbol_table, analysis):
        self.parser = parser
        self.symbol_table = symbol_table
        self.analysis = analysis

    def assemble(self, asm_file):
        self.prepare_files(asm_file)
        par = self.parser

        while par.more_commands:
            par.advance()
            if par.command_type == 'L_COMMAND':
                self.write_L(par.symbol)
        self.ram_add = 16
        par.reset_file()
        while par.more_commands:
            par.advance()
            if par.command_type == 'A_COMMAND':
                self.write_A(par.symbol)
            elif par.command_type == 'C_COMMAND':
                self.write_C(par.dest, par.comp, par.jump)
        par.close_asm()
        self.hack.close()

    def prepare_files(self, asm_file):
        assert '.asm' in asm_file, 'False!'
        self.parser.load_file(asm_file)
        hack_file = asm_file.replace('.asm', '.hack')
        self.hack = open(hack_file, 'w')
    def write(self, instruction):
        self.hack.write(instruction+'\n')
    def create_add(self, symbol):
        address = '{0:b}'.format(int(symbol))
        base = (15 - len(address)) * '0'
        return base + address

    def write_A(self, symbol):
        instruction = '0'
        try:
            int(symbol)
        except ValueError:
            if not self.symbol_table.contains(symbol): 
                address = self.create_add(self.ram_add)
                self.symbol_table.add_entry(symbol, address)
                self.ram_add += 1
            instruction += self.symbol_table.get_add(symbol)
        else:
            instruction += self.create_add(symbol)
        self.write(instruction)

    def write_L(self, symbol):
        address = self.create_add(self.parser.instruction_num+1)
        self.symbol_table.add_entry(symbol, address)

    def write_C(self, dest, comp, jump):
        inst = '111'
        inst += self.analysis.comp(comp)
        inst += self.analysis.dest(dest)
        inst += self.analysis.jump(jump)
        self.write(inst)
class SymbolTable(object):
    def __init__(self):
        self.symbol_dict = self.table()
        self.ram_position = 16 # 0-15 have preset values

    def get_add(self, symbol):
        return self.symbol_dict[symbol]

    def contains(self, symbol):
        return symbol in self.symbol_dict

    def add_entry(self, symbol, address):
        self.symbol_dict[symbol] = address

    def table(self): # 15 bit addresses, 32K locations
        return {
             'SP': '000000000000000',
            'LCL': '000000000000001',
            'ARG': '000000000000010',
           'THIS': '000000000000011',
           'THAT': '000000000000100',
             'R0': '000000000000000',
             'R1': '000000000000001',
             'R2': '000000000000010',
             'R3': '000000000000011',
             'R4': '000000000000100',
             'R5': '000000000000101',
             'R6': '000000000000110',
             'R7': '000000000000111',
             'R8': '000000000001000',
             'R9': '000000000001001',
            'R10': '000000000001010',
            'R11': '000000000001011',
            'R12': '000000000001100',
            'R13': '000000000001101',
            'R14': '000000000001110',
            'R15': '000000000001111',
         'SCREEN': '100000000000000',
            'KBD': '110000000000000',
        }

class Parser(object):
    def load_file(self, asm_filename):
        self.asm = open(asm_filename, 'r')
        self.reset_file()
        self.symbol = None
        self.dest = None
        self.comp = None
        self.jump = None
        self.command_type = None

    def reset_file(self):
        self.asm.seek(0)
        line = self.asm.readline().strip()
        while self.is_not_instruction(line):
            line = self.asm.readline().strip()
        self.curr_instruction = line
        self.instruction_num = -1 

    def close_asm(self):
        self.asm.close()

    def is_not_instruction(self, line):
        return not line or line[:2] == '//'

    @property
    def more_commands(self):
        return bool(self.curr_instruction)

    def get_next_instruction(self):
        line = self.asm.readline().strip()
        line = line.split('//')[0]
        line = line.strip()
        self.curr_instruction = line

    def advance(self):
        ci = self.curr_instruction
        if ci[0] == '@':
            self.parse_A(ci)
            self.instruction_num += 1
        elif ci[0] == '(':
            self.parse_L(ci)
        else:
            self.parse_C(ci)
            self.instruction_num += 1
        self.get_next_instruction()

    def parse_A(self, instruction):
        self.symbol = instruction[1:]
        self.command_type = 'A_COMMAND'

    def parse_L(self, instruction):
        self.symbol = instruction[1:-1]
        self.command_type = 'L_COMMAND'

    def parse_C(self, instruction):
        '''C instruction format: dest=comp;jump
        '''
        self.dest, self.comp, self.jump = None, None, None
        parts = instruction.split(';')
        remainder = parts[0]
        if len(parts) == 2:
            self.jump = parts[1]
        parts = remainder.split('=')
        if len(parts) == 2:
            self.dest = parts[0]
            self.comp = parts[1]
        else:
            self.comp = parts[0]
        self.command_type = 'C_COMMAND'


class Analysis(object):

    def comp(self, value):
        comp_dict = {
              '0': '101010',
              '1': '111111',
             '-1': '111010',
              'D': '001100',
              'A': '110000',
             '!D': '001101',
             '!A': '110001',
             '-D': '001111',
             '-A': '110011',
            'D+1': '011111',
            'A+1': '110111',
            'D-1': '001110',
            'A-1': '110010',
            'D+A': '000010',
            'D-A': '010011',
            'A-D': '000111',
            'D&A': '000000',
            'D|A': '010101',
        }
        a = '0'
        if 'M' in value:
            a = '1'
            value = value.replace('M', 'A')
        c = comp_dict.get(value, '000000')
        return a + c
    
    def dest(self, value):
        list1 = ['0', '0', '0']
        if value is None:
            return ''.join(list1)
        if 'A' in value:
            list1[0] = '1'
        if 'D' in value:
            list1[1] = '1'
        if 'M' in value:
            list1[2] = '1'
        return ''.join(list1)

    def jump(self, value):
        jump_dict = {
            'JGT': '001',
            'JEQ': '010',
            'JGE': '011',
            'JLT': '100',
            'JNE': '101',
            'JLE': '110',
            'JMP': '111',
        }
        return jump_dict.get(value, '000')




if __name__ == '__main__':
    asm_filename = sys.argv[1]
    assembler = Assembler(Parser(), SymbolTable(), Analysis())
    assembler.assemble(asm_filename)