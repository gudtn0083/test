CC = gcc
CFLAGS = -Wall -Wextra -std=c99
TARGETS = main example

all: $(TARGETS)

main: main.c main.h
	$(CC) $(CFLAGS) -o main main.c

example: example.c utils.h
	$(CC) $(CFLAGS) -o example example.c

clean:
	rm -f $(TARGETS) test_output.txt

run-main: main
	./main

run-example: example
	./example

.PHONY: all clean run-main run-example