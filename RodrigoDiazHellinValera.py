#!/usr/bin/python3

# Es necesario importarlo para utilizar los objetos de socket
from socket import * 
# importamos la librería de arboles de python para la etapaSegunda para realizar las operaciones 
import ast 
#importamos los operadores de python para la etapaSeguna para realizar las cuentas en el árbol de python
import operator as op
#importamos para utlizarlo en la etapaTercera para abrir un recurso por una URL
import urllib.request 
import struct, time, sys

#Son los operadores que podrán venir con las operaciones.
operators = {ast.Add: op.add, ast.Sub: op.sub, ast.Mult: op.mul, ast.Div: op.floordiv}
#Declaramos una variable global para guardar el servidor de la UCLM
UCLM_SERVER = 'atclab.esi.uclm.es' 
#Declaramos una variable global para guardar el puerto de la UCLM
UCLM_PUERTO = 2000 
# Declaramos una variable global para guardar mi puerto Personal
MI_PUERTO = 4000 
# Creamos una tupla con el servidor de la uclm y el puerto para su posterior uso
tupla = (UCLM_SERVER, UCLM_PUERTO) 
print('\n*********************.- RODRIGO DIAZ-HELLÍN VALERA -.************************\n')
print('********************************.- 2º C -.***********************************\n')

#----------------------------------------------------------------------------------------

def etapaCero(): 
	#Creamos un nuevo socket de flujo que usa protocolo TCP
	sock = socket(AF_INET, SOCK_STREAM)
	#Conectamos a ese socket con la tupla de la UCLM
	sock.connect((tupla))
	#Recibimos el mensaje decodificado y lo guardamos en la variable
	mensaje = sock.recv(1024).decode()
	# Mostramos el mensaje
	print('\n' + mensaje + '\n')
	#Cerramos el socket 
	sock.close()
	#Cogemos el identificador que nos da al finalizar la etapa que despues lo usaremos
	id = mensaje.split('\n')
	#Devolvemos el identificador que nos hace falta para la siguiente etapa
	return id [0] 

#----------------------------------------------------------------------------------------
	#pasamos el id que hemos recibido en la etapa anterior
	
#****************************.- Etapa 1 -.************************************************* 
	
	#Crea un servidor UDP en tu máquina (en el puerto que quieras)
 	#Envía un mensaje al servidor UDP atclab.esi.uclm.es:2000
  	#indicando el identificador "93541" y el puerto en el que has creado
  	#tu servidor UDP, separados por un espacio.
  	#Ejemplo: "93541 7777" (sin comillas).

#******************************************************************************************

def etapaPrimera(codigo): 
	#De nuevo, nos creamos otro socket UDP
	UDP_SERVER = socket(AF_INET, SOCK_DGRAM)
	#Ponemos a escuchar en nuestro puerto
	UDP_SERVER.bind(('', MI_PUERTO)) 
	#De nuevo, nos creamos otro socket UDP
	servidor = socket(AF_INET, SOCK_DGRAM)
	#Metemos en una variable el ID junto con el nombre de nuestro puerto
	mensaje_Salida = codigo + ' 4000'
	#Enviamos al servidor de la UCLM el mensaje codificado 
	servidor.sendto((mensaje_Salida.encode()), (tupla))
	#Recibimos le mensaje de nos manda y lo decoficamos
	mensaje = UDP_SERVER.recv(1024).decode()
	#Mostramos el mensaje por pantalla
	print('\n'+ mensaje+'\n')
	#Cogemos el nuevo ID para la siguiente etapa
	puerto = mensaje.split('\n')
	#Cerramos la conexión
	servidor.close()
	#Cerramos la conexión ocn el servidor UDP
	UDP_SERVER.close() 
	#Devolvemos el puerto para la proxima etapa
	return puerto[0]


#----------------------------------------------------------------------------------------

#Introducimos el puerto que nos dio previamente


#****************************.- Etapa 2 -.*************************************************
	
	#Conecta al servidor TCP atclab.esi.uclm.es:1905
	#Recibirás una cadena de texto con una operación matemática en formato ASCII.
	#La expresión contiene paréntesis y están bien balanceados (hay tantos de
	#apertura como de cierre).
	#Calcula el resultado del a operación y responde a través del socket, colocando
	#la cifra resultante entre paréntesis.
	#El proceso se repite para un número indeterminado de operaciones.

#******************************************************************************************

