100 030000   reg 0 holds the sum, set to zero
101 031200   put address (200) of 1st number in reg 1
102 032001   reg 2 holds the number one.
103 043001   next number (via reg 1) to reg 3
104 113108   if zero we're done so jump to halt inst
105 050003   otherwise add reg 3 to the sum in reg 0
106 051002   add one (in reg 2) to reg 1 so it points to next number
107 100103   jump back to 103 to get the next number
108 000000   all done so halt. the sum is in reg 0

200 000123   the numbers to add
201 000234
202 000345
203 000000   the end of the list