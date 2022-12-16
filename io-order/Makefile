CC=gcc
CFLAGS=-I.
OBJ = read get_inode get_lsa

LIBS=-lpthread

all: $(OBJ)

$(OBJ): %: %.c
	$(CC) -o $@ $^ $(CFLAGS) $(LIBS)

clean:
	rm -f *.o $(OBJ)