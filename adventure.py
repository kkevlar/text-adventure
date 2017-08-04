from time import sleep


globalProps = dict()
rooms = []
currRoom = False
parent = False
roomsInitCount = 0;

class Room:
	def __init__(self,lbl='default_label'):
		self.label = lbl
		self.paragraph = ''
		self.choices = dict()
		self.propset = []
		self.conditional = False
		self.contElse = False
		self.isStory = False
		self.isCoords = False
		self.isQInfo = False
	def exe(self):
		globalProps.update(self.propset)

#PARSING

with open("TheRoad.adv") as f:
	for line in f:
		line = line.replace('\n','').trim()
		#ROOM HEADER
		if line.startswith("#"): 
			if currRoom is not False:
				rooms.append(currRoom)
				roomsInitCount += 1
			story = False
			line = line[1:]
			if line[0] is 's' or line[0] is 'S':
				if len(line) is 1 or line[1] is ' ' or line[1] is '\n':
					story = True
					line = line[1:]
			rmName = line.strip();
			if rmName.isspace or len(rmName) == 0:
				if story is True:
					rmName = "StoryRoom%d"%roomsInitCount
			currRoom = Room(rmName)
			if story is True:
				currRoom.isStory = True
		#EMPTY SPACE
		elif line.isspace():
			continue
		elif line.startswith("->")
			line = line[2:]
			currRoom.isQInfo = line.trim()
		#PROPERTY MUTATION
		elif line.startswith('^'):
			currRoom.propset.append(line[1:].trim())
		#PROPERTY TEST
		elif line.startswith('?'):
			line = line[1:].trim()
			if line.startswith("<"):
				line = line[1:].trim()
				intLimit = int(line)
				if ##TODO PROPER PROP TESTS
			currRoom.conditional = True
			cont = line.split("=")
			reslt = cont[1].split("->")
			currRoom.propset.update({
				cont[0]:{
				reslt[0] : reslt[1]
				}
				})
		#PROPERTY ELSE TEST
		elif '->' in line and currRoom.conditional is True:
			spl = line.split("->")
			if spl[0].lower() == "else".lower():
				currRoom.contElse = spl[1]
		#USER RESPONSE DEFINITION
		elif line.startswith("!"):
			sp = line[1:].split("->")
			choiceWords = sp[0].split(",")
			for choice in choiceWords:
				currRoom.choices.update({choice : sp[1]})
		#PARAGRAPH TEXT
		else:
			currRoom.paragraph = currRoom.paragraph + line + '\n'


rooms.append(currRoom)

for room in rooms:
	print("no:%d lbl:%s"%(rooms.index(room),room.label))


#PLAYING


currRoom = rooms[0]
glbCont = False

def findRoom(rmId):
	global rooms
	global currRoom
	global glbCont
	roomFound = False
	for rmm in rooms:
		if rmm.label.lower().strip() == rmId.lower().strip():
			currRoom = rmm
			glbCont = True
			roomFound = True
	if roomFound is False:
		print("FAILED TO FIND ROOM %s" % rmId)

while True:
	if currRoom.conditional is True:
		for gk in globalProps:
			for ck in currRoom.propset:
				if ck in currRoom.propset:
					for ckk in currRoom.propset[ck]:
						if gk.lower() == ck.lower():
							if globalProps[gk].lower() == ckk.lower():
								rmId = (currRoom.propset[ck])
								rmId = rmId[ckk]
								findRoom(rmId)						
		if(glbCont is False and currRoom.contElse is not False):
			rmId = currRoom.contElse
			findRoom(rmId)
	if glbCont is True:
		glbCont = False
		continue
	currRoom.exe();
	for i in range(0,len(currRoom.paragraph)):
		slptime=0.004 #0.04
		char=currRoom.paragraph[i]
		if char is '.':
			slptime=slptime*10
		if char is '\n':
			slptime=slptime*2
		if i is len(currRoom.paragraph) -1:
			slptime=slptime*0
		print(currRoom.paragraph[i],end="",flush=True)
		sleep(slptime)
	#print("")
	if room.isQInfo is not False:
		rmId = room.isQInfo
		findRoom(rmId)
		continue;
	choice = input("  >").replace('\n','')
	if currRoom.isStory is True:
		nIndex = rooms.index(currRoom);
		if(nIndex < 0):
			print("STORY ROOMS NOT LINKED PROPERLY")
		currRoom = rooms[nIndex+1]
		continue;
	if not choice in currRoom.choices:
		print("Not an option. Choices are: ",end="",flush=True)
		for chx in currRoom.choices:
			print(" \"%s\" "%chx,end="",flush=True)
		print("\n")
		continue;
	rmId = currRoom.choices[choice]
	findRoom(rmId)