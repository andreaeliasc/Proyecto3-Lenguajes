### Disenio de Lenguajes de Programacion
### Profesor Carlos Valdez
### Andrea Elias
### Carnet 17048

### Importar el puente
import bridge

### Este sera nuestro programa que recibira un archivo de entrada para leer la gramatica a utilizar
import math
import random
import copy
import pickle

### Se importan los distintos modulos creados para realizar las distintas tareas del proyecto
import lectorExpresionesMejorado
import traductorExpresion_a_AFD
import simulaciones

### Se importa el modulo Nodo para utilizar la estructura definida para nodos
from Nodo import Nodo

### Definicion de constantes
STRING = 'string'
COMPILER = 'COMPILER'
BEGINCOMMENT = '(.'
ENDCOMMENT = '.)'
END = 'END'

CHARACTERS = 'CHARACTERS'
KEYWORDS = 'KEYWORDS'
TOKENS = 'TOKENS'
PRODUCTIONS = 'PRODUCTIONS'
IGNORE = 'IGNORE'
COMILLAS = '"'

PLUS = '+'
MINUS = '-'
DOT = '.'
UNTIL = '..'
ANY = 'ANY'
EXCEPTKEYWORDS = 'EXCEPT KEYWORDS'

anySet = set()
for i in range(9, 128):
    anySet.add(i)
    anySet.add(241)
    anySet.add(209)

### Metodo para determinar si una linea es el header de compiler y si lo es obtener el ident
def compilerHeader(linea):
    linea = linea.strip('\n').strip('\t').strip()
    if linea.startswith(COMPILER):
        return linea.split(COMPILER,1)[1]

    return None

### Metodo para determinar si una linea es el END de compiler y si lo es obtener el ident
def compilerEnd(linea):
    linea = linea.strip('\n').strip('\t').strip()
    if linea.startswith(END):
        return linea.split(END,1)[1]

    return None

### Metodo para determinar si una linea es IGNORE y si lo es obtener el SET
def whiteSpaceIgnore(linea):
    linea = linea.strip('\n').strip('\t').strip()
    if linea.startswith(IGNORE):
        return linea.split(IGNORE,1)[1]

    return None

### Metodo para poder determinar si una linea tiene el inicio de un comentario
def isBeginComment(linea):
    comentario = ''
    linea = linea.strip()
    if linea.startswith(BEGINCOMMENT):
        return True, linea.split(BEGINCOMMENT,1)[1]

    return None, comentario

def isEndComment(linea):
    comentario = ''
    linea = linea.strip()
    if linea.endswith(ENDCOMMENT):
        return True, linea.split(ENDCOMMENT,1)[0]

    return None, comentario

