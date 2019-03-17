Hola!!

Te dejamos la informaci�n que consideramos m�s relevante para la correcci�n de este laboratorio:

1- Lectura y manejo de los datos entregados: para obtener los datos que nos entregaron usamos la libreria json,
 con lo cual los datos quedan almacenados en un diccionario. Luego, con esta informaci�n creamos los objetos de la clase 
persona y los agregamos a una lista llamada "poblacion". Adem�s, creamos un set con todos los apellidos de las personas. 
Posteriormente dividimos la "poblacion" en dos listas: "lista_familia" donde se junto a las personas que tenian el mismo apellido
y "lista_conyuges" donde se junto a las personas que no tenian a nadie m�s con su mismo apellido. Finalmente, con "lista_familia"
se creo un arbol donde se ordenaron las generaciones de cada familia y luego a cada arbol de una familia, se le agregan los conyuges.

2- Sobre las consultas y los supuestos utilizados: 

	-Para la consulta agregar persona: asumimos que solo nos pedir�n agregar una persona a la vez y nos dar�n todos sus datos,
	 de manera secuencial, en el mismo orden en el cual se entregaban los datos de las personas en el archivo personas.jason

	-Para descendiente m�s lejano: consideramos que cualquier pariente, por ejemplo un sobrino, puede ser considerado descendiente
	 de una persona. Por otro lado, en caso de "empate", es decir, que dos o m�s personas esten a la misma distancia de la persona
	a la cual nos interesa encontrar su descendiente m�s lejano, el programa entregar� todas esas personas dado que todas cumplen
	con ser el descendiente m�s lejano.

	-Para mostrar arbol: Usamos una parte de un codigo que encontramos en internet, tal como recomendaron los profesores, para 
	printear de manera bonita el arbol, donde en este caso, se ve que las rayas muestran las conexiones en la familia. Destacar que 
	para esto se creo un nodo extra para cada familia, con el apellido de la familia, de la cual sale la primera generaci�n de esa
	familia, junto con su conyuge y luego continuan sus hijos. Cada conyuge aparece junto a su pareja que es la del apellido de la
	familia.

3- Precauciones para que el programa no se caiga: junto con crear un men� que orienta a la persona que quiere hacer una solicitud, se
implementaron varios if para ver si se acepta lo ingresado por la persona que hace la solicitud  y varios try para que si ingresa algo que 
aparentemente es valido pero que realmente no cumple con las condiciones (por ejemplo, se ingresa un n�mero que no corresponde a un rut, 
se ingresan letras cuando se espera un n�mero o se ingresa un n�mero cuando se esperan letras)   