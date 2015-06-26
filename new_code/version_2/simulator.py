#! /usr/bin/env python3
__author__ = 'Stephen "Zero" Chappell <Noctis.Skytower@gmail.com>'


class MagicMachine:

    def __init__(self, ports):
        self.__ports = ports
        self.__mem = [0] * (1 << 20)
        self.__reg = [0] * (1 << 20)
        self.__code = 0
        self.__next = 0

    def cycle(self):
        self.__code = self.__mem[self.__next]
        self.__next += 1
        code, b3 = divmod(self.__code, 1 << 20)
        code, a3 = divmod(code, 1 << 4)
        code, b2 = divmod(code, 1 << 20)
        code, a2 = divmod(code, 1 << 4)
        code, cc = divmod(code, 1 << 8)
        code, b1 = divmod(code, 1 << 20)
        code, a1 = divmod(code, 1 << 4)
        code, op = divmod(code, 1 << 4)
        if code:
            raise ValueError('instruction is too large')
        if op == 0:
            return False
        if op == 1:
            self.__set(a1, b1, self.__exe(cc, self.__get(
                a2, b2), self.__get(a3, b3)))
            return True
        if op == 2:
            self.__next = self.__get(a1, b1) if self.__exe(cc, self.__get(
                a2, b2), 0) else self.__next = self.__get(a3, b3)
            return True
        raise ValueError('instruction could not be understood')

    def __get(self, a, b):
        if a == 0:
            return b
        elif a == 1:
            return self.__mem[b]
        elif a == 2:
            return self.__reg[b]
        elif a == 3:
            return self.__mem[self.__mem[b]]
        elif a == 4:
            return self.__mem[self.__reg[b]]
        elif a == 5:
            return self.__reg[self.__mem[b]]
        elif a == 6:
            return self.__reg[self.__reg[b]]
        elif a == 7:
            return self.__mem[self.__mem[self.__mem[b]]]
        elif a == 8:
            return self.__mem[self.__mem[self.__reg[b]]]
        elif a == 9:
            return self.__mem[self.__reg[self.__mem[b]]]
        elif a == 10:
            return self.__mem[self.__reg[self.__reg[b]]]
        elif a == 11:
            return self.__reg[self.__mem[self.__mem[b]]]
        elif a == 12:
            return self.__reg[self.__mem[self.__reg[b]]]
        elif a == 13:
            return self.__reg[self.__reg[self.__mem[b]]]
        elif a == 14:
            return self.__reg[self.__reg[self.__reg[b]]]
        elif a == 15:
            return self.__ports[b].get_in()
        else:
            raise ValueError('could not understand operand type')

    @staticmethod
    def __exe(c, x, y):
        if c == 0:
            return x < y
        elif c == 1:
            return x <= y
        elif c == 2:
            return x == y
        elif c == 3:
            return x != y
        elif c == 4:
            return x > y
        elif c == 5:
            return x >= y
        elif c == 6:
            return x + y
        elif c == 7:
            return x - y
        elif c == 8:
            return x * y
        elif c == 9:
            return x / y
        elif c == 10:
            return x // y
        elif c == 11:
            return x % y
        elif c == 12:
            return x ** y
        elif c == 13:
            return x << y
        elif c == 14:
            return x >> y
        elif c == 15:
            return x & y
        elif c == 16:
            return x ^ y
        elif c == 17:
            return x | y
        else:
            raise ValueError('could not understand operation type')

    def __set(self, a, b, c):
        if a == 0:
            raise ValueError('immediate value may not be set')
        elif a == 1:
            self.__mem[b] = c
        elif a == 2:
            self.__reg[b] = c
        elif a == 3:
            self.__mem[self.__mem[b]] = c
        elif a == 4:
            self.__mem[self.__reg[b]] = c
        elif a == 5:
            self.__reg[self.__mem[b]] = c
        elif a == 6:
            self.__reg[self.__reg[b]] = c
        elif a == 7:
            self.__mem[self.__mem[self.__mem[b]]] = c
        elif a == 8:
            self.__mem[self.__mem[self.__reg[b]]] = c
        elif a == 9:
            self.__mem[self.__reg[self.__mem[b]]] = c
        elif a == 10:
            self.__mem[self.__reg[self.__reg[b]]] = c
        elif a == 11:
            self.__reg[self.__mem[self.__mem[b]]] = c
        elif a == 12:
            self.__reg[self.__mem[self.__reg[b]]] = c
        elif a == 13:
            self.__reg[self.__reg[self.__mem[b]]] = c
        elif a == 14:
            self.__reg[self.__reg[self.__reg[b]]] = c
        elif a == 15:
            self.__ports[b].set_out(c)
        else:
            raise ValueError('could not understand operand type')

    def load(self, name):
        with open(name) as file:
            for line in file:
                if line[0] != '#':
                    fields = line.split()
                    try:
                        address = int(fields[0], 16)
                        instruction = int(fields[1], 16)
                        self.__mem[address] = instruction
                    except (IndexError, ValueError):
                        pass
