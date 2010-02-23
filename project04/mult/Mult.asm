 //This is a Hack assembly language program to multiply the numbers in registers
 //R0 and R1

@R2
M=0

(LOOP)
    @R1
    D = M
    @INFINITE_LOOP
    D;JLE


    @R0
    D = M
    @R2
    M = D + M

    @R1
    M = M - 1
    D = M
    @LOOP
    0;JMP

(INFINITE_LOOP)
    @INFINITE_LOOP
    0;JMP 
