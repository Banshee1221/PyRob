counter = 19
for i in range(8):
	print(i)
	if i % 2 == 0:
		print("even")
		for j in range(counter):
			moveUp()
		for j in range(counter):
			moveRight()
	else:
		print("odd")
		for j in range(counter):
			moveDown()
		for j in range(counter):
			moveLeft()
	counter -= 2
	print("counter")