#! /usr/bin/env python3

import pathlib
import sys


def main():
    ap = AssemblerProgram(sys.stdout)
    ap.run(sys.stdin)


class AssemblerProgram:

    CODES = {'hlt': 0, 'ld': 1, 'sto': 2, 'ld#': 3, 'ldi': 4, 'add': 5,
             'sub': 6, 'mul': 7, 'div': 8, 'jmp': 10, 'jz': 11}

    def __init__(self, out_file):
        self.__out_file = out_file
        self.__lookup = {'r0': 0, 'r1': 1, 'r2': 2, 'r3': 3, 'r4': 4, 'r5': 5,
                         'r6': 6, 'r7': 7, 'r8': 8, 'r9': 9}

    def get_value(self, s):
        if s:
            a = self.__lookup.get(s)
            return int(s) if a is None else a
        return 0

    def pass_one(self, program):
        p_reg = 100
        for line in program:
            fields = line.split()
            if fields:
                if line[0] <= ' ':
                    p_reg += 1
                else:
                    self.__lookup[fields[0]] = p_reg
                    if len(fields) > 1:
                        p_reg += 1

    def assemble(self, fields):
        op_value = self.CODES.get(fields[0])
        if op_value is not None:
            if op_value != 0:
                parts = fields[1].split(',')
                if len(parts) == 1:
                    parts = 0, parts[0]
                return (op_value * 10000 +
                        self.get_value(parts[0]) * 1000 +
                        self.get_value(parts[1]))
            return 0
        return int(fields[0])

    def pass_two(self, program):
        p_reg = 100
        for line in program:
            fields = line.split()
            if line[0] > ' ':
                fields = fields[1:]
            if fields:
                try:
                    instruction = self.assemble(fields)
                    self.__out_file.write('{:03} {:06}   {}'
                                          .format(p_reg, instruction, line))
                    p_reg += 1
                except ValueError:
                    self.__out_file.write('*** ******   ' + line)
            else:
                self.__out_file.write(' ' * 13 + line)

    def run(self, in_file):
        program = in_file.readlines()
        program = self.patch_program(program)
        self.pass_one(program)
        self.pass_two(program)

    @staticmethod
    def patch_program(program):
        if len(program) == 1:
            path = pathlib.Path(program[0].strip())
            if path.is_file():
                return path.open().readlines()
        return program

if __name__ == '__main__':
    main()
