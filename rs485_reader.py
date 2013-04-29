import serial

##########################################################################################################################
## SCRIVI COMANDO SU SERIALE
def write_port(data):
# write_port("06 10 46 46")
	dataB = []
	data = data.split(' ')
	for i in range(len(data)):
		dataB.insert(i,int(data[i],16))
	ser.write( "".join(chr(i) for i in dataB) )

##########################################################################################################################
## RECUPERA VALORE REGISTRO DA DISPOSITIVO ISO 1745
def get_value_from(slave_address_high,slave_address_low):
	
	## CONVERTO IL CARATTERE IN VALORE HEX
        hex_high = slave_address_high.encode("hex")
	hex_low = slave_address_low.encode("hex")
	
	## CHIEDO IL DATO AL DISPOSITIVO	
	write_port("04 "+hex_high+" "+hex_low+" 3A 31 05")

	## RECUPERO LA STRINGA IN HEX FINO ALLA FINE
	response = ser.read()
	value_hex = response.encode("hex")
	while(value_hex != '\x03'):
 		value_hex = ser.read()
		response += value_hex

	## MEMORIZZO LA STRINGA IN UNA LISTA ED ELIIMINO TUTTI I CARATTERI DI CONTROLLO
	list = []	
	valore = response.encode("hex")
       		
	for index in range(0,len(valore),2):
		list.append(valore[index:index+2])

	## PULISCO LA STRINGA DAI CARATTERI DI CONTROLLO 02 E 03
	chr_inizio = '02'
	chr_fine = '03'
  	
	## SE PRESENTE CARATTERE INIZIO
	if chr_inizio in list:
		list.pop(list.index(chr_inizio))
	## SE PRESENTE CARATTERE FINE
	if chr_fine in list:
		list.pop(list.index(chr_fine))

	## CONVERTIRE LA LISTA (VALORI HEX) IN ASCII
	stringa_ascii = ""
	for item in list:
		stringa_ascii += chr(int(item,16))
	
	return slave_address_high+slave_address_low+"#"+stringa_ascii

#############################################################################################################################
### MAIN PROGRAM 
ser = serial.Serial(
    port='/dev/ttyUSB0',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)
ser.open()

if ser.isOpen():
	print get_value_from('1','2')
else: 
	print "PROBLEMA DURANTE L'APERTURA DELLA SERIALE"

	



	