def processCharacter(setCharacter, dictCharacters):
    setCharacter = setCharacter[:-1]
    setCharacter = setCharacter.replace("'", '"')

    comillas = 0
    saltos = None
    signo = None
    set1 = set()
    set2 = set()
    palabra1 = ''
    palabra2 = ''

    for i in range(len(setCharacter)):
        if not saltos:
            if setCharacter[i] == COMILLAS:
                comillas = comillas + 1
                continue
        
            ### Se revisa en busca de un signo o CHR
            if comillas % 2 == 0:
                if (setCharacter[i] == PLUS) or (setCharacter[i] == MINUS) or ((setCharacter[i] == '.') and (setCharacter[i+1] == '.')):
                    if signo:
                        if (len(set1) == 0) and (len(set2) == 0):
                            set1 = dictCharacters[palabra1]
                            set2 = dictCharacters[palabra2]

                            palabra1 = ''
                            palabra2 = ''
                        elif (len(set1) == 0):
                            set1 = dictCharacters[palabra1]
                            palabra1 = ''
                        elif (len(set2) == 0):
                            set2 = dictCharacters[palabra2]
                            palabra2 = ''
                        else:
                            pass

                        ### Se hace la operacion entre los 2 string si hay un signo almacenado
                        if signo == PLUS:
                            set1 = set1.union(set2)
                        elif signo == MINUS:
                            set1 = set1.difference(set2)
                        else:
                            s1 = list(set1)
                            s2 = list(set2)

                            set1 = set()
                            for k in range(int(s1[0]), int(s2[0])+1):
                                set1.add(k)

                        set2 = set()
                        signo = None
                    if (setCharacter[i] == '.') and (setCharacter[i+1] == '.'):
                        saltos = 1
                        signo = UNTIL
                    else:
                        signo = setCharacter[i]
                    continue
                
                ### Se revisa si lo siguiente es CHR(
                if (setCharacter[i] == 'C') and (setCharacter[i+1] == 'H') and (setCharacter[i+2] == 'R') and (setCharacter[i+3] == '('):
                    saltos = 3
                    for j in range(0,len(setCharacter)-i-4):
                        saltos = saltos + 1
                        if setCharacter[i+j+4] == ')':
                            caracter = setCharacter[i+4:i+j+4]

                            if caracter:
                                ### Si ya hay un signo entonces almacenamos en un set2
                                if signo:
                                    set2.add(int(caracter))
                                ### Si no hay un signo entonces almacenamos en un set1
                                else:
                                    ### Se revisa que el 
                                    set1.add(int(caracter))
                            break
                
                else:
                    if signo:
                        palabra2 = palabra2 + setCharacter[i]
                    else:
                        palabra1 = palabra1 + setCharacter[i]

            ### Significa que los caracteres son parte de un conjunto y los almacenamos en un string
            else:
                ### Si ya hay un signo entonces almacenamos en un set2
                if signo:
                    set2.add(ord(setCharacter[i]))
                ### Si no hay un signo entonces almacenamos en un set1
                else:
                    set1.add(ord(setCharacter[i]))
        else:
            saltos = saltos - 1    

    ### Si aun hay un signo despues de recorrer todo el string
    if signo:
        if (len(set1) == 0) and (len(set2) == 0):
            set1 = dictCharacters[palabra1]
            set2 = dictCharacters[palabra2]
        elif (len(set1) == 0):
            set1 = dictCharacters[palabra1]
        elif (len(set2) == 0):
            set2 = dictCharacters[palabra2]
        else:
            pass

        ### Se hace la operacion entre los 2 string si hay un signo almacenado
        if signo == PLUS:
            set1 = set1.union(set2)
        elif signo == MINUS:
            set1 = set1.difference(set2)
        else:
            s1 = list(set1)
            s2 = list(set2)

            set1 = set()
            for k in range(int(s1[0]), int(s2[0])+1):
                set1.add(k)
        set2 = set()
        signo = None

    if (len(set1) == 0) and (len(palabra1) != 0):
        set1 = dictCharacters[palabra1]

    return set1

def processToken(setTokens, dictCharacters):
    ### La variable bandera en 0 significa que no tiene Except Keywords y en 1 significa que la tiene
    bandera = 0

    ### La variable comillas en numeracion par significa que lo que sigue despues de es un string concatenado, e impar significa que es una variable o un signo de la regex
    comillas = 0
    saltos = None
    expresionRegular = ''

    ### Se revisa si se trae la bander EXCEPT KEYWORDS
    if EXCEPTKEYWORDS in setTokens:
        bandera = 1
        setTokens = setTokens.replace(EXCEPTKEYWORDS, '').strip()

    #print(setTokens)
    for i in range(len(setTokens)):
        if not saltos:
            if setTokens[i] == COMILLAS:
                comillas = comillas + 1
                continue

            ### Si comillas es 0 entonces procesamos los caracteres como variables y signos de regex
            if comillas % 2 == 0:
                ### Se revisa hasta donde hay comillas nuevamente para hacer los saltos
                if COMILLAS in setTokens[i:]:
                    #print("----------------------------")
                    indice = setTokens[i:].index('"')
                    saltos = indice - 1

                    ### Se procesa la parte obtenida
                    tokenReplace = setTokens[i:indice + i]

                else:
                    saltos = len(setTokens[i:])
                    tokenReplace = setTokens[i:]

                ### Reemplazamos los signos '{' por '(', y los '}' por ')*', los '[' por '(', y los ']' por ')?'
                tokenReplaceDict = tokenReplace.replace('{', '(').replace('}', ')*').replace('[', '(').replace(']', ')?')

                ### Remplazamos las variables con el diccionario ordenado por len KEY de caracter para formar una expresion regular
                #print(tokenReplaceDict)
                #print(sorted(dictCharacters, key=len, reverse=True))
                for key in sorted(dictCharacters, key=len, reverse=True):
                    if key in tokenReplaceDict:
                        preRegex = ''
                        ### Se procesa el SET para ser una regex en string
                        for value in dictCharacters[key]:
                            preRegex = preRegex + str(value) + '|'

                        tokenReplaceDict = tokenReplaceDict.replace(key, '(' + preRegex[:-1] + ')')

                expresionRegular = expresionRegular + tokenReplaceDict

            ### Si comilllas es 1 entonces procesamos los caracteres concatenados
            else:
                expresionRegular = expresionRegular + str(ord(setTokens[i]))

        else:
            saltos = saltos - 1

    return expresionRegular, bandera

