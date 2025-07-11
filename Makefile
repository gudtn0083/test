CC=gcc
CFLAGS=-Wall -O2

all: gugudan

# Build gugudan executable from gugudan.c

gugudan: gugudan.c
	$(CC) $(CFLAGS) $^ -o $@

clean:
	rm -f gugudan