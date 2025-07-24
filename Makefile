CC ?= gcc
CFLAGS = -O2 -Wall -std=c11 -fopenmp

SRC = wildfire.c fire_water.c wildfire_parallel.c test_wildfire.c
HDR = fire.h water.h mountain.h weather.h wildfire.h wildfire_parallel.h fire_water.h

all: test_wildfire

test_wildfire: $(SRC) $(HDR)
	$(CC) $(CFLAGS) $(SRC) -o $@

clean:
	rm -f test_wildfire