### Funcion para obtener las expresiones como tokens en un diccionario
def tokenizacionProducciones(producciones):
    listaProducciones = []

    ### Lectura de pickle del Automata Serializado
    with open('automataCocol.pickle', 'rb') as f:
        afdd = pickle.load(f)

    ### Lectura de pickle de la definicion de TOKENS Serializado
    with open('tokensCocol.pickle', 'rb') as f:
        tokens = pickle.load(f)

    ### Lectura de pickle de la definicion de TOKENS Serializado
    with open('keywordsCocol.pickle', 'rb') as f:
        keywords = pickle.load(f)

    ### Lectura de pickle de la definicion de IGNORE Serializado
    with open('ignoreCocol.pickle', 'rb') as f:
        ignoreSet = pickle.load(f)

    ### Se revisa cada una de las producciones
    for produccion in producciones:
        tokensList = []

        ### Ahora pasamos el string a la simulacion
        posicion = 0
        while posicion < len(produccion):
            token, posicion, cadenaRetornar = simulaciones.simulacionAFD2(afdd, produccion, posicion, tokens, ignoreSet)

            ### Se limpia la cadena a retornar de los ignores
            cadenaFinal = ''
            for caracter in cadenaRetornar:
                if ignoreSet:
                    caracterAscii = ord(caracter)
                    if caracterAscii in ignoreSet:
                        continue
                cadenaFinal = cadenaFinal + caracter

            if token:
                ### Se obtiene el valor de la bandera del token
                valorToken = tokens[token]
                valorBandera = valorToken[1]

                ### Revisar el valor de la bandera
                if (valorBandera == 1) and (cadenaFinal in keywords.values()):
                    llave = [key for key, value in keywords.items() if value == cadenaFinal]
                    tokensList.append([llave[0], cadenaFinal])
                else:
                    tokensList.append([token, cadenaFinal])
            else:
                pass

        ### Se elimina el primer elemento que es el IDENTIFICADOR de la PRODUCCION
        tokenCopy = copy.deepcopy(tokensList)

        ### Se genera el diccionario de la PRODUCCION
        #diccionarioProducciones[tokensList[0][1]] = tokenCopy
        for token in tokenCopy:
            listaProducciones.append((token[0], token[1]))

    ### Se devuelven las PRODUCCIONES
    return listaProducciones

###-------------------------MAIN---------------------------###
### Se solicita el nombre del archivo
fileName = input("Ingrese el nombre de su archivo de entrada para obtener la gramatica (con su extension): ")

### Se extraen las lineas del archivo que se leera
archivo = open(fileName, 'r', encoding='utf-8')
lineas = archivo.readlines()

identCompiler = None
identEndCompiler = None
thereIsBeginCommet = None
thereIsEndCommet = None
readCharacters = None
readKeywords = None
readTokens = None
readProductions = None
readWhitespace = None

dictCharacters = {}
dictKeywords = {}
dictTokens = {}
dictProductions = {}
listProductions = []
whiteSpace = None

pilaComentario = ''
lineaAnterior = ''
contador = 0

### Agregamos la definicion de ANY a los CHARACTERS
dictCharacters[ANY] = anySet

