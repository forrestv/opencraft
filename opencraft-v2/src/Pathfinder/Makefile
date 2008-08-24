all: Pathfinder.so

src/pathfinder.o: src/pathfinder.c
	gcc -c src/pathfinder.c -o src/pathfinder.o -Wall -O3

src/pathfindermod.o: src/pathfindermod.c
	gcc -c src/pathfindermod.c -o src/pathfindermod.o -I /usr/include/python2.5 -Wall -O3

Pathfinder.so: src/pathfinder.o src/pathfindermod.o
	ld -shared src/pathfinder.o src/pathfindermod.o -o Pathfinder.so

clean:
	rm -fr src/pathfinder.o src/pathfindermod.o Pathfinder.so
