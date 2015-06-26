100 030005     ld# r0,5
101 020118     sto r0,term
102 030001     ld# r0,1
103 020117     sto r0,ans
             z1
104 010118     ld r0,term
105 110115     jz  r0,z2
106 011117     ld r1,ans
107 012118     ld r2,term
108 071002     mul r1,r2
109 021117     sto r1,ans
110 011118     ld r1,term
111 032001     ld# r2,1
112 061002     sub r1,r2
113 021118     sto r1,term
114 100104     jmp  z1
             z2
115 010117     ld r0,ans
116 000000     hlt
117 000000   ans 0
118 000000   term 0
