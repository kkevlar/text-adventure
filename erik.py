
globalProps = dict()
rooms = []
currRoom = False

class Room:
	def __init__(self,lbl='default_label'):
		self.label = lbl
		self.paragraph = ''
		self.choices = dict()
		self.propset = dict()
		self.conditional = False
		self.contElse = False
	def exe(self):
		globalProps.update(self.propset)

with open("story.e") as f:
	for line in f:
		line = line.replace('\n','')
		if line.startswith("#"):
			if currRoom is not False:
				rooms.append(currRoom)
			currRoom = Room(line[1:])
		elif line.isspace():
			continue
		elif '=' not in line and '!' not in line and '->' in line and line.startswith("<") and line.endswith(">"):
			line = line[1:]
			line = line[:-1]
			spl = line.split("->")
			currRoom.propset.update({spl[0]:spl[1]})
		elif '=' in line and '->' in line:
			currRoom.conditional = True
			cont = line.split("=")
			reslt = cont[1].split("->")
			currRoom.propset.update({
				cont[0]:{
				reslt[0] : reslt[1]
				}
				})
		elif '->' in line and currRoom.conditional is True:
			spl = line.split("->")
			if spl[0].lower() == "else".lower():
				currRoom.contElse = spl[1]

		elif line.startswith("!"):
			sp = line[1:].split("->")
			choiceWords = sp[0].split(",")
			for choice in choiceWords:
				currRoom.choices.update({choice : sp[1]})
		else:
			currRoom.paragraph = currRoom.paragraph + line
'''
rm = Room()
rm.label = '0'
rm.paragraph = 'The first room.'
rm.choices.update({
	'die':'die',
	'next':'next-rm'
	})
rooms.append(rm)

exit()

rm = Room()
rm.label = 'die'
rm.paragraph = 'YOU DIED'
rooms.append(rm)

rm = Room()
rm.label = 'next-rm'
rm.paragraph = 'UR in the next rm'
rooms.append(rm)

currRoom = rooms[0]


print(len(rooms))
for rm in rooms:
	print(rm.label)
	print(rm.paragraph)
'''

currRoom = rooms[0]
glbCont = False

while True:
	if currRoom.conditional is True:
		for gk in globalProps:
			for ck in currRoom.propset:
				for ckk in currRoom.propset[ck]:
					if gk.lower() == ck.lower():
						if globalProps[gk].lower() == ckk.lower():
							rmId = (currRoom.propset[ck])
							rmId = rmId[ckk]
							for rmm in rooms:
								if rmm.label.lower() == rmId.lower():
									currRoom = rmm
									glbCont = True
		if(glbCont is False and currRoom.contElse is not False):
			rmId = currRoom.contElse
			for rmm in rooms:
				if rmm.label.lower() == rmId.lower():
					currRoom = rmm
					glbCont = True
					print("yay")
	if glbCont is True:
		glbCont = False
		continue
	currRoom.exe();
	print(currRoom.paragraph)
	choice = input("	>").replace('\n','')
	if not choice in currRoom.choices:
		print("Not an option. Choices are: ",end="",flush=True)
		for chx in currRoom.choices:
			print(" \"%s\" "%chx,end="",flush=True)
		print("\n")
		continue;
	rmId = currRoom.choices[choice]
	for rmm in rooms:
		if rmm.label.lower() == rmId.lower():
			currRoom = rmm