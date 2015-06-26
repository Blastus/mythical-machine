  ld# r0,0
  sto r0,fib
  ld# r0,1
  sto r0,next
  ld# r0,30
  sto r0,index
z1
  ld r0,index
  jz  r0,z2
  ld r1,fib
  ld r2,next
  add r1,r2
  sto r1,temp
  ld r1,next
  sto r1,fib
  ld r1,temp
  sto r1,next
  ld r1,index
  ld# r2,1
  sub r1,r2
  sto r1,index
  jmp  z1
z2
  ld r0,fib
  hlt
fib 0
index 0
next 0
temp 0
