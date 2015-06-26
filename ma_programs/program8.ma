z1
  ld r0,a
  jz  r0,z2
  ld r1,b
  ld r2,c
  mul r1,r2
  sto r1,b
  ld r1,a
  ld# r2,1
  sub r1,r2
  sto r1,a
  jmp  z1
z2
  hlt
a 0
b 0
