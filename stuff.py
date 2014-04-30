import random
file = open("en-US.dic")

newlist=[]
for line in file:
	newlist.append(line)
	
	
x=random.choice(newlist)

print x
file.close()

