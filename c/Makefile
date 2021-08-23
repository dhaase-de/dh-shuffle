#CC      = gcc
CC      = clang
CFLAGS  = -Wall -Wextra -pedantic -ansi -Wfatal-errors -O3
IFLAGS  = 
LDFLAGS = 
PROGS   = main

.PHONY: all
all: $(PROGS)

%: %.c
	$(CC) $(CFLAGS) $(IFLAGS) $(LDFLAGS) -o $@ $@.c

.PHONY: clean
clean:
	rm -f $(PROGS)
