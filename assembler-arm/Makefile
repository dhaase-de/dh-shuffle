# for native ARM system (e.g. Raspberry Pi)
AS=$(shell which as)
CC=$(shell which gcc)

all:
	$(AS) -o main.o main.s
	$(CC) -o main main.o

clean:
	rm -f main main.o
