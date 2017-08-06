from time import sleep

rooms = []
currRoom = False
roomsInitCount = 0;
varList = dict()




class ConditionTest:
	def __init__(self,parseString):
		self.var1 = False
		self.var1isConstant = False
		self.comparison = False
		self.var2 = False
		self.var2isConstant = False

		if(parseString.startswith('?')):
			parseString = parseString[1:]
		v1 = ''
		v2 = ''
		compString = ''
		part = 0
		compCharList = ['!','<','>','=']
		for char in parseString:
			if part is 0:
				if char in compCharList:
					part = 1
				else:
					v1 += char
			if part is 1:
				if char not in compCharList:
					part = 2
				else:
					compString += char
			if part is 2:
				v2 += char
		try:
			self.var1 = int(v1)
			self.var1isConstant = True
		except ValueError:
			self.var1 = v1
			self.var1isConstant = False
		try:
			self.var2 = int(v2)
			self.var2isConstant = True
		except ValueError:
			self.var2 = v2
			self.var2isConstant = False
		self.comparison = compString

	def success(self):
		v1 = self.var1
		if self.var1isConstant is False:
			v1 = int (varList[self.var1])
		v2 = self.var2
		if self.var2isConstant is False:
			v2 = int (varList[self.var2])
		ret = False
		#CURRENTLY greater/lessthan combined with equals
		if self.comparison is '<=':
			ret = (v1 < v2 or v1 is v2)
		elif self.comparison is '>=':
			ret = (v1 > v2 or v1 is v2)
		elif self.comparison is '=<':
			ret = (v1 < v2 or v1 is v2)
		elif self.comparison is '=>':
			ret = (v1 > v2 or v1 is v2)
		elif self.comparison is '=':
			ret = (v1 is v2)
		elif self.comparison is '!=':
			ret = (v1 != v2)
		elif self.comparison is '<':
			ret = (v1 < v2)
		elif self.comparison is '>':
			ret = (v1 > v2)
		

		return ret

class Room:
	def __init__(self,lbl='default_label'):
		self.label = lbl
		self.paragraph = ''
		self.choices = dict()

		self.isStory = False
		self.isCoords = False
		self.isQInfo = False

		self.parent = False
		self.children = []
		self.tests = []
	def exe(self):
		globalProps.update(self.propset)

#varList.update({'snelly':'5'})
#t = ConditionTest('snelly>2')
#print(t.success())
#exit()


#PARSING

with open("TheRoad.adv") as f:
	for line in f:
		line = line.replace('\n','').trim()
		#ROOM HEADER
		if line.startswith("@"): 
			if currRoom is not False:
				rooms.append(currRoom)
				roomsInitCount += 1
			story = False
			line = line[1:].strip()
			if line[0] is 's' or line[0] is 'S':
				if len(line) is 1 or line[1] is ' ' or line[1] is '\n':
					story = True
					line = line[1:]
			rmName = line.strip()
			if rmName.isspace() or len(rmName) == 0:
				if story is True:
					rmName = "StoryRoom%d"%roomsInitCount
			currRoom = Room(rmName)
			if story is True:
				currRoom.isStory = True
		#EMPTY SPACE
		elif line.isspace():
			continue
		#QInfo automatically moves player to next room after printing paragraph
		elif line.startswith("->"):
			line = line[2:]
			currRoom.isQInfo = line.trim()
		#PROPERTY MUTATION
		elif line.startswith('$'):
			currRoom.varList.update({line[1:].trim() : 1})
		#PROPERTY TEST
		elif line.startswith('?'):
			line = line[1:].trim()
			nTest = Test(line)
			nRm = Room(currRoom.lbl + '-child-' + len(currRoom.children))
			nRm.parent = currRoom
			currRoom.children.append(nRm)
			currRoom.tests.append(nTest)
			currRoom = nRm
		elif line.startswith('^')
			currRoom = currRoom.parent
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