import json
from collections import deque

with open('personas.json') as json_file:
    data = json.load(json_file)
lista_consultas=[]

class Nodo:
    
    def __init__(self, nombre, rut, rut_padre, rut_madre, padre=None):
        self.nombre = nombre
        self.padre = padre
        self.rut = rut
        self.rut_padre = rut_padre
        self.rut_madre = rut_madre
        self.hijos = []

        if padre:
            self.padre.hijos.append(self)

class Persona:
    def __init__(self, rut, nombre, apellido, genero, rut_padre, rut_madre, padre=None):
        self.rut = rut
        self.nombre = nombre
        self.apellido = apellido
        self.genero = genero
        self.rut_madre = rut_madre
        self.rut_padre = rut_padre
        self.hijos = []
        self.padre = padre
        self.conyuge = None
        
        if padre:
            self.padre.hijos.append(self)
        
    def agregar_pareja(self,pareja):
        self.conyuge = pareja

    def __repr__(self):
        return self.nombre

    def agregar_padre(self, padre):
        self.padre = padre

def busca_persona(rut):
    persona=None
    for k in poblacion:
        if k.rut == rut:
            persona = k
    return persona
        
class Arbol:
    def __init__(self, familia):
        self.familia = familia
        self.familia_resp = self.familia[:]
        self.familia_ordenada = []
        self.generaciones_con_conyuges =[]
        self.apellido_fam = None
        self.hijos={}
        self.jefe = None

    def patriarca(self):
        for i in self.familia:
            if i.rut_padre == None and i.rut_madre == None:
                patriarca = i
                self.familia.remove(i)
                self.apellido_fam = patriarca.apellido
                self.familia_ordenada.append([patriarca])
                self.jefe = i
                break
            else:
                None

    def agregar_hijos(self):
        while len(self.familia) > 0:
            aux = []
            a_borrar = []

            for j in self.familia_ordenada:
                for k in j:# para cada posible "padre"
                    hijos_aux = []
                    for i in self.familia: # buscar en el resto de familia
                        if i.rut_padre == k.rut or i.rut_madre == k.rut:
                            aux.append(i)
                            a_borrar.append(i)
                            hijos_aux.append(i)
                        else:
                            None
                    if len(hijos_aux) > 0:
                        self.hijos[k.nombre]=hijos_aux

            self.familia_ordenada.append(aux)
            for j in a_borrar:
                self.familia.remove(j)

    def agregar_persona(self,persona):
        i = 0
        for j in self.familia_ordenada:
            for k in j:
                if persona.rut_padre == k.rut or persona.rut_madre == k.rut:
                    if len(self.generaciones_con_conyuges) > (i+2):
                        self.familia_ordenada[i+1].append(persona)
                        self.generaciones_con_conyuges[i+1].append(persona)#Dado que soy el hijo, me agrego en la generacion siguiente
                        break
                    else:
                        self.familia_ordenada.append([])
                        self.generaciones_con_conyuges.append([])
                        self.familia_ordenada[i+1].append(persona)
                        self.generaciones_con_conyuges[i+1].append(persona)
                        break
                else:
                    None
            i = i + 1

    def agregar_conyu(self,lista):
        agrego_algo = False
        lista_aux = []
        for j in lista:
            i = 0
            for k in self.familia_ordenada:
                lista_aux1 = []
                for t in k:
                    if j.rut == t.rut_padre:
                        lista_aux1.append(t)
                        lista_aux[i-1].append(j) #Dado que soy el padre, me agrego en la generacion anterior
                        madre=busca_persona(t.rut_madre)
                        padre=busca_persona(t.rut_padre)
                        padre.agregar_pareja(madre)
                        madre.agregar_pareja(padre)
                        agrego_algo = True
                        break
                    elif j.rut == t.rut_madre:
                        lista_aux1.append(t)
                        lista_aux[i-1].append(j) #Dado que soy la madre, me agrego en la generacion anterior
                        madre=busca_persona(t.rut_madre)
                        padre=busca_persona(t.rut_padre)
                        padre.agregar_pareja(madre)
                        madre.agregar_pareja(padre)
                        agrego_algo = True
                        break
                    else:
                        lista_aux1.append(t)
                i = i + 1
                if len(lista_aux) < len(self.familia_ordenada):
                    lista_aux.append(lista_aux1)
                else:
                    None
        self.generaciones_con_conyuges = lista_aux
        return (agrego_algo)
    
    def __repr__(self):
        return self.apellido_fam


