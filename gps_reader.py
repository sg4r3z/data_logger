from gps import *
import os,time,serial,datetime,rs485_reader

#############################################################################################################################
### MAIN PROGRAM 

### APRO LA SERIALE
ser = serial.Serial(
    port='/dev/rs485_seriale',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)
ser.open()

### APRO LA CONNESSIONE CON GPS
session = gps()
session.stream(WATCH_ENABLE|WATCH_NEWSTYLE)

shot = 0

while 1:
	
	##os.system('clear')
	report = session.next()
	
	## SE PRESENTE REPORT
	if report != "":
		
		## SE GPS FISSATO
		if session.fix.mode-1 != 0:
			##print 'latitude   ',session.fix.latitude
			##print 'longitude  ',session.fix.longitude
			##print 'time utc   ',session.utc
			##print 'fix        ',("NOFIX","FIX","DGPS_FIX")[session.fix.mode-1]
				
			## ACCENDI IL LED PRESENZA E IMPOSTA SHOT = 1
			os.system("sudo sh -c 'echo 1 > /sys/class/gpio/gpio7/value'")
			shot = 1
			
			## SE SHOT == 1
			if shot == 1:
				
				## LEGGI PULSANTE
				in_file = open("/sys/class/gpio/gpio4/value","r")
				value_shot = int(in_file.read())
				in_file.close()
				
				## SE PREMUTO
				if value_shot == 1:
					
					## RECUPERO LA DATA E LA TRASFORMO IN ITALIANA
					datautc = datetime.datetime.strptime(session.utc, '%Y-%m-%dT%H:%M:%S.%fZ')
					dataita = datautc + datetime.timedelta( 0, 2*60*60)

					## CATTURA LE ALTRE INFORMAZIONI
					## CHIAMA RS485 E RECUPERA STRINGA COMPLETA DI TUTTI I SENSORI
					if ser.isOpen():
						## GIRA TUTTO L'ARRAY DEI SENSORI 485						
						k = rs485_reader.human_readable_string(ser,'1','2',"PROF")
						
					else: 
						print "PROBLEMA DURANTE L'APERTURA DELLA SERIALE"					
						exit(-1)
					
					
					## CREA LA STRINGA DA SCRIVERE SUL FILE
					stringa = "LAT:"+str(session.fix.latitude)+",LON:"+str(session.fix.longitude)+",DATA:"+str(dataita)+','+k
					print stringa
					

			
		
		else:
			## SPEGNI LED SEGNALAZIONE PERSO FIX
			os.system("sudo sh -c 'echo 0 > /sys/class/gpio/gpio7/value'")
			shot = 0
		
	else:
		## SPEGNI LED SEGNALAZIONE
		os.system("sudo sh -c 'echo 0 > /sys/class/gpio/gpio7/value'")
		shot = 0	