#! /usr/bin/env python3
__author__ = 'Stephen "Zero" Chappell <Noctis.Skytower@gmail.com>'

import math
import struct
import sys

FLOAT = struct.Struct('>d')
INTEGER = struct.Struct('>Q')


def main():
    ports = StandardInput(), StandardOutput(), StandardError()
    mm = MagicalMachine(ports)
    mm.run('program1.m2l')


def float_to_int(obj):
    return INTEGER.unpack(FLOAT.pack(obj))[0]


def int_to_float(obj):
    return FLOAT.unpack(INTEGER.pack(obj))[0]

###############################################################################


class MagicalMachine:

    def __init__(self, ports):
        self.__ports = ports
        self.__mem = MemoryCells(20, 84)
        self.__reg = MemoryCells(20, 84)
        self.__next = 0

    def cycle(self):
        code = self.__mem[self.__next]
        if isinstance(code, float):
            code = float_to_int(code)
        self.__next += 1
        code, b3 = divmod(abs(code), 1 << 20)
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
                a2, b2), 0) else self.__get(a3, b3)
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
            return self.__ports[b].in_()
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
            self.__ports[b].out(c)
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
                    except (IndexError, ValueError):
                        pass
                    else:
                        self.__mem[address] = instruction

    def run(self, name):
        self.load(name)
        self.__next = 1 << 10
        while self.cycle():
            pass

###############################################################################


class MemoryCells:

    def __init__(self, address_bus_width, data_bus_width):
        total_cells = 1 << address_bus_width
        self.__cells = [0] * total_cells
        self.__address_bus_mask = total_cells - 1
        self.__data_bus_mask = (1 << data_bus_width) - 1

    def __getitem__(self, key):
        return self.__cells[self.__scrub_key(key)]

    def __scrub_key(self, key):
        if isinstance(key, float):
            key = float_to_int(key)
        return abs(key) & self.__address_bus_mask

    def __setitem__(self, key, value):
        self.__cells[self.__scrub_key(key)] = self.__scrub_value(value)

    def __scrub_value(self, value):
        if isinstance(value, float):
            # float sign bits are included on the data bus size
            return int_to_float(float_to_int(value) & self.__data_bus_mask)
        # integer sign bits are exclude on the data bus size
        if value < 0:
            return -(-value & self.__data_bus_mask)
        return value & self.__data_bus_mask

###############################################################################


class Port:

    def in_(self):
        raise NotImplementedError()

    def out(self, value):
        raise NotImplementedError()

###############################################################################


class BinaryPort(Port):

    def in_(self):
        return int.from_bytes(self._exe_in(), 'big')

    def _exe_in(self):
        raise NotImplementedError()

    def out(self, value):
        value = float_to_int(value) if isinstance(value, float) else abs(value)
        value = value.to_bytes(math.ceil(value.bit_length() / 8), 'big')
        self._exe_out(value)

    def _exe_out(self, value):
        raise NotImplementedError()

###############################################################################


class StringPort(Port):

    def __init__(self, encoding='utf-8', errors='strict'):
        self.__encoding, self.__errors = encoding, errors

    def in_(self):
        return int.from_bytes(self._exe_in().encode(
            self.__encoding, self.__errors), 'big')

    def _exe_in(self):
        raise NotImplementedError()

    def out(self, value):
        value = float_to_int(value) if isinstance(value, float) else abs(value)
        value = value.to_bytes(math.ceil(value.bit_length() / 8), 'big')
        self._exe_out(value.decode(self.__encoding, self.__errors))

    def _exe_out(self, value):
        raise NotImplementedError()

###############################################################################


class StandardInput(StringPort):

    def _exe_in(self):
        return sys.stdin.read(1)

    def _exe_out(self, value):
        pass


class StandardOutput(StringPort):

    def _exe_in(self):
        pass

    def _exe_out(self, value):
        sys.stdout.write(value)


class StandardError(StringPort):

    def _exe_in(self):
        pass

    def _exe_out(self, value):
        sys.stdout.write(value)

if __name__ == '__main__':
    main()