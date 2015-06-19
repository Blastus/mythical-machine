go    ld#  r0,0      reg 0 will hold the sum
      ld#  r1,nums   reg 1 points to next num
      ld#  r3,1      PATCH
loop  ldi  r2,r1     get next number into reg 2
      jz   r2,done   if its zero we're done
      add  r0,r2     else add it to the sum
      add  r1,r3     PATCH
      jmp  loop      go for the next one
done  hlt            all done. sum is in reg 0
nums  123            the numbers to add
      234
      345
        0            zero marks the end