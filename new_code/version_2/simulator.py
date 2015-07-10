#! /usr/bin/env python3
__author__ = 'Stephen "Zero" Chappell <Noctis.Skytower@gmail.com>'

import ast
import math
import struct
import sys

FLOAT = struct.Struct('>d')
INTEGER = struct.Struct('>Q')


def main():
    ports = StandardInput(), StandardOutput(), StandardError()
    mm = MagicalMachine(ports)
    mm.run('program2.m2l')


def float_to_int(obj):
    return INTEGER.unpack(FLOAT.pack(obj))[0]


def int_to_float(obj):
    return FLOAT.unpack(INTEGER.pack(obj))[0]

###############################################################################


class MagicalMachine:

    A_TEMPLATE = ('{:X}',
                  'MEM[{:X}]',
                  'REG[{:X}]',
                  'MEM[MEM[{:X}]]',
                  'MEM[REG[{:X}]]',
                  'REG[MEM[{:X}]]',
                  'REG[REG[{:X}]]',
                  'PORT[{:X}]',
                  'PORT[MEM[{:X}]]',
                  'PORT[REG[{:X}]]',
                  'PORT[MEM[MEM[{:X}]]]',
                  'PORT[MEM[REG[{:X}]]]',
                  'PORT[REG[MEM[{:X}]]]',
                  'PORT[REG[REG[{:X}]]]')

    C_FUNCTION = ('{} < {}',
                  '{} <= {}',
                  '{} == {}',
                  '{} != {}',
                  '{} > {}',
                  '{} >= {}',
                  '{} + {}',
                  '{} - {}',
                  '{} * {}',
                  '{} / {}',
                  '{} // {}',
                  '{} % {}',
                  '{} ** {}',
                  '{} << {}',
                  '{} >> {}',
                  '{} & {}',
                  '{} ^ {}',
                  '{} | {}',
                  '{} OR {}',
                  '{} AND {}',
                  'MEM[{} + {}]',
                  'REG[{} + {}]')

    def __init__(self, ports):
        self.__ports = ports
        self.__mem = MemoryCells(20, 84)
        self.__reg = MemoryCells(20, 84)
        self.__next = 0

    def cycle(self):
        code = self.__mem[self.__next]
        if isinstance(code, float):
            code = float_to_int(code)
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
        self.__explain(op, a1, b1, cc, a2, b2, a3, b3)
        if op == 0:
            return False
        self.__next += 1
        if op == 1:
            self.__set(a1, b1, self.__exe(cc, self.__get(
                a2, b2), self.__get(a3, b3)))
            return True
        if op == 2:
            self.__next = self.__get(a1, b1) if self.__exe(cc, self.__get(
                a2, b2), 0) else self.__get(a3, b3)
            return True
        raise ValueError('instruction could not be understood')

    def __explain(self, op, a1, b1, cc, a2, b2, a3, b3):
        if op == 0:
            print('{:05X}   halt'.format(self.__next))
        elif op == 1:
            print('{:05X}   {} = {}'.format(
                self.__next,
                self.A_TEMPLATE[a1].format(b1),
                self.C_FUNCTION[cc].format(
                    self.A_TEMPLATE[a2].format(b2),
                    self.A_TEMPLATE[a3].format(b3))))
        elif op == 2:
            print('{:05X}   goto {} if {} else {}'.format(
                self.__next,
                self.A_TEMPLATE[a1].format(b1),
                self.C_FUNCTION[cc].format(
                    self.A_TEMPLATE[a2].format(b2), 0),
                self.A_TEMPLATE[a3].format(b3)))

    def __get(self, a, b):
        if a == 0x0:
            return b
        elif a == 0x1:
            return self.__mem[b]
        elif a == 0x2:
            return self.__reg[b]
        elif a == 0x3:
            return self.__mem[self.__mem[b]]
        elif a == 0x4:
            return self.__mem[self.__reg[b]]
        elif a == 0x5:
            return self.__reg[self.__mem[b]]
        elif a == 0x6:
            return self.__reg[self.__reg[b]]
        elif a == 0x7:
            return self.__ports[b].in_()
        elif a == 0x8:
            return self.__ports[self.__mem[b]].in_()
        elif a == 0x9:
            return self.__ports[self.__reg[b]].in_()
        elif a == 0xA:
            return self.__ports[self.__mem[self.__mem[b]]].in_()
        elif a == 0xB:
            return self.__ports[self.__mem[self.__reg[b]]].in_()
        elif a == 0xC:
            return self.__ports[self.__reg[self.__mem[b]]].in_()
        elif a == 0xD:
            return self.__ports[self.__reg[self.__reg[b]]].in_()
        else:
            raise ValueError('could not understand operand type')

    def __exe(self, c, x, y):
        if c == 0x00:
            return x < y
        elif c == 0x01:
            return x <= y
        elif c == 0x02:
            return x == y
        elif c == 0x03:
            return x != y
        elif c == 0x04:
            return x > y
        elif c == 0x05:
            return x >= y
        elif c == 0x06:
            return x + y
        elif c == 0x07:
            return x - y
        elif c == 0x08:
            return x * y
        elif c == 0x09:
            return x / y
        elif c == 0x0A:
            return x // y
        elif c == 0x0B:
            return x % y
        elif c == 0x0C:
            return x ** y
        elif c == 0x0D:
            return x << y
        elif c == 0x0E:
            return x >> y
        elif c == 0x0F:
            return x & y
        elif c == 0x10:
            return x ^ y
        elif c == 0x11:
            return x | y
        elif c == 0x12:
            return x or y
        elif c == 0x13:
            return x and y
        elif c == 0x14:
            return self.__mem[x + y]
        elif c == 0x15:
            return self.__reg[x + y]
        else:
            raise ValueError('could not understand operation type')

    def __set(self, a, b, c):
        if a == 0x0:
            raise ValueError('immediate value may not be set')
        elif a == 0x1:
            self.__mem[b] = c
        elif a == 0x2:
            self.__reg[b] = c
        elif a == 0x3:
            self.__mem[self.__mem[b]] = c
        elif a == 0x4:
            self.__mem[self.__reg[b]] = c
        elif a == 0x5:
            self.__reg[self.__mem[b]] = c
        elif a == 0x6:
            self.__reg[self.__reg[b]] = c
        elif a == 0x7:
            self.__ports[b].out(c)
        elif a == 0x8:
            self.__ports[self.__mem[b]].out(c)
        elif a == 0x9:
            self.__ports[self.__reg[b]].out(c)
        elif a == 0xA:
            self.__ports[self.__mem[self.__mem[b]]].out(c)
        elif a == 0xB:
            self.__ports[self.__mem[self.__reg[b]]].out(c)
        elif a == 0xC:
            self.__ports[self.__reg[self.__mem[b]]].out(c)
        elif a == 0xD:
            self.__ports[self.__reg[self.__reg[b]]].out(c)
        else:
            raise ValueError('could not understand operand type')

    def load(self, name):
        with open(name) as file:
            for line in file:
                if line[0] != '#':
                    fields = line.split(' ')
                    try:
                        address = int(fields[0], 16)
                    except (IndexError, ValueError):
                        pass
                    else:
                        try:
                            instruction = int(fields[1], 16)
                        except ValueError:
                            tail_end = ' '.join(fields[1:])
                            try:
                                literal = ast.literal_eval(tail_end)
                            except SyntaxError:
                                pass
                            else:
                                if isinstance(literal, str):
                                    self.__mem[address] = len(literal)
                                    iterator = enumerate(literal, address + 1)
                                    for position, character in iterator:
                                        self.__mem[position] = ord(character)
                        except IndexError:
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
        sys.stderr.write(value)

if __name__ == '__main__':
    main()