### Se va haciendo una lectura del archivo linea por linea
for linea in lineas:
    ### Si aun no tenemos el header COMPILER con el ident lo buscamos hasta encontrarlo
    if not identCompiler:
        ### Primero se busca que lo primero en el archivo sea el header con COMPILER ident
        identCompiler = compilerHeader(linea)
        if identCompiler:
            identCompiler = identCompiler.strip()
        continue

    ### Si ya tenemos el header COMPILER con el ident buscamos END ident
    if identCompiler:
        ### Primero se busca que lo primero en el archivo sea el header con COMPILER ident
        identEndCompiler = compilerEnd(linea)
        if identEndCompiler:
            identEndCompiler = identEndCompiler.strip()

        if identEndCompiler:
            if identEndCompiler[-1] != DOT:
                identEndCompiler = identEndCompiler + DOT

            if (identEndCompiler[:-1] == identCompiler):
                break
            elif (identEndCompiler[:-1] != identCompiler):
                print("Error de identificador de COMPILER")
                exit()

    ### Una vez tenemos el COMPILER ident se procede a revisar comentarios
    if not thereIsBeginCommet:
        thereIsBeginCommet, pilaComentario = isBeginComment(linea)
        if thereIsBeginCommet:
            comentario = ''
            thereIsEndCommet, comentario = isEndComment(linea)

            if thereIsEndCommet:
                pilaComentario = pilaComentario + '\n' + comentario
                thereIsBeginCommet = False
                thereIsEndCommet = False

                ### Se muestran los comentarios del archivo en pantalla
                #print(pilaComentario)
            else:
                pilaComentario = pilaComentario + '\n' + linea
            
            continue

    ### Si se inicio un comentario, solo hay que imprimir hasta que termine el comentario
    if thereIsBeginCommet:
        ### Siempre se busca el final del comentario para seguir procesando el resto del archivo
        ### que no esta dentro de los comentarios
        comentario = ''
        thereIsEndCommet, comentario = isEndComment(linea)

        if thereIsEndCommet:
            pilaComentario = pilaComentario + '\n' + comentario
            thereIsBeginCommet = False
            thereIsEndCommet = False

            ### Se muestran los comentarios del archivo en pantalla
            #print(pilaComentario)
        else:
            pilaComentario = pilaComentario + '\n' + linea
        
        continue
    
    ### Si no hay un inicio de comentario se procede a revisar la estructura de COCOR
    if linea.strip() == CHARACTERS:
        readCharacters = True
        readKeywords = False
        readTokens = False
        readProductions = False
        continue
    elif linea.strip() == KEYWORDS:
        readCharacters = False
        readKeywords = True
        readTokens = False
        readProductions = False
        continue
    elif linea.strip() == TOKENS:
        readCharacters = False
        readKeywords = False
        readTokens = True
        readProductions = False
        continue
    elif linea.strip() == PRODUCTIONS:
        readCharacters = False
        readKeywords = False
        readTokens = False
        readProductions = True
        continue
    elif whiteSpaceIgnore(linea.strip()) != None:
        whiteSpace = whiteSpaceIgnore(linea.strip()).strip()

        ### Revisar si el whiteSpace corresponde a un SET
        whiteSpace = whiteSpace.strip().replace("' '", 'CHR(32)').replace(' ', '')
        whiteSpace = whiteSpace.strip('\n').strip('\t').strip()

        ### Ingresar al diccionario si termina con un punto
        if whiteSpace[-1] != DOT:
            whiteSpace = whiteSpace + '.'

        ### Procesar el SET
        whiteSpace = processCharacter(whiteSpace, dictCharacters)

        ### Determinar que no se esta leyendo CHARACTERS, TOKENS, KEYWORDS, ni PRODUCTIONS
        readCharacters = False
        readKeywords = False
        readTokens = False
        readProductions = False
        continue


    ### Revisar si la linea esta vacia y continuar
    if linea.strip() == '':
        continue

    ### Concatenar linea anterior
    linea = lineaAnterior + linea.strip('\n').strip('\t').strip()

    contador = contador + 1


    ### Si estoy leyendo CHARACTERS los proceso como corresponde
    if readCharacters:
        ### Revisar si la linea termina con punto
        if linea.strip('\n').strip('\t').strip()[-1] != DOT:
            lineaAnterior = linea.strip('\n').strip('\t').strip()
            continue

        ### Extraer el ident y el SET
        particionCharacter = linea.partition('=')
        identCharacter = particionCharacter[0].strip()
        setCharacter = particionCharacter[2].strip().replace("' '", 'CHR(32)').replace(' ', '')
        setCharacter = setCharacter.strip('\n').strip('\t').strip()

        ### Ingresar al diccionario si termina con un punto
        if setCharacter[-1] == DOT:
            lineaAnterior = ''

            ### Procesar el SET
            setCharacter = processCharacter(setCharacter, dictCharacters)

            ### Conjutos de CHARACTERS a almacenar (Se van a volver string separador por OR cuando se sutituyan en el TOKEN)
            dictCharacters[identCharacter] = setCharacter

        else:
            lineaAnterior = linea.strip('\n').strip('\t').strip()

        continue

    ### Si estoy leyendo KETWORDS los proceso como corresponde
    if readKeywords:
        ### Revisar si la linea termina con punto
        if linea.strip('\n').strip('\t').strip()[-1] != DOT:
            lineaAnterior = linea.strip('\n').strip('\t').strip()
            continue

        ### Extraer el ident y el SET
        particionKeywords = linea.partition('=')
        identKeyword = particionKeywords[0].strip().replace(' ', '')
        setKeyword = particionKeywords[2].strip().replace('"', '').replace("' '", 'CHR(32)').replace(' ', '')
        setKeyword = setKeyword.strip('\n').strip('\t').strip()

        ### Ingresar al diccionario si termina con un punto
        if setKeyword[-1] == DOT:
            lineaAnterior = ''
            dictKeywords[identKeyword] = setKeyword[:-1]
        else:
            lineaAnterior = linea.strip('\n').strip('\t').strip()

        continue
    ### Si estoy leyendo TOKENS los proceso como corresponde
    if readTokens:
        ### Revisar si la linea termina con punto
        if linea.strip('\n').strip('\t').strip()[-1] != DOT:
            lineaAnterior = linea.strip('\n').strip('\t').strip()
            continue

        ### Extraer el ident y el SET
        particionTokens = linea.partition('=')
        identTokens = particionTokens[0].strip()
        setTokens = particionTokens[2].strip('\n').strip('\t').strip()

        ### Ingresar al diccionario si termina con un punto
        if setTokens[-1] == DOT:
            lineaAnterior = ''

            ### Procesar el TokenExpr a una expresion regular
            expresionRegular, bandera = processToken(setTokens[:-1], dictCharacters)

            dictTokens[identTokens] = [expresionRegular, bandera]
        else:
            lineaAnterior = linea.strip('\n').strip('\t').strip()

        continue

    ### Si estoy leyendo PRODUCTIONS los proceso como corresponde
    if readProductions:
        ### Revisar si la linea termina con punto
        if linea.strip('\n').strip('\t').strip()[-1] != DOT:
            lineaAnterior = linea.strip('\n').strip('\t').strip()
            continue
        
        listProductions.append(linea.strip('\n').strip('\t').strip().replace('\t', ''))
        lineaAnterior = ''

