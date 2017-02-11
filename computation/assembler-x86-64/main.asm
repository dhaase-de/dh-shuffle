extern printf


section .data
    format db "%d %d ", 10, 0


section .text
    global main

    main:
        ; loop range
        mov r13, 1      ; start
        mov r14, 100000 ; end
        mov r15, 1      ; step

        .loop:
            ; calculate shuffle number
            mov r8, 1 ; k
            mov r9, 2 ; n
            mov r10, r13    ; 
            shl r10, 1      ; r10 = 2N + 1
            add r10, 1      ;
            .loop2:
                add r8, 1
                shl r9, 1
                cmp r9, r10
                jle .skipsub
                sub r9, r10
                .skipsub:
                cmp r9, 1
                jne .loop2

            ; print result
            sub rsp, 8
            mov rdi, format
            mov rsi, r13
            mov rdx, r8
            xor rax, rax
            call printf

            ; end reached?
            add r13, r15
            cmp r13, r14
            jle .loop

        ; sys_exit
        mov rax, 60 
        mov rdi, 0
        syscall

