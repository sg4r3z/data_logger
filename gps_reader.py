from gps import *
import os,time,serial,datetime,rs485_reader,string,sys

#############################################################################################################################
### MAIN PROGRAM 

print "-------------------GPS TRACKER 1.0-------------------"
print "--LED VERDE FISSO = GPS AGGANCIATO"
print "--LED LAMPEGGIANTE = ACQUISIZIONE DATI"
print "--LED SPENTO = PROBLEMA (GPS PERSO, PROBLEMI RS485"
print "-----------------------------------------------------"
print "FILE : "+sys.argv[1]

storage_file = "/home/pi/data/"+sys.argv[1]
### APRO LA SERIALE
ser = serial.Serial(
    port='/dev/rs485_seriale',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=0
)
ser.open()
print "Apertura Seriale 485"

### APRO LA CONNESSIONE CON GPS
session = gps()
session.stream(WATCH_ENABLE|WATCH_NEWSTYLE)
print "Apertura collegamento con GPS"

## NON HO MAI FATTO UNO SHOT
shot = 0

## CARICA ARRAY SENSORI 485
## PREPARO L'ARRAY CONTENENTE LE RIGHE DI CONFIGURAZIONE
serial_485 = []

## CARICO LA CONFIGURAZIONE
try:
	file = open("/home/pi/data_logger/485_conf.txt","r")
	for line in file.readlines():
		line = line.replace("\n","")
		line = line.replace("\r","")
		val = string.split(line,',')
		serial_485.append(val)
	file.close()
	
except IOError:
	print "ERRORE DURANTE LA LETTURA DEL FILE DI CONFIGURAZIONE"
	exit(-1)

while 1:
	
	## LEGGI DA GPS
	report = session.next()
	
	## SE SESSIONE GPS PRESENTE
	if report != "":
		
		## SE GPS FISSATO
		if session.fix.mode-1 != 0:

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
					
					## FACCIO LAMPEGGIARE PER SEGNALARE LO SHOT
					os.system("sudo sh -c 'echo 0 > /sys/class/gpio/gpio7/value'")

					## RECUPERO LA DATA E LA TRASFORMO IN ITALIANA
					datautc = datetime.datetime.strptime(session.utc, '%Y-%m-%dT%H:%M:%S.%fZ')
					dataita = datautc + datetime.timedelta( 0, 2*60*60)

					## CATTURA LE ALTRE INFORMAZIONI DEI SENSORI 485
					if ser.isOpen():
						
						## GIRA TUTTO L'ARRAY DEI SENSORI 485
						string_485 = ""
						
						for i in range(0,len(serial_485)):	
							sens = serial_485[i]					
							string_485 += rs485_reader.human_readable_string(ser,sens[0],sens[1],sens[2])
							if i < len(serial_485)-1:
								string_485 += ','		
							
							
					else: 
						## SPENGO IL LED PER SEGNALARE IL PROBLEMA
						os.system("sudo sh -c 'echo 0 > /sys/class/gpio/gpio7/value'")
						print "PROBLEMA DURANTE L'APERTURA DELLA SERIALE"					
						exit(-1)
					
					
					## CREA LA STRINGA DA SCRIVERE SUL FILE
					stringa = "LAT:"+str(session.fix.latitude)+",LON:"+str(session.fix.longitude)+",DATA:"+str(dataita)+','+string_485
					fl_file = open(storage_file,"a")
					fl_file.write(stringa+'\n')
					fl_file.close()

					print stringa

					os.system("sudo sh -c 'echo 1 > /sys/class/gpio/gpio7/value'")

			
		
		else:
			## SPEGNI LED SEGNALAZIONE PERSO FIX
			os.system("sudo sh -c 'echo 0 > /sys/class/gpio/gpio7/value'")
			shot = 0
		
	else:
		## SPEGNI LED SEGNALAZIONE
		os.system("sudo sh -c 'echo 0 > /sys/class/gpio/gpio7/value'")
		shot = 0	
