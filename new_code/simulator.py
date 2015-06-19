#! /usr/bin/env python3


def main():
    mm = MythicalMachine()
    mm.run('..\\mml_programs\\prog2.mml')


class MythicalMachine:

    PANEL = '''\
      The Mythical Machine

P reg  {0:06}      I reg  {1:06}

reg 0  {2:06}      reg 5  {7:06}
reg 1  {3:06}      reg 6  {8:06}
reg 2  {4:06}      reg 7  {9:06}
reg 3  {5:06}      reg 8  {10:06}
reg 4  {6:06}      reg 9  {11:06}'''

    def __init__(self):
        self.__mem = [0] * 1000
        self.__reg = [0] * 10
        self.__confirm = True
        self.__p_reg = 0
        self.__i_reg = 0

    def update_panel(self):
        print(self.PANEL.format(self.__p_reg, self.__i_reg, *self.__reg))

    def pause(self, msg):
        if self.__confirm:
            ans = input(msg)
            if ans[:1] in {'a', 'A'}:
                self.__confirm = False

    def cycle(self):
        self.pause('About to retrieve instruction: ')
        self.__i_reg = self.__mem[self.__p_reg]
        self.update_panel()
        self.pause('About to execute instruction: ')
        self.__p_reg += 1
        self.update_panel()
        op_code = self.__i_reg // 10000
        r = self.__i_reg // 1000 % 10
        address = self.__i_reg % 1000
        if op_code == 0:
            return False
        elif op_code == 1:
            self.__reg[r] = self.__mem[address]
        elif op_code == 2:
            self.__mem[address] = self.__reg[r]
        elif op_code == 3:
            self.__reg[r] = address
        elif op_code == 4:
            self.__reg[r] = self.__mem[self.__reg[address]]
        elif op_code == 5:
            self.__reg[r] += self.__reg[address]
        elif op_code == 6:
            self.__reg[r] -= self.__reg[address]
        elif op_code == 7:
            self.__reg[r] *= self.__reg[address]
        elif op_code == 8:
            self.__reg[r] //= self.__reg[address]
        elif op_code == 10:
            self.__p_reg = address
        elif op_code == 11:
            if self.__reg[r] == 0:
                self.__p_reg = address
        self.update_panel()
        return True

    def load_program(self, name):
        with open(name) as file:
            for line in file:
                if line[0] >= '0':
                    try:
                        fields = line.split()
                        address = int(fields[0])
                        instruction = int(fields[1])
                        self.__mem[address] = instruction
                    except (IndexError, ValueError):
                        pass

    def run(self, name):
        self.load_program(name)
        self.__p_reg = 100
        self.__i_reg = 0
        self.update_panel()
        while self.cycle():
            pass

if __name__ == '__main__':
    main()
