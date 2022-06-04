### Disenio de Lenguajes de Programacion
### Profesor Carlos Valdez
### Andrea Elias
### Carnet 17048

import pickle

### Clase Parser creada a partir del arbol sintactico    
class Parser():
    def __init__(self, tokens):
        self.tokens = tokens
        self.posicion = 0
        self.currentToken = None
        self.lastvalue = None

        self.nextToken = self.tokens[self.posicion]
        self.get()

        self.parser()

    def error(self, reporte):
        print(reporte)

    def expect(self, terminal):
        if self.currentToken == terminal:
            self.get()
        else:
            self.error('SINTAX ERROR')

    def get(self):
        if self.posicion - 1 < 0:
            self.lastvalue = None
        else:
            self.lastvalue = self.tokens[self.posicion - 1][1]

        if self.nextToken == None:
            self.currentToken = None
        else:
            self.currentToken = self.nextToken[0]
        self.posicion = self.posicion + 1

        if self.posicion >= len(self.tokens):
            self.nextToken = None
        else:
            self.nextToken = self.tokens[self.posicion]

    def parser(self):
        self.EstadoInicial()

    def EstadoInicial(self):
        while self.currentToken in ['numero']:
        	if self.currentToken in ['numero']:
        		self.Instruccion()
        		if self.currentToken == "nuevo1":
        			self.expect("nuevo1")
        if self.currentToken == "nuevo2":
        	self.expect("nuevo2")

    def Instruccion(self):
        resultado=0
        resultado = self.Expresion(resultado)
        print("Resultado: ", resultado)

    def Expresion(self, resultado):
        resultado1, resultado2 = 0, 0
        resultado1 = self.Termino(resultado1)
        while self.currentToken in ['nuevo3']:
        	if self.currentToken == "nuevo3":
        		self.expect("nuevo3")
        		resultado2 = self.Termino(resultado2)
        		resultado1+=resultado2; print("Termino: ", resultado1); 
        resultado = resultado1; print("Termino: ", resultado); return resultado;

    def Termino(self, resultado):
        resultado1, resultado2 = 0, 0
        resultado1 = self.Factor(resultado1)
        while self.currentToken in ['nuevo4']:
        	if self.currentToken == "nuevo4":
        		self.expect("nuevo4")
        		resultado2 = self.Factor(resultado2)
        		resultado1*=resultado2
        resultado=resultado1; return resultado;

    def Factor(self, resultado):
        resultado1=0
        resultado1 = self.Numero(resultado1)
        resultado=resultado1; print("Numero: ", resultado); return resultado;

    def Numero(self, resultado):
        if self.currentToken == "numero":
        	self.expect("numero")
        	resultado = int(self.lastvalue); print("Token: ", resultado); return resultado;

### Lectura de pickle del Automata Serializado
with open('tokensScanner.pickle', 'rb') as f:
    tokens = pickle.load(f)

### Correr el Parser
parser = Parser(tokens)

parser.parser()