def etapaSegunda(puerto):
	#Creamos un socket
	sock = socket(AF_INET, SOCK_STREAM)
	#Creamos una conexión al servidor de la UCLM con el puerto que hemos recibido
	sock.connect((UCLM_SERVER, int(puerto)))
	#Inicializamos las varibles de los parentesis a 0
	parentesis_Abierto = 0
	parentesis_Cerrado = 0

	#Creamos un bucle infinito para recibir las operaciones 
	while 1:
		#Recibimos la operación y la decodificamos
		operacion = sock.recv(1024).decode()

		#Recorremos la operación para comprobar cuantos paréntesis tiene de apertura y de cierre
		for i in range(len(operacion)):

			if operacion[i] == '(':
				parentesis_Abierto += 1
				pass
			if operacion[i] == ')':
				parentesis_Cerrado += 1
				pass
			pass #for

		#Comprobamos si son distintos y si son seguimos escuchando para completar la operación
		if parentesis_Abierto != parentesis_Cerrado:
			operacion = operacion + sock.recv(1024).decode()
			pass
		#Comprobamos que la operación que hemos recibido empieza por un paretesis 
		if operacion[0] == '(':
			#Si empieza por parentesis comprobamos que tiene el mismo numero de parentesis de apertura y de cierre
			if parentesis_Abierto == parentesis_Cerrado:
				#Llamamos al metodo eval_expr que nos va a evaluar la operación y guardar el resultado en la variable
				resultado = eval_expr(operacion)
				#Le damos el formato al resultado para poder enviarlo
				resultado_Enviar = "("+ str(resultado) + ")"
				#Mostramos por pantalla la operación y el resultado
				print('La operación es: ' + operacion + '   \nResultado: ' + resultado_Enviar + '\n')
				#Enviamos al sock el resultado de la operación para que nos envíe la siguiente operación
				sock.sendto((resultado_Enviar.encode()), (UCLM_SERVER, int(puerto)))
				pass
			pass
		else:
			#Mostramos el código que nos da esta etapa
			print(operacion + '\n')
			#lo metemos en la variable puerto que posteriormente la devolveremos para su utilización en la siguiente etapa
			puerto = operacion.split('\n')
			return puerto[0]
		pass
		#Cerramos la conexión
	sock.close()

#-------------------------------------------------------------------------------------------------
   # Cogido de la siguiente página
   # http://stackoverflow.com/questions/2371436/evaluating-a-mathematical-expression-in-a-string
   # Los siguiente método los que hacen es insertar en los nodos de un arbol los números y los operadores
   # El cual luego es recorrido hasta abajo para luego ir subiendo hasta la raíz. Con el resultado de la operación.
def eval_expr(expr):
	return eval_(ast.parse(expr, mode ='eval').body)

def eval_(node):

    if isinstance(node, ast.Num): # <number>
        return node.n
    elif isinstance(node, ast.BinOp): # <left> <operator> <right>
        return operators[type(node.op)](eval_(node.left), eval_(node.right))
    elif isinstance(node, ast.UnaryOp): # <operator> <operand>
        return operators[type(node.op)](eval_(node.operand))
    else:
        raise TypeError(node)


#----------------------------------------------------------------------------------------
#Introducimos el puerto que vamos a utilizar

#****************************.- Etapa 3 -.*************************************************

	# Debes descargar el fichero "http://atclab.esi.uclm.es:5000/39518".

#******************************************************************************************
def etapaTercera(puerto):
    #Creamos la url a utilizar con el puerto que hemos introducido
    url = "http://atclab.esi.uclm.es:5000/" + puerto
    #Abrimos la dirección url  para leer el archivo con las intrucciones para la siguiente etapa
    msg = (urllib.request.urlopen(url)).read().decode()
    #Mostramos el mensaje
    print(msg)
    #Guardamos la cadena
    cadena = msg.splitlines()[0]
    return cadena

#----------------------------------------------------------------------------------------
	  
 #Utilizado el código de la siguiente dirección: https://bitbucket.org/arco_group/python-net/src/tip/raw/icmp_checksum.py
