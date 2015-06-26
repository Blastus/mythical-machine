#! /usr/bin/env python3

import re
import sys


def main():
    sc = SimpleCompiler(sys.stdout)
    sc.run(sys.stdin if len(sys.argv) < 2 else sys.argv[1])


class SimpleCompiler:

    OPERATIONS = {'+': 'add', '-': 'sub', '*': 'mul', '/': 'div'}

    def __init__(self, out_file):
        self.__out_file = out_file
        self.__next_label = 1
        self.__variables = set()

    @staticmethod
    def search(pattern, string):
        match = re.search(pattern, string)
        if match:
            return match.start()
        return -1

    @classmethod
    def get_token(cls, program):
        program = program.strip()
        if program:
            if program[0].isalpha():
                p = cls.search('[^0-9A-Za-z]', program)
                if p < 0:
                    return program, ''
                return program[:p], program[p:]
            if program[0].isdigit():
                p = cls.search('[^0-9]', program)
                if p < 0:
                    return program, ''
                return program[:p], program[p:]
            return program[0], program[1:]
        return '', ''

    def get_stat(self, program, register):
        token, remainder = self.get_token(program)
        if token:
            if token == 'while':
                expr, remainder = self.get_expr(remainder, register)
                stat, remainder = self.get_stat(remainder, register + 1)
                code = 'z{0}\n{1}  jz  r{2},z{3}\n{4}  jmp  z{0}\nz{3}\n' \
                    .format(self.__next_label, expr, register,
                            self.__next_label + 1, stat)
                self.__next_label += 2
                return code, remainder
            if token == '{':
                code = ''
                while True:
                    token, other_remainder = self.get_token(remainder)
                    if not token:
                        return '', ''
                    if token == '}':
                        return code, other_remainder
                    stat, remainder = self.get_stat(remainder, register)
                    code += stat
            other_token, other_remainder = self.get_token(remainder)
            if other_token == '=':
                self.__variables.add(token)
                expr, remainder = self.get_expr(other_remainder, register)
                return '{}  sto r{},{}\n'.format(expr, register, token), \
                       remainder
            return self.get_expr(program, register)
        return '', ''

    @classmethod
    def get_expr(cls, program, register):
        term, remainder = cls.get_term(program, register)
        if term:
            token, other_remainder = cls.get_token(remainder)
            if token in cls.OPERATIONS:
                expr, remainder = cls.get_expr(other_remainder, register + 1)
                word = cls.OPERATIONS[token]
                code = '  {} r{},r{}\n'.format(word, register, register + 1)
                return term + expr + code, remainder
            return term, remainder
        return '', ''

    @classmethod
    def get_term(cls, program, register):
        token, remainder = cls.get_token(program)
        if token:
            if token == '(':
                expr, remainder = cls.get_expr(remainder, register)
                if expr:
                    token, remainder = cls.get_token(remainder)
                    if token == ')':
                        return expr, remainder
                return '', ''
            if token < 'A':
                return '  ld# r{},{}\n'.format(register, token), remainder
            return '  ld r{},{}\n'.format(register, token), remainder
        return '', ''

    def run(self, program):
        remainder = program if isinstance(program, str) else program.read()
        while remainder:
            stat, remainder = self.get_stat(remainder, 0)
            self.__out_file.write(stat)
        self.__out_file.write('  hlt\n')
        for var in sorted(self.__variables):
            sys.stdout.write(var + ' 0\n')
        self.__out_file.flush()

if __name__ == '__main__':
    main()
