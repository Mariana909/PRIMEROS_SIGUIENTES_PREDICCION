from tabulate import tabulate
import csv
import sys
""""
  Terminales: minúsculas, números y operadores
  No terminales: mayúsculas
  Derivación: "->"
  Simbolo vacío: _

  Formato
  A -> a B
  A -> b A 
  A -> _
  B -> a A 
  B -> b B
"""
class gramatica:
    def __init__(self, nombre, terminales, no_terminales, simbolo_inicial, producciones):
        self.nombre = nombre
        self.terminales = terminales
        self.no_terminales = no_terminales
        self.simbolo_inicial = simbolo_inicial
        self.producciones = producciones

    def __str__(self):
        filas_prod = [
            [f"{nt} -> {' '.join(prod)}"]
            for nt, prods in self.producciones.items()
            for prod in prods
        ]
        t = tabulate(filas_prod, tablefmt="simple")
        return (
            f"Gramática:       {self.nombre}\n"
            f"Símbolo inicial: {self.simbolo_inicial}\n"
            f"No terminales:   {{ {', '.join(self.no_terminales)} }}\n"
            f"Terminales:      {{ {', '.join(self.terminales)} }}\n"
            f"Producciones:\n{t}"
        )

class psp:
    def __init__(self, gramatica):
        self.gramatica = gramatica
        self.PRIMEROS = {}
        self.SIGUIENTES = {}
        self.PREDICCION = {}
    
    def calcular_PRIMEROS(self):
        for no_terminal in self.gramatica.no_terminales:
            self.PRIMEROS[no_terminal] = set()
        # Regla 1: Si X -> _; entonces PRIMEROS(X) incluye _
        for no_terminal, producciones in self.gramatica.producciones.items():
            for produccion in producciones:
                if produccion == ['_']:
                    self.PRIMEROS[no_terminal].add('_')
        # Regla 2: Si X es un terminal, entonces PRIMEROS(X) = {X}
        for terminal in self.gramatica.terminales:
            self.PRIMEROS[terminal] = {terminal}
        # Regla 3: Si X -> Y1 Y2 ... Yn; entonces PRIMEROS(X) incluye PRIMEROS(Y1) sin _
        # Si PRIMEROS(Y1) incluye _, entonces incluye PRIMEROS(Y2)
        # Si PRIMEROS(Y1) y PRIMEROS(Y2) incluyen _, entonces incluye PRIMEROS(Y3) y así sucesivamente
        # Si todos los Yi incluyen _, entonces incluye _
        cambios = True
        while cambios:  
            cambios = False
            
            for no_terminal, producciones in self.gramatica.producciones.items():
                for produccion in producciones:
                    if produccion == ['_']:
                        continue
                    for simbolo in produccion:
                        if simbolo == '_':
                            if '_' not in self.PRIMEROS[no_terminal]:
                                self.PRIMEROS[no_terminal].add('_')
                                cambios = True
                            break
                        elif simbolo in self.gramatica.terminales:
                            if simbolo not in self.PRIMEROS[no_terminal]:
                                self.PRIMEROS[no_terminal].add(simbolo)
                                cambios = True
                            break
                        else:  # es un no-terminal
                            antes = len(self.PRIMEROS[no_terminal])
                            self.PRIMEROS[no_terminal].update(self.PRIMEROS[simbolo] - {'_'})
                            if len(self.PRIMEROS[no_terminal]) != antes:
                                cambios = True
                            if '_' not in self.PRIMEROS[simbolo]:
                                break
                    else:
                        if '_' not in self.PRIMEROS[no_terminal]:
                            self.PRIMEROS[no_terminal].add('_')
                            cambios = True
   
    def calcular_SIGUIENTES(self):
        for no_terminal in self.gramatica.no_terminales:
            self.SIGUIENTES[no_terminal] = set()
        # Regla 1: El símbolo inicial siempre incluye $
        self.SIGUIENTES[self.gramatica.simbolo_inicial] = {'$'}
        # Regla 2: Si A -> α B β; entonces SIGUIENTES(B) incluye PRIMEROS(β) sin _
        # Si PRIMEROS(β) incluye _ o β=_, entonces SIGUIENTES(B) incluye SIGUIENTE(A)
        cambios = True
        while cambios:
            cambios = False
            for no_terminal, producciones in self.gramatica.producciones.items():
                for produccion in producciones:
                    for i, simbolo in enumerate(produccion):
                        if simbolo in self.gramatica.no_terminales:
                            siguientes_antes = len(self.SIGUIENTES[simbolo])
                            # Agregar PRIMEROS(β) sin _
                            if i + 1 < len(produccion):
                                beta = produccion[i + 1:]
                                primeros_beta = set()
                                for b in beta:
                                    if b in self.gramatica.terminales:
                                        primeros_beta.add(b)
                                        break
                                    else:
                                        primeros_beta.update(self.PRIMEROS[b] - {'_'})
                                        if '_' not in self.PRIMEROS[b]:
                                            break
                                self.SIGUIENTES[simbolo].update(primeros_beta)
                            # Agregar SIGUIENTES(A) si PRIMEROS(β) incluye _ o β=_
                            beta_puede_ser_vacio = all(
                                '_' in self.PRIMEROS.get(b, set()) 
                                for b in produccion[i+1:]
                            ) if i + 1 < len(produccion) else True

                            if beta_puede_ser_vacio:
                                self.SIGUIENTES[simbolo].update(self.SIGUIENTES[no_terminal])
    def calcular_PREDICCION(self):
        for no_terminal, producciones in self.gramatica.producciones.items():
            for produccion in producciones:
                conjunto_prediccion = set()
                if produccion == ['_']:
                    conjunto_prediccion.update(self.SIGUIENTES[no_terminal])
                else:
                    for simbolo in produccion:
                        if simbolo in self.gramatica.terminales:
                            conjunto_prediccion.add(simbolo)
                            break
                        else:
                            conjunto_prediccion.update(self.PRIMEROS[simbolo] - {'_'})
                            if '_' not in self.PRIMEROS[simbolo]:
                                break
                    else:
                        conjunto_prediccion.update(self.SIGUIENTES[no_terminal])
                self.PREDICCION[(no_terminal, tuple(produccion))] = conjunto_prediccion

    def _construir_tablas(self):
        filas_ps = [
            [nt,
             "{ " + ", ".join(sorted(self.PRIMEROS[nt])) + " }",
             "{ " + ", ".join(sorted(self.SIGUIENTES[nt])) + " }"]
            for nt in self.gramatica.no_terminales
        ]
        filas_pred = [
            [f"{nt} -> {' '.join(prod)}",
             "{ " + ", ".join(sorted(conj)) + " }"]
            for (nt, prod), conj in self.PREDICCION.items()
        ]
        return filas_ps, filas_pred
 
    def exportar_csv(self):
        filas_ps, filas_pred = self._construir_tablas()
        nombre_archivo = f"{self.gramatica.nombre}.csv"
        with open(nombre_archivo, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f, delimiter=";")
            # Datos de la gramática
            writer.writerow(["Gramática", self.gramatica.nombre])
            writer.writerow(["Símbolo inicial", self.gramatica.simbolo_inicial])
            writer.writerow(["No terminales", ", ".join(self.gramatica.no_terminales)])
            writer.writerow(["Terminales", ", ".join(self.gramatica.terminales)])
            writer.writerow(["Producciones"])
            for nt, prods in self.gramatica.producciones.items():
                for prod in prods:
                    writer.writerow(["", f"{nt} -> {' '.join(prod)}"])
            writer.writerow([])
            # Primeros y Siguientes
            writer.writerow(["No Terminal", "PRIMEROS", "SIGUIENTES"])
            writer.writerows(filas_ps)
            writer.writerow([])
            # Predicción
            writer.writerow(["Regla", "Conjunto de Prediccion"])
            writer.writerows(filas_pred)
        print(f"Exportado: {nombre_archivo}")
 
    def __str__(self, tabla=False):
        print(self.gramatica)
        if tabla:
            filas_ps, filas_pred = self._construir_tablas()
            t1 = tabulate(filas_ps,   headers=["No Terminal", "PRIMEROS", "SIGUIENTES"], tablefmt="fancy_grid")
            t2 = tabulate(filas_pred, headers=["Regla", "Conjunto de Prediccion"],       tablefmt="fancy_grid")
            return f"\n{t1}\n\n{t2}"
        else:
            return f"PRIMEROS: {self.PRIMEROS}\nSIGUIENTES: {self.SIGUIENTES}\nPREDICCION: {self.PREDICCION}"

