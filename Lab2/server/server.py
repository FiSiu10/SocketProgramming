import sys, socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("", int(sys.argv[1])))

while True:
	packet, address = s.recvfrom(20)
	operator = packet[0]
	numberofop = packet[1]

	i = 0

	if operator == 1:
		total = 0 

		while numberofop > 0:
			a = packet[2+i]
			b = a >> 4
			c = a & 0x0f

			total = total + b + c
		
			i += 1
			numberofop -= 2

	if operator == 2:
		while numberofop > 0:
			a = packet[2+i] 	
			b = a >> 4
			c = a & 0x0f
			print("1")
			print(type(a))
			print("2")
			print(type(b))
			print("3")
			print(type(c))

			bit7 = 2**7
			test_c = c & bit7
			if test_c == bit7:
				# negative number
				c = c - 2**8

			test_b = b & bit7
			if test_b == bit7:
				# negative number
				b = b - 2**8

			print("4")
			print(type(bit7))
			print("5")
			print(type(test_c))
			print("6")
			print(type(test_b))

			if i == 0:
				total = b - c
			else:
				total = total - b - c

			i += 1
			numberofop -= 2

	if operator == 4:
		total = 0

		while numberofop > 0:
			a = packet[2+i] 
			b = a >> 4
			c = a & 0x0f

			bit7 = 2**7
			test_c = c & bit7
			if test_c == bit7:
				# negative number
				c = c - 2**8

			test_b = b & bit7
			if test_b == bit7:
				# negative number
				b = b - 2**8

			if i == 0:
				total = b * c
			else:
				if c == 0:
					total = total * b
				else:
					total = total * b * c

			i += 1
			numberofop -= 2

	packet = total.to_bytes(4, byteorder="big", signed=True)
	

	s.sendto(packet, address)