#obtencion de datos y creacion de objetos (personas)
poblacion=[]
for i in data:
    aux=[]
    for j in data[i]:
        aux.append(data[i][j])
    poblacion.append(Persona(i,aux[0],aux[1],aux[2],aux[3],aux[4]))


#definiendo los conjuntos de personas (con mismo apellido)
set_apellidos= set()
for i in poblacion:
    set_apellidos.add(i.apellido)

id=0
lista_grupos=[]
lista_conyuges=[]
for j in set_apellidos:
    lista_grupos.append([])
    for k in poblacion:
        if k.apellido == j:
            lista_grupos[id].append(k)
    id+=1

lista_familias=[]
for familia in lista_grupos:
    if len(familia)>1:     #es una familia
        lista_familias.append(familia)
    else:         #es conyuge
        lista_conyuges.append(familia[0])

grafos = []
dicc_arboles={}
for i in lista_familias:
    grafo = Arbol(i)
    grafo.patriarca()
    grafo.agregar_hijos()
    grafos.append(grafo)
    dicc_arboles[grafo.apellido_fam]=grafo
for i in grafos:
    i.agregar_conyu(lista_conyuges) 


## -----------------------------------------CONSULTAS--------------------------------------
def cant_per_gen(gen,familia):
    #print(dicc_arboles[familia].generaciones_con_conyuges[gen-1])
    #print(len(dicc_arboles[familia].generaciones_con_conyuges[gen-1]))
    lista_consultas.append(dicc_arboles[familia].generaciones_con_conyuges[gen-1])
    lista_consultas.append(len(dicc_arboles[familia].generaciones_con_conyuges[gen-1]))

def agregar_per(datos): #Asumiendo que me piden agregar de a 1 persona y me entregan sus 6 datos en una lista
    aux=[]
    apellidos_existentes=[]
    se_agrego = False
    for i in datos:
        aux.append(i)
    persona_creada = Persona(aux[0],aux[1],aux[2],aux[3],aux[4],aux[5])
    poblacion.append(persona_creada)
    for i in grafos:
        apellidos_existentes.append(i.apellido_fam)
        if persona_creada.apellido == i.apellido_fam:
            i.agregar_persona(persona_creada)
            se_agrego = True
            break
        else:
            se_agrego = False
            None
    if persona_creada.apellido not in apellidos_existentes:  # se crea en caso de que no exista fam con apellido ingresado
        persona_creada.rut_padre = None
        persona_creada.rut_madre = None
        grafo_nuevo = Arbol([persona_creada])
        grafo_nuevo.patriarca()
        grafo_nuevo.agregar_conyu(lista_conyuges)
        #grafo.agregar_hijos()
        grafos.append(grafo_nuevo)
        dicc_arboles[grafo_nuevo.apellido_fam]=grafo_nuevo
        se_agrego = True
        pass
        
        
    t = 0
    modo_lista = []
    modo_lista.append(persona_creada)
    lista_consultas.append("persona "+ str(persona_creada) +" ha sido ingresada")



                
def fam_con_mas(k):
    largo = []
    for i in grafos:
        largo.append([len(i.familia_ordenada),i])
    t = 0
    while t < k:
        familia = largo[0][1]
        familia_larga = largo[0][0]
        eliminar = [familia_larga, familia]
        for i in largo:
            if i[0] > familia_larga:
                familia_larga = i[0]
                familia = i[1]
                eliminar = [familia_larga, familia]
            else:
                None
        t = t + 1
        largo.remove(eliminar)
        #print("Largo familia es: "+str(familia_larga))
        #print(familia.familia_resp)
        lista_consultas.append(("Largo familia es: "+str(familia_larga)))
        lista_consultas.append(familia.familia_resp)          