### Revisamos lo obtenido
#print(dictCharacters)
#print(dictKeywords)
#print(dictTokens)
#print(listProductions)
#print(whiteSpace)

### Hacer uso del proyecto 2 para obtener las PRODUCCIONES como TOKENS
if listProductions:
    dictProductions = tokenizacionProducciones(listProductions)
    
    ### Serializar las producciones con Pickle
    with open('productions.pickle', 'wb') as f:
        pickle.dump(dictProductions, f)

    contador = 1
    ### Agregar tokens de tipo string a los tokens
    for produccion in dictProductions:
        if produccion[0] == STRING:
            ### Procesar el TokenExpr a una expresion regular
            expresionRegular, bandera = processToken(produccion[1], dictCharacters)

            nombreToken = 'nuevo' + str(contador)

            if [expresionRegular, bandera] not in dictTokens.values():
                dictTokens[nombreToken] = [expresionRegular, bandera]
                contador = contador + 1

### Se contruye una unica expresion regular con los tokens
expresion = ''
for regex in dictTokens.values():
    expresion = expresion + '(' + regex[0] + ')#|'

expresion = expresion[:-1]

### Mandamos a llamar al bridge para que construya el Scanner con la expresion formada a partir de Tokens
bridge.automata(expresion, dictTokens, dictKeywords, whiteSpace)
