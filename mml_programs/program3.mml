100 030000   go    ld#  r0,0      register 0 will hold the sum, init it
101 031109         ld#  r1,nums   register 1 points to the numbers to add
102 032001         ld#  r2,1      register 2 holds the number one.
103 043001   loop  ldi  r3,r1     get next number into register 3
104 113108         jz   r3,done   if its zero we're finished
105 050003         add  r0,r3     otherwise add it to the sum
106 051002         add  r1,r2     add one to register one (next number to load)
107 100103         jmp  loop      go for the next one
108 000000   done  hlt  00        all done. sum is in register 0
109 000123   nums  123            the numbers to add
110 000234         234
111 000345         345
112 000000           0            end of the list