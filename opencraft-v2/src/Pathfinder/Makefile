all: Pathfinder.so

src/pathfindermod.o: src/pathfindermod.c src/pathfinder.c
	gcc -c src/pathfindermod.c -o src/pathfindermod.o -I /usr/include/python2.5 -Wall -O3

Pathfinder.so: src/pathfindermod.o
	ld -shared src/pathfindermod.o -o Pathfinder.so

clean:
	rm -fr src/pathfinder.o src/pathfindermod.o Pathfinder.so
