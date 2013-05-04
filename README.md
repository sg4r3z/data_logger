DATALOGGER PIERPAOLO

## FILE gps_reader.py

Il file gps_reader permette al raspberry di comunicare con il gps attraverso il demone gpsd

## FILE rs485_reader.py

Il file rs485_reader permette al raspberry di leggere tutti i sensori, interrogandoli per indirizzo, questo restituisce una stringa con tutti i dati letti
Per far funzionare questo modulo, è necessario installare python-serial
	
	sudo apt-get install python-serial

## FILE rc.local

Il file rc.local configura l'ambiente inziale per permettere ai vari moduli di lavorare correttamente
Qui sono state inserite le configurazione del pin sensing del dispositivo di gpio.
Sono state anche inserite 2 righe che stoppano e riavviano il servizio gpsd per farlo funzionare correttamente

## REGOLE UDEV /etc/udev/rules.d/00-myserial.rules

In questo file sono presenti le regole udev dei dispositivi seriali aggiunti.
La prima identifica il gps, creando un link simbolico in /dev/ con il nome di gps_seriale, che verrà utilizzato in seguito, dai programmi che accedereanno al gps

La seconda indetifica il gruppo rs485, la regola verra utilizzata nel modulo python rs485
