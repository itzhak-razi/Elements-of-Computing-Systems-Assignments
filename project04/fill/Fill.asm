//This program should be an infinite loop that listens for keyboard input.  
//When the user presses any key the screen is darkened.

@SCREEN
D = A
@R0
M = D

(INFINITE_LOOP)
@0
D = !A
@R0
A = M
M = D

@R0
M = M + 1

(KEYBOARD_TEST) 
@KBD
D=M
@KEYBOARD_TEST
D;JEQ //If keyboard == 0 then loop again.



@INFINITE_LOOP
0;JMP
