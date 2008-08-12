all: path.so

pathmod.o: pathmod.c path.c
	gcc -c pathmod.c -I /usr/include/python2.5 -Wall -o pathmod.o `sdl-config --cflags` -g

path.so: pathmod.o
	ld -shared pathmod.o -o path.so `sdl-config --libs`


clean:
	rm -fr path.o pathmod.o path.so
