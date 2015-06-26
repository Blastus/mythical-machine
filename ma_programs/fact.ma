  ld# r0,5
  sto r0,term
  ld# r0,1
  sto r0,ans
z1
  ld r0,term
  jz  r0,z2
  ld r1,ans
  ld r2,term
  mul r1,r2
  sto r1,ans
  ld r1,term
  ld# r2,1
  sub r1,r2
  sto r1,term
  jmp  z1
z2
  ld r0,ans
  hlt
ans 0
term 0
