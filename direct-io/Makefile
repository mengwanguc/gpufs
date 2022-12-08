CC=gcc
CFLAGS=-I.
OBJ = direct_io.o

%.o: %.c
	$(CC) -c -o $@ $< $(CFLAGS)

direct_io: $(OBJ)
	$(CC) -o $@ $^ $(CFLAGS)

clean:
	rm -f *.o direct_io