def antepasado_comun(rut1,rut2):
    rut_persona1=rut1
    rut_persona2=rut2
    antepasado_per1=[]
    antepasado_per2=[]
    dist=0
    def busca_persona(rut):
        persona=None
        for k in poblacion:
            if k.rut == rut:
                persona = k
        return persona
    persona1=busca_persona(rut_persona1)
    persona2=busca_persona(rut_persona2)
    a = 50
    aux=[]
    while a > 0:
        if len(antepasado_per1) == 0 or len(antepasado_per2) == 0:
            if persona1.rut_padre != None and persona1.rut_madre != None and persona2.rut_padre != None and persona2.rut_madre != None:
                antepasado_per1.append(busca_persona(persona1.rut_padre))
                antepasado_per1.append(busca_persona(persona1.rut_madre))
                antepasado_per2.append(busca_persona(persona2.rut_padre))
                antepasado_per2.append(busca_persona(persona2.rut_madre))
        for i in antepasado_per1:
            if busca_persona(i.rut_padre) != None and busca_persona(i.rut_madre) != None:
                antepasado_per1.append(busca_persona(i.rut_padre))
                antepasado_per1.append(busca_persona(i.rut_madre))
        for j in antepasado_per2:
            if busca_persona(j.rut_padre) != None and busca_persona(j.rut_madre) != None:
                antepasado_per2.append(busca_persona(j.rut_padre))
                antepasado_per2.append(busca_persona(j.rut_madre))
        a-=1
        if len(set(antepasado_per1).intersection(set(antepasado_per2))) > 0:
            aux0 = set(antepasado_per1).intersection(set(antepasado_per2))  # TODOS LOS ANTEPASADOS EN COMUN
            aux =  list(set(aux0).difference(lista_conyuges))               # TODOS LO ANTERIOR MENOS LOS CONYUGES
            lista_consultas.append(("El primer antepasado en común entre "+"["+str(persona1)+" y "+str(persona2)+"]"+"es :"+str(aux[-1])))
            #print("El primer antepasado en común entre","[",persona1,"y",persona2,"]","es :",aux[-1]) # "primer" antepasado en comun
            # aux[-1] el primer antepasado en comun
            break
    if len(aux) != 0:
        def posicion(per):
            pos=0
            while True:
                if per in dicc_arboles[per.apellido].familia_ordenada[pos]:
                    break
                else:
                    pos+=1
            return pos
        dist=posicion(persona1)+posicion(persona2)-2*posicion(aux[-1])
        
        #print("La distancia es:",dist)
        lista_consultas.append(("La distancia es:"+str(dist)))
    else:
        #print("No hay antepasados en comun entre","[",persona1,"-",persona2,"]")
        lista_consultas.append(("No hay antepasados en comun entre"+"["+str(persona1)+"-"+str(persona2)+"]"))

    # posicion da el numero de la generacion en la que se encuentra.
    return

def personas_mas_jovenes(k):
    lista_ruts=[]
    id={}
    for i in poblacion:
        numero=int(i.rut.split("-")[0])
        lista_ruts.append(numero)
        id[numero] = i.rut.split("-")[1]
    lista_ruts_ordenados=sorted(lista_ruts)
    consulta1=[]
    for i in range(k):
        consulta1.append(str(lista_ruts_ordenados[-(i+1)])+'-'+id[lista_ruts_ordenados[-(i+1)]])
        #print(str(lista_ruts_ordenados[-(i+1)])+'-'+id[lista_ruts_ordenados[-(i+1)]])
    lista_consultas.append(consulta1)

def descendiente_mas_lejano(rut_persona): #Printea todas las personas que se encuentran en el menor nivel del arbol, de la familia, del rut ingresado 
    persona=None
    rut_objetivo=rut_persona
    for k in poblacion:
        if k.rut == rut_objetivo:
            persona = k
        else:
            None
    for i in grafos:
        if i.apellido_fam == persona.apellido:
            gen=0
            for h in i.familia_ordenada:
                if persona in h:
                    gen_persona = gen
                encontrado = (h,gen)
                gen+=1
            real_encontrado = encontrado[0]
            #Esta seria si nos pudieran con distancia #real_encontrado = (encontrado[0],encontrado[1]-gen_persona)
            #print("Los descendientes más lejanos de",persona.nombre,"son:",real_encontrado) #O se le podría poner el rut a la persona
            lista_consultas.append(("Los descendientes más lejanos de "+str(persona.nombre)+" son:"+str(real_encontrado)))

