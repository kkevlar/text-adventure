
globalProps = dict()
rooms = []
currRoom = False

class Room:
	def __init__(self,lbl='default_label'):
		self.label = lbl
		self.paragraph = 'default_paragraph\n\n<NO TEXT RN>'
		self.choices = dict()
		self.propset = dict()
	def exe(self):
		globalProps.update(self.propset)

with open("erik.story") as f:
	for line in f:
		print(line + "ddd")
		print("moa")
		if '#' in line:
			if currRoom is not False:
				rooms.append(currRoom)
				print("append")
			currRoom = Room(line[1:])
		else:
			currRoom.paragraph.append(line)
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
while True:
	print(currRoom.paragraph)
	print(currRoom.choices)
	choice = input("\n>")
	print(choice)
	rmId = currRoom.choices[choice]
	print(rmId)
	for rmm in rooms:
		if rmm.label is rmId:
			currRoom = rmm
'''
print(len(rooms))
for rm in rooms:
	print(rm.label)
	print(rm.paragraph)