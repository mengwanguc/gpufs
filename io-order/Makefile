CC=gcc
CFLAGS=-I.
OBJ = read.o

LIBS=-lpthread

%.o: %.c
	$(CC) -c -o $@ $< $(CFLAGS) 

read: $(OBJ)
	$(CC) -o $@ $^ $(CFLAGS) $(LIBS)

clean:
	rm -f *.o read