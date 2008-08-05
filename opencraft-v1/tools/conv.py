i = open("inp")
i = i.read()
i = i.split(",")
i = [x.strip("\n") for x in i]

print len(i)

o = open("out","w")
for x in i:
  o.write(chr(int(x[2],16)*16+int(x[3],16)))
