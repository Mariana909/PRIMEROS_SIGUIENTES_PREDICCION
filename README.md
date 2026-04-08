# conjutos PRIMEROS, SIGUIENTES y PREDICCIÓN

Requerimiento:
Python 

Instalación dependencias:
python3 -m venv venv
source venv/bin/activate
pip install tabulate


Programa
Recibe uno o varios archivos con las gramáticas 
Descripción de entrada
Línea 1: Nombre de la gramática
Línea 2: Número de reglas
Línea 3 en adelante: Reglas de la gramática

Formato Reglas
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

Como ejecutar:
Opción 1:
Comando 
python3 psp.py
A continuación copie y pegue lo siguiente

Ejercicio 1
11
S -> A uno B C
S -> S dos
A -> B C D
A -> A tres
A -> _
B -> D cuatro C tres
B -> _
C -> cinco D B
C -> _
D -> seis
D -> _
Ejercicio 2
10
S -> A B uno
A -> dos B
A -> _
B -> C D
B -> tres
B -> _
C -> cuatro A B
C -> cinco
D -> seis
D -> _


Opción 2:
Usar comando
python3 psp.py Ejercicio1.txt Ejercicio2.txt


Salidas:
Para la primera gramática
Info sobre gramática:

<img width="462" height="311" alt="image" src="https://github.com/user-attachments/assets/7948aed4-e53e-4d4a-a408-cc7bf29d5e18" />

Conjuntos PRIMEROS, SIGUIENTES y PREDICCIÓN (Tablas)

<img width="693" height="207" alt="image" src="https://github.com/user-attachments/assets/7530ee4e-cbff-415e-9a1a-29a169934b81" />

Exportado: Ejercicio 1.csv


Para la segunda gramática
Info sobre gramática

<img width="455" height="286" alt="image" src="https://github.com/user-attachments/assets/08aefb5a-7f58-4486-b46d-17353434d18f" />

Conjuntos PRIMEROS, SIGUIENTES y PREDICCIÓN (Tablas)

<img width="715" height="208" alt="image" src="https://github.com/user-attachments/assets/0f42d099-5116-4f15-9104-0a07cc5a1e31" />

<img width="444" height="378" alt="image" src="https://github.com/user-attachments/assets/7ae9e0cf-8bc2-4238-9ce7-29a18af5c64c" />

Exportado: Ejercicio 2.csv
