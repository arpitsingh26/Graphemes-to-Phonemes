import sys
from itertools import izip


avgaccuracy=0
i=1
while i<6:
	s1="inputgp"+str(i)+".txt"
	s2="respg"+str(i)+".txt"
	with  open(s1,'r') as wfile1, open(s2,'r') as wfile2:
		totalg=0
		totalmg=0
		for a, b in izip(wfile2,wfile1):
			a=a.split()
			b=b.split()
			ab=len(a)
			totalg=totalg+ab
			for j in range(0,ab):
				if a[j]==b[j]:
					totalmg=totalmg+1
		avgaccuracy=avgaccuracy+totalmg*1.0/totalg
	i=i+1
print avgaccuracy*20

			
l2=[]
for line in sys.stdin.readlines():
	l=line.split()
	if '(' in l[0]:
		if (len(l[0])-3==(len(l)-1)) :
			if not ((line in l2) or ('.'  in line) or ('\'' in line) or ('-' in line) or ('_' in line)):
				l2.append(line)
	elif len(l[0])==(len(l)-1):
		if not ((line in l2) or ('.'  in line) or ('\'' in line) or ('-' in line) or ('_' in line)):
			l2.append(line)

for i in range(0, len(l2)):
	sys.stdout.write("%s"%l2[i])

for line in sys.stdin.readlines():
	l=line.split()
	k=l[0]+"\n"
	wfile2.write(k)
	k=""
	for i in range(1,len(l)-1):
		k=k+l[i]+" "
	k=k+l[len(l)-1]+"\n"
	wfile1.write(k)
			
