import os,string

if len(os.listdir("/home/pi/data/")) == 0:
	os.system("python /home/pi/data_logger/gps_reader.py 1.txt")
else:
	maggiore = 0
	for filename in os.listdir("/home/pi/data/"):
		n = string.split(filename,".txt")
		numero = int(n[0])
		if maggiore < numero: 
			maggiore = numero
	
	os.system("python /home/pi/data_logger/gps_reader.py "+str(maggiore+1)+".txt")