def main_archivo():
    if len(sys.argv) < 2:
        return -1
    for arg in sys.argv[1:]:
        nombre_archivo = arg
        with open(nombre_archivo, "r", encoding="utf-8-sig") as f:
            lineas = [linea.strip() for linea in f if linea.strip()]
        nombre = lineas[0]
        n = int(lineas[1])
        terminales = []
        no_terminales = []
        simbolo_inicial = ""
        producciones = {}
        for i in range(2, 2 + n):
            regla = lineas[i]
            no_terminal, produccion = regla.split("->")
            no_terminal = no_terminal.strip()
            produccion = produccion.strip().split()
            if i == 2:
                simbolo_inicial = no_terminal
            if no_terminal not in no_terminales:
                no_terminales.append(no_terminal)
                producciones[no_terminal] = []
            producciones[no_terminal].append(produccion)
            for simbolo in produccion:
                if simbolo.islower() or simbolo.isdigit() or simbolo in "+-*/":
                    if simbolo not in terminales:
                        terminales.append(simbolo)
        gramatica1 = gramatica(nombre, terminales, no_terminales, simbolo_inicial, producciones)
        psp1 = psp(gramatica1)
        psp1.calcular_PRIMEROS()
        psp1.calcular_SIGUIENTES()
        psp1.calcular_PREDICCION()
        print(psp1.__str__(tabla=True))
        psp1.exportar_csv()

def main_interactivo():
    print("Ingrese el nombre de la gramática")
    nombre = input()
    print("Ingrese el número de reglas de la gramática")
    n=int(input())
    terminales=[]
    no_terminales=[]
    simbolo_inicial=""
    producciones={}
    for i in range(n):
        regla = input()
        no_terminal, produccion = regla.split("->")
        no_terminal = no_terminal.strip()
        produccion = produccion.strip().split()
        if i==0:
            simbolo_inicial=no_terminal
        if no_terminal not in no_terminales:
            no_terminales.append(no_terminal)
            producciones[no_terminal] = []
        producciones[no_terminal].append(produccion)
        for simbolo in produccion:
            if simbolo.islower() or simbolo.isdigit() or simbolo in "+-*/":
                if simbolo not in terminales:
                    terminales.append(simbolo)
    gramatica1 = gramatica(nombre, terminales, no_terminales, simbolo_inicial, producciones)
    psp1 = psp(gramatica1)
    psp1.calcular_PRIMEROS()
    psp1.calcular_SIGUIENTES()
    psp1.calcular_PREDICCION()
    print(psp1.__str__(tabla=True))
    psp1.exportar_csv()

if __name__ == "__main__":
    while True:
        try:
            if main_archivo() == -1:
                main_interactivo()
            else:
                main_archivo()
                break
        except ValueError:
            print("PROGRAMA FINALIZADO")
            break

