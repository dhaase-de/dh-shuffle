# for native ARM system (e.g. Raspberry Pi)
AS=$(shell which as)
#CC=$(shell which gcc)
CC=$(shell which clang)

all:
	$(AS) -o main.o main.s
	$(CC) -o main main.o

clean:
	rm -f main main.o
