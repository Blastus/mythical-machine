100 030000     ld# r0,0
101 020123     sto r0,fib
102 030001     ld# r0,1
103 020125     sto r0,next
104 030030     ld# r0,30
105 020124     sto r0,index
             z1
106 010124     ld r0,index
107 110121     jz  r0,z2
108 011123     ld r1,fib
109 012125     ld r2,next
110 051002     add r1,r2
111 021126     sto r1,temp
112 011125     ld r1,next
113 021123     sto r1,fib
114 011126     ld r1,temp
115 021125     sto r1,next
116 011124     ld r1,index
117 032001     ld# r2,1
118 061002     sub r1,r2
119 021124     sto r1,index
120 100106     jmp  z1
             z2
121 010123     ld r0,fib
122 000000     hlt
123 000000   fib 0
124 000000   index 0
125 000000   next 0
126 000000   temp 0
