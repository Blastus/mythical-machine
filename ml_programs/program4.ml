100 030000   go    ld#  r0,0      reg 0 will hold the sum
101 031109         ld#  r1,nums   reg 1 points to next num
102 033001         ld#  r3,1      PATCH
103 042001   loop  ldi  r2,r1     get next number into reg 2
104 112108         jz   r2,done   if its zero we're done
105 050002         add  r0,r2     else add it to the sum
106 051003         add  r1,r3     PATCH
107 100103         jmp  loop      go for the next one
108 000000   done  hlt            all done. sum is in reg 0
109 000123   nums  123            the numbers to add
110 000234         234
111 000345         345
112 000000           0            zero marks the end