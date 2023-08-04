CC=gcc
CFLAGS=-I.
OBJ = direct_io lba_distance_measure

%.o: %.c
	$(CC) -c -o $@ $< $(CFLAGS)

all: $(OBJ)

$(OBJ): %: %.c
	$(CC) -o $@ $^ $(CFLAGS)

clean:
	rm -f *.o $(OBJ)