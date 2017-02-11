##
## main function
##

.balign 4
.global main
main:
   # save lr on stack 
   str lr, [sp, #-8]!
 
   # print program info
   ldr r0, p_svnid
   bl printf

   # loop variable (argument for each shuffle call)
   ldr r0, N_start
   sub r0, r0, #1
   str r0, [sp, #-8]!

   # calls to shuffle function
   main_loop:
      ldr r0, [sp]
      add r0, r0, #1
      str r0, [sp]
      ldr r1, N_end
      cmp r0, r1
      bgt main_end
      bl shuffle
      b main_loop

   # return
   main_end:
      add sp, #8
      ldr lr, [sp], #+8
      mov r0, #0
      bx lr

##
## shuffle function
##

# input: number N in r0
# returns: nothing
# side effect: prints the shuffle number of the input to stdout
# calculates the shuffle number for number given in r0 and prints it

.balign 4
shuffle:
   # save lr on stack
   str lr, [sp, #-8]!

   # r0: N (input)

   # r1: n (current position of first element)
   mov r1, #1
   
   # r2: k (shuffle number)
   mov r2, #0

   # r3: -(2N + 1) == bitwise not of 2N (helper variable)
   mov r3, r0, lsl #1
   mvn r3, r3

   # loop
   shuffle_loop:
      add r2, r2, #1
      cmp r1, r0
      lsl r1, r1, #1
      addgt r1, r1, r3
      cmp r1, #1
      bne shuffle_loop
   
   # print input number (in r0) and result (in r2) and return to main function
   mov r1, r0
   ldr r0, p_format
   ldr lr, [sp], #+8
   b printf

##
## helpers
##

# input numbers
.balign 4
N_start:
   .word 1
.balign 4
N_diff:
   .word 1
.balign 4
N_end:
   .word 10000

# printf related
.global printf
.balign 4
format: .asciz "%d %d \n"
p_format: .word format

# SVN version string
.balign 4
svnid: .asciz "# $Id: main.s 237 2013-07-11 02:04:13Z dh $\n"
p_svnid: .word svnid
