import sys, socket

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
	length = len(sys.argv)
	packet = bytearray(length)
	
	operator = sys.argv[3]
	if operator == "+":
		packet[0] = 1
	if operator == "-":
		packet[0] = 2
	if operator == "*":
		packet[0] = 4

	numberofop = length - 4
	packet[1] = numberofop

	i = 4
	j = 1

	if (numberofop % 2) == 0:
		while numberofop > 0:
			value = int(sys.argv[i])
			value1 = value << 4
			value2 = int(sys.argv[i+1])
			
			packet[j+1] = value1 | value2

			i += 2
			j += 1
			numberofop -= 2
	else:		
		while numberofop > 1:
			value = int(sys.argv[i])
			value1 = value << 4
			value2 = int(sys.argv[i+1])
			
			packet[j+1] = value1 | value2

			i += 2
			j += 1
			numberofop -= 2
		value3 = int(sys.argv[i])
		packet[j+1] = value3 << 4
		numberofop -= 1


	s.sendto(packet, ("localhost", int(sys.argv[2])))
	packet = bytearray(4)
	n = s.recv_into(packet)

	hostInteger = int.from_bytes(packet, byteorder="big", signed=True)
	
	print("Total: %d" % hostInteger + "\n")

	
