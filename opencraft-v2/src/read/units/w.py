import units

desc = [x for x in sorted(dir(units.units[0])) if x[0] != '_']

#print '<meta http-equiv="refresh" content="1"/>'

print '<table border=2>'
print '<tr><td>ID</td><td>'+'</td><td>'.join(desc)+'</td></tr>'
for i, x in enumerate(units.units):
  print '<tr><td>'+str(i)+'</td><td>'+'</td><td>'.join(map(str,[getattr(x,n) for n in desc]))+'</td></tr>'
print '</table>'