def cksum(data):

    def sum16(data):
        if len(data) % 2:
        	#Es necesario codificar el dato
            data += '\0'.encode()
            #es necesario añadir una / para hacer la división de enteros
        return sum(struct.unpack('!%sH' % (len(data) // 2), data))

    retval = sum16(data)                       
    retval = sum16(struct.pack('!L', retval)) 
    retval = (retval & 0xFFFF) ^ 0xFFFF
    return retval

#****************************.- Etapa 4 -.************************************************* 

	# Debes enviar un mensaje ICMP Echo Request a atclab.esi.uclm.es.
  	# La carga útil de dicho mensaje debe incluir, DESPUÉS del contenido
  	# habitual, la cadena ASCII "77552".
  	# Recibirás un mensaje ICMP Echo Reply con las instrucciones para continuar.

#******************************************************************************************



def etapaCuatro(puerto):
	#En este paso se obtiene el número de protocolo asociado al nombre de dicho protocolo (icmp).
	Socket_RAW = socket(AF_INET,SOCK_RAW, getprotobyname('icmp'))

	# Creamos la cabecera indicando 0 en el campo Checksum.
	# Estructura de la cabecera: Tipo (8 bits), Código (8 bits), Checksum (16 bits), numero aleatorio, Secuencia (16 bits).
	cabecera = struct.pack('!bbhhh', 8, 0, 0, 3510, 0)

	# Creamos el payload, al final de dicha carga (time.time()) añadimos el puerto que nos asigna la etapa anterior.
	payload = struct.pack('!d5s', time.time(), puerto.encode())

	# Concatenamos 'cabecera' y 'carga' y calculamos el valor de su Checksum.
	valor = cksum(cabecera + payload)

	# Creamos nuevamente la cabecera indicando ahora si, el valor del Checksum.
	cabecera = struct.pack('!bbHhh', 8, 0, valor, 3510, 0)

	# Creamos el paquete ICMP que enviaremos al servidor, concatenando la cabecera nueva y payload
	ICMP = cabecera + payload

	# Enviamos el paquete
	Socket_RAW.sendto(ICMP,(UCLM_SERVER, 1))

	# Recibimos un paquete que que no es válido (solo cabecera)
	msgNoValido = Socket_RAW.recv(1024)

	# Recibimos el mensaje completo
	mensajeValido = Socket_RAW.recv(2048)

	# Recibimos el mensaje completo pero hasta la posición 36 es cabecera. Por lo tanto cojemos a partir del 36
	mensajeValido = mensajeValido[36:].decode()

	# Guardamos el código
	codigo = mensajeValido.split('\n', 1)

   	# Imprimimos el mensaje
	print (mensajeValido)

	# Recogemos el código para la siguiente etapa
	return codigo[0]

     # Cerramos el socket RAW
	Socket_RAW.close()
	


#----------------------------------------------------------------------------------------
	  
def main():
	#Este es el main que ejecutará los métodos según las etapas
	print('\nETAPA 0 ----------->\n')
	print('\nETAPA 0 ----------------------------->\n')
	print('\nETAPA 0 ----------------------------------------------->\n')
	print('\nETAPA 0 ------------------------------------------------------------->\n')
	#Guardamos el identificador que nos devuelve
	id = etapaCero()
	print('\nETAPA 1 ----------->\n')
	print('\nETAPA 1 ----------------------------->\n')
	print('\nETAPA 1 ----------------------------------------------->\n')
	print('\nETAPA 1 ------------------------------------------------------------->\n')
	#Guardamos el puerto que nos da al haber ejecutado el método y haber introducido el identicador anterior
	puerto = etapaPrimera(id)
	print('\nETAPA 2 ----------->\n')
	print('\nETAPA 2 ----------------------------->\n')
	print('\nETAPA 2 ----------------------------------------------->\n')
	print('\nETAPA 2 ------------------------------------------------------------->\n')
	#De la misma manera que en anterior introducimos el puerto a la segundaEtapa y esta nos devolverá otro nuevo puerto
	puerto = etapaSegunda(puerto)
	print('\nETAPA 3 ----------->\n')
	print('\nETAPA 3 ----------------------------->\n')
	print('\nETAPA 3 ----------------------------------------------->\n')
	print('\nETAPA 3 ------------------------------------------------------------->\n')
	#Igual que anterior pero esta vez guardamos una cadena
	cadena = etapaTercera(puerto)
	print('\nETAPA 4 ----------->\n')
	print('\nETAPA 4 ----------------------------->\n')
	print('\nETAPA 4 ----------------------------------------------->\n')
	print('\nETAPA 4 ------------------------------------------------------------->\n')
	ID = etapaCuatro(cadena)
main()

#******************.- WEBGRAFÍA -.***************************
	
	# http://strackoverflow.com/
	# https://bitbucket.org/arco_group/python-net/src/tip/raw/icmp_checksum.py
	# http://docs.python.org/3/

#***********************************************************

