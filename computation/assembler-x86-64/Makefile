ASM     = nasm
PROGS   = main

.PHONY: all
all: $(PROGS)

%: %.asm
	$(ASM) -f elf64 -o $@.o $@.asm
	gcc -O3 -o $@ $@.o

.PHONY: clean
clean:
	rm -f $(PROGS)
	rm -f $(PROGS).o
