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

	def success(self,rm):
		try:
			v1 = self.var1
			if v1 == '':
				v1 = rm.visits
			elif self.var1isConstant is False:
				v1 = int (varList[self.var1])
			v2 = self.var2
			if v2 == '':
				v2 = rm.visits
			elif self.var2isConstant is False:
				v2 = int (varList[self.var2])
			ret = False
		except Exception as e:
			return False
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
	def __init__(self,line='',lbl='default_label'):
		self.label = lbl
		self.paragraph = ''
		self.choices = dict()

		self.isStory = False
		self.isCoords = False
		self.isQInfo = False

		self.parent = False
		self.children = []
		self.tests = []

		self.proplist = dict()

		self.visits = 0
		
		self.w = -1
		self.x = 0
		self.y = 0
		self.z = 0

		if not line.isspace():
			if line.startswith('-s') or  line.startswith('-S'):
				line = line[2:].strip()
				self.isStory = True	
				if len(line) is 0 or line[1] is ' ' or line[1] is '\n' or line.isspace():
					self.label = "StoryRoom%d"%roomsInitCount	
				else:
					self.label = line.strip().lower()				
			elif  line.startswith('-c') or  line.startswith('-C'):
				self.isCoords = True
				optCount = 0
				line = line[2:].strip().lower()
				for char in line:
					action = '#'
					chs = []
					if char is 'n':
						action += '0,0,0,1'
						chs.append('n')
						chs.append('north')
					elif char is 's':
						action += '0,0,0,-1'
						chs.append('s')
						chs.append('south')
					elif char is 'e':
						action += '0,1,0,0'
						chs.append('e')
						chs.append('east')
					elif char is 'w':
						action += '0,-1,0,0'
						chs.append('w')
						chs.append('west')
					elif char is 'u':
						action += '0,0,1,0'
						chs.append('u')
						chs.append('up')
					elif char is 'd':
						action += '0,0,-1,0'
						chs.append('d')
						chs.append('down')
					elif char is 'f':
						action += '1,0,0,0'
						chs.append('f')
						chs.append('forward')
					elif char is 'b':
						action += '-1,0,0,0'
						chs.append('b')
						chs.append('back')
					else:
						break
					if action is not '#' and len(chs) > 0:
						for choice in chs:
							self.choices.update({choice:action})
						optCount += 1
				line = line[optCount:]
				splits = line.split('@')
				self.label = splits[0]
				preCommaSplice = splits[1].replace('(','').replace(')','').replace('[','').replace(']','')
				coordStrings = preCommaSplice.split(',')
				self.w = int(coordStrings[0])
				self.x = int(coordStrings[1])
				self.y = int(coordStrings[2])
				self.z = int(coordStrings[3])
			else:
				self.label = line.strip()
		
	def exe(self):
		varList.update(self.proplist)
		self.visits += 1

#varList.update({'snelly':'5'})
#t = ConditionTest('snelly>2')
#print(t.success())
#exit()


#PARSING

with open("test.adv") as f:
	for line in f:
		line = line.replace('\n','').strip()
		#ROOM HEADER
		if line.startswith("@"): 
			if currRoom is not False:
				rooms.append(currRoom)
				roomsInitCount += 1
			story = False
			line = line[1:].strip()
			currRoom = Room(line=line)
		#EMPTY SPACE
		elif line.isspace():
			continue
		#QInfo automatically moves player to next room after printing paragraph
		elif line.startswith("->"):
			line = line[2:]
			currRoom.isQInfo = line.strip()
		#PROPERTY MUTATION
		elif line.startswith('$'):
			currRoom.proplist.update({line[1:].strip() : 1})
		#PROPERTY TEST
		elif line.startswith('?'):
			line = line[1:].strip()
			nTest = ConditionTest(line)
			nRm = Room(lbl="%s-child-%d" % (currRoom.label, len(currRoom.children)))
			nRm.parent = currRoom
			currRoom.children.append(nRm)
			#print("somebody got a child %d" % len(currRoom.children))
			currRoom.tests.append(nTest)
			currRoom = nRm
		elif line.startswith('^'):
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
	print("no:%d lbl:%s story:%s qinfo:%s coords:%s"%(rooms.index(room),room.label, room.isStory, room.isQInfo,room.isCoords))


#PLAYING


currRoom = rooms[0]
glbCont = False

def findRoom(rmId):
	global rooms
	global currRoom
	global glbCont
	roomFound = False
	print(rmId)
	if(rmId.startswith("@") or rmId.startswith("#")):
		coordStrings = rmId[1:].replace('(','').replace(')','').replace('[','').replace(']','').split(",")
		fw = int(coordStrings[0])
		fx = int(coordStrings[1])
		fy = int(coordStrings[2])
		fz = int(coordStrings[3])
		if(rmId[0] == '#'):
			fw += currRoom.w;
			fx += currRoom.x;
			fy += currRoom.y;
			fz += currRoom.z;
		for room in rooms:
			if not room.isCoords:
				continue
			if(fw != room.w):
				continue;
			if(fx != room.x):
				continue;
			if(fy != room.y):
				continue;
			if(fz != room.z):
				continue;
			currRoom = room
			glbCont = True
			roomFound = True
	else:
		for rmm in rooms:
			if rmm.label.lower().strip() == rmId.lower().strip():
				currRoom = rmm
				glbCont = True
				roomFound = True
	if roomFound is False:
		print("FAILED TO FIND ROOM %s" % rmId)

while True:
	glbCont = False
	currRoom.exe();
	print ("coords: %d,%d,%d,%d" % (currRoom.w,currRoom.x,currRoom.y,currRoom.z))
	#print(len(currRoom.tests))
	#print(len(currRoom.children))
	#print("cLen=%d" % len(currRoom.children))
	#print("ROOM: " + currRoom.label)
	if len(currRoom.tests) > 0:
		for test in currRoom.tests:
			if test.success(currRoom):
				num = currRoom.tests.index(test)
				currRoom = currRoom.children[num]
				glbCont = True
				break
		if glbCont is False:
			currRoom = currRoom.children[-1]

	if glbCont is True:
		glbCont = False
		continue
	
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
	if currRoom.isQInfo is not False:
		rmId = currRoom.isQInfo
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
		currRoom.visits -= 1
		continue;
	rmId = currRoom.choices[choice]
	findRoom(rmId)