def print_arbol(nodo_actual, indent="", last='updown'):

    nb_hijos = lambda nodo: sum(nb_hijos(hijo) for hijo in nodo.hijos) + 1
    size_branch = {hijo: nb_hijos(hijo) for hijo in nodo_actual.hijos}

    """ Creation of balanced lists for "up" branch and "down" branch. """
    up = sorted(nodo_actual.hijos, key=lambda nodo: nb_hijos(nodo))
    down = []
    while up and sum(size_branch[nodo] for nodo in down) < sum(size_branch[nodo] for nodo in up):
        down.append(up.pop())

    """ Printing of "up" branch. """
    for hijo in up:     
        next_last = 'up' if up.index(hijo) is 0 else ''
        next_indent = '{0}{1}{2}'.format(indent, ' ' if 'up' in last else '│', " " * len(nodo_actual.nombre))
        print_arbol(hijo, indent=next_indent, last=next_last)

    """ Printing of current node. """
    if last == 'up': start_shape = '┌'
    elif last == 'down': start_shape = '└'
    elif last == 'updown': start_shape = ' '
    else: start_shape = '├'

    if up: end_shape = '┤'
    elif down: end_shape = '┐'
    else: end_shape = ''

    #print ("{0}{1}{2}{3}".format(indent, start_shape, nodo_actual.nombre, end_shape))
    lista_consultas.append("{0}{1}{2}{3}".format(indent, start_shape, nodo_actual.nombre, end_shape))

    """ Printing of "down" branch. """
    for hijo in down:
        next_last = 'down' if down.index(hijo) is len(down) - 1 else ''
        next_indent = '{0}{1}{2}'.format(indent, ' ' if 'down' in last else '│', " " * len(nodo_actual.nombre))
        #print(hijo)
        print_arbol(hijo, indent=next_indent, last=next_last)

def Mostrar_Arboles(nombre_familia): #incluye conyuges y personas agregadas #incluye conyuges y personas agregadas
    lista_fam = []
    nodos=[]
    t = 0
    for j in grafos:
        p = Persona( str(t), j.apellido_fam, j.apellido_fam, None, None, None, None)
        lista_fam.append(p)
        n = Nodo(p.nombre, p.rut, None, None)
        nodos.append(n)
        t = t + 1
    for i in poblacion:
        if i.rut_padre == None and i.rut_madre == None:
            for h in lista_fam:
                if h.apellido == i.apellido:
                    nombre = i.nombre
                    i.agregar_padre(h) #Ojo que a conyuges estan quedando como patriarcas
        else:
            for k in poblacion:
                if i.rut_padre == k.rut:
                    padre = k
                    nombre = i.nombre
                    i.agregar_padre(k)
                elif i.rut_madre == k.rut:
                    madre = k
                    nombre = i.nombre
                    i.agregar_padre(k)
                else:
                    None
    for i in poblacion:
        if i.rut_padre == None and i.rut_madre == None:
            for h in lista_fam:
                #print(i.padre)
                if i.padre == h:
                    for u in nodos:
                        if u.nombre == i.apellido:
                            if i.conyuge!= None:
                                conyuge=str(i.conyuge)
                                a=str(' + ')
                            else:
                                conyuge=''
                                a=''
                            nombre = i.nombre
                            nombre = Nodo(i.nombre+ a +conyuge, i.rut, i.rut_padre, i.rut_madre, u)
                            nodos.append(nombre)
        else:
            for k in nodos:
                if i.rut_padre == k.rut:
                    if i.conyuge!= None:
                        conyuge=str(i.conyuge)
                        a=str(' + ')
                    else:
                        conyuge=''
                        a=''
                    nombre = i.nombre
                    nombre = Nodo(i.nombre+ a +conyuge, i.rut, i.rut_padre, i.rut_madre, k)
                    nodos.append(nombre)
                elif i.rut_madre == k.rut:
                    if i.conyuge!= None:
                        conyuge=str(i.conyuge)
                        a=str(' + ')
                    else:
                        conyuge=''
                        a=''
                    nombre = i.nombre
                    nombre = Nodo(i.nombre+ a +conyuge, i.rut, i.rut_padre, i.rut_madre, k)
                    nodos.append(nombre)
                else:
                    None
    #for i in POBLACION:
        #print(i.padre)
    for k in lista_fam:
        if nombre_familia == k.nombre:
            fam = k
            for i in nodos:
                if i.nombre == fam.nombre:
                    print_arbol(i)
                
                
#--------------------------------------Ejecucion consultas--------------------------------------
#cant_per_gen(2,0) #Serian los hijos del patriarca (por eso arriba le puse el -1)
#cant_per_gen(2,1)
#cant_per_gen(2,2)
#agregar_per(["1924526-k", "Juanito", "Gonzalez", "Masculino", "9999999-9", "10999825-7"])
#for k in grafos:
    #if k.apellido_fam == "Gonzalez":
        #print(k.familia_ordenada) #Con Juanito agregado

#fam_con_mas(3)

#for i in grafos:
#    print(i.familia_ordenada, "sin conyuges")
#    print(i.generaciones_con_conyuges, "con conyuges")

#personas_mas_jovenes(3)

#antepasado_comun('12646363-3','13714991-8') #april 12646363-3, 13714991-8 james, jon 16302658-9, JAMES Y APRIL SON HERMANOS, JON ES SU PRIMO
#antepasado_comun('16107137-4','8350373-3')  # prueba del hijo de duane; Heather ; con hijo de cheryl: JASON (sobrino)
#antepasado_comun('12646363-3','8350373-3')

#descendiente_mas_lejano('20289115-5') #Dado que es el rut de Crystal, nos tira a su ¿hijo? Jason
#descendiente_mas_lejano('16446564-2') #Dado que es el rut de daniel, nos tira los 6 nietos 
#descendiente_mas_lejano('11514289-4')  #Dado que es el rut de Jessica, nos tira los 6 sobrinos 

#  Familia => persona.apellido + conyuge 
#Mostrar_Arboles('Thompson')
#Mostrar_Arboles('Gonzalez')
#Mostrar_Arboles('Carrillo')



#print(dicc_arboles)

#----------------------------------------menu------------------------------
def programa():
    opt=0
    print("Hola!, realiza tus consultas")
    print("1: Antepasado en Común")
    print("2: Descendiente más lejano")
    print("3: Cantidad de personas por generación")
    print("4: Personas más jóvenes")
    print("5: Familia con más generaciones")
    print("6: Mostrar Familia")
    print("7: Agregar persona")
    print("8: Salir")
    numero_consulta=1
    while opt != 8:
        registro=[]
        for i in poblacion:
            registro.append(i.rut)
        while True:
            try:
                print("_________________________________________________")
                opt = int(input('Ingresa alguna opción : '))
                break
            except:
                print("That's not a valid option!")
        if opt==1:
            print("Ingresa los ruts de los a consultar antepasados:")
            while True:
                try:
                    rut1= str(input('Ingresa el rut 1: '))
                    rut2= str(input('Ingresa el rut 2: '))
                    if rut1 in registro and rut2 in registro and rut1!=rut2:
                        break
                    elif rut1==rut2:
                        print("mismo rut!")
                    else:
                        print(" ruts no encontrados intenta de nuevo")
                except:
                    print("ruts invalidos!")
            lista_consultas.append(("_________________________________________________"))
            lista_consultas.append(("CONSULTA N°"+str(numero_consulta) +": Antepasado Común"))
            antepasado_comun(rut1,rut2)
            numero_consulta+=1
            print("Su consulta se ha ingresado exitosamente!")

        elif opt==2:
            print("Ingresa el rut del la persona a consultar descendientes:")
            while True:
                try:
                    rut1= str(input('Ingresa el rut 1: '))
                    if rut1 in registro:
                        break
                    else:
                        print(" rut no encontrado intenta de nuevo")
                except:
                    print("rut invalido!")
            lista_consultas.append(("_________________________________________________"))
            lista_consultas.append(("CONSULTA N°"+str(numero_consulta) +": Descendiente más lejano"))
            descendiente_mas_lejano(rut1)
            numero_consulta+=1
            print("Su consulta se ha ingresado exitosamente!")
            
        elif opt==3:
            print("Ingresa el número de generacion y familia en particular:")
            while True:
                try:
                    Num_gen = int(input('Ingresa el numero de generación ej:2 : '))
                    familia= str(input('Ingresa la familia ej:Carrillo :'))
                    if familia in dicc_arboles and Num_gen<=len(dicc_arboles[familia].generaciones_con_conyuges):
                        break
                    elif familia not in dicc_arboles:
                        print("Familia no encontrada")
                        
                    elif Num_gen>len(dicc_arboles[familia].generaciones_con_conyuges):
                        print("Generación inexistente")
                    
                    else:
                        print("Familia no encontrada o generación inexistente")
                except:
                    print("parametros invalidos!")
            lista_consultas.append(("_________________________________________________"))
            lista_consultas.append(("CONSULTA N°"+str(numero_consulta) +": Cantidad personas por gen"))
            cant_per_gen(Num_gen,familia)
            numero_consulta+=1
            print("Su consulta se ha ingresado exitosamente!")
            
        elif opt == 4:
            print("Ingresa la cantidad de personas mas jovenes a retornar")
            while True:
                try:
                    k = int(input('Ingresa numero entero : '))
                    if k<=len(poblacion):
                        break
                    else:
                        print("ha excedido el numero maximo de la población")
                except:
                    print("parametros invalidos!")
            lista_consultas.append(("_________________________________________________"))
            lista_consultas.append(("CONSULTA N°"+str(numero_consulta) +": Cantidad personas mas jovenes"))
            personas_mas_jovenes(k)
            numero_consulta+=1
            print("Su consulta se ha ingresado exitosamente!")
            
            pass
        elif opt == 5:
            print("Ingrese un numero de familas que tengan mas generaciones")
            while True:
                try:
                    k = int(input('Ingresa numero entero : '))
                    if k<=len(grafos):
                        break
                    else:
                        print("ha excedido el numero maximo de familias existentes")
                except:
                    print("parametros invalidos!")
            lista_consultas.append(("_________________________________________________"))
            lista_consultas.append(("CONSULTA N°"+str(numero_consulta) +": Familias con mas generaciones"))
            fam_con_mas(k)
            numero_consulta+=1
            print("Su consulta se ha ingresado exitosamente!")
            
        elif opt == 6:
            print("Ingrese nombre de familia a consultar arbol genealogico")
            while True:
                try:
                    familia = str(input('Ingresa nombre de la familia '))
                    if familia in dicc_arboles :
                        break
                    else:
                        print("Parametro invalido, familia no encontrada")

                except:
                    print("parametros invalidos!")
            lista_consultas.append(("_________________________________________________"))
            lista_consultas.append(("CONSULTA N°"+str(numero_consulta) +": Arbol Genealogico"))
            Mostrar_Arboles(familia)
            numero_consulta+=1
            print("Su consulta se ha ingresado exitosamente!")
            
        elif opt == 7:
            print("Ingrese datos de la persona a agregar ej: ")
            while True:
                try:
                    rut = str(input('Ingresa el rut : '))
                    nombre = str(input('Ingresa nombre : '))
                    apellido = str(input('Ingresa apellido : '))
                    sexo = str(input('Ingresa sexo : '))
                    rut_padre = str(input('Ingresa rut del padre : '))
                    rut_madre = str(input('Ingresa rut de la madre : '))
                    break
                except:
                    print("parametros invalidos!")
            lista_consultas.append(("_________________________________________________"))
            lista_consultas.append(("CONSULTA N°"+str(numero_consulta) +": Agregar Persona"))
            agregar_per([rut, nombre, apellido, sexo, rut_padre, rut_madre])
            numero_consulta+=1
            print("Su consulta se ha ingresado exitosamente!")

            
            pass
        elif opt == 8:
            print("###################################################################")
            print("-------------------------SUS CONSULTAS REALIZADAS--------------------------")
            print("###################################################################")
        
            #print("sus consultas:")
            for i in lista_consultas:
                print(i)
            print("###################################################################")
            print("-------------------------HA SALIDO DEl PROGRAMA---------------------------")
            print("###################################################################")
            
            break
        else:
            opt=input("Ingresa alguna opción valida!")

programa()

