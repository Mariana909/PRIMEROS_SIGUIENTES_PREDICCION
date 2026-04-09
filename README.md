# Conjuntos PRIMEROS, SIGUIENTES y PREDICCIÓN

Herramienta para calcular automáticamente los conjuntos **PRIMEROS**, **SIGUIENTES** y **PREDICCIÓN** de una gramática libre de contexto, con exportación a CSV.

---

## Requisitos

- Python 3

## Instalación

```bash
python3 -m venv venv
source venv/bin/activate
pip install tabulate
```

---

## Formato de entrada

Cada gramática se define en un archivo de texto (o por entrada interactiva) con la siguiente estructura:

| Línea | Contenido |
|-------|-----------|
| 1 | Nombre de la gramática |
| 2 | Número de reglas |
| 3+ | Reglas de la gramática |

### Convenciones

| Elemento | Representación |
|----------|---------------|
| Terminales | Minúsculas, dígitos u operadores (`+`, `-`, `*`, `/`) |
| No terminales | Mayúsculas |
| Derivación | `->` |
| Símbolo vacío | `_` |

### Ejemplo de reglas

```
A -> a B
A -> b A
A -> _
B -> a A
B -> b B
```

---

## Ejecución

### Opción 1 — Modo interactivo

```bash
python3 psp.py
```

Luego ingrese la gramática manualmente. Por ejemplo:

**Ejercicio 1**
```
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
```

**Ejercicio 2**
```
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
```

### Opción 2 — Desde archivos

```bash
python3 psp.py Ejercicio1.txt Ejercicio2.txt
```

Se pueden pasar uno o varios archivos como argumentos.

---

## Salidas

Por cada gramática procesada el programa imprime en consola:

1. **Información de la gramática** — símbolo inicial, no terminales, terminales y producciones.
2. **Tablas de PRIMEROS, SIGUIENTES y PREDICCIÓN**.
3. **Archivo CSV exportado** — con nombre igual al de la gramática (e.g. `Ejercicio 1.csv`).

### Ejercicio 1

Información de la gramática:

![Gramática Ejercicio 1](https://github.com/user-attachments/assets/7948aed4-e53e-4d4a-a408-cc7bf29d5e18)

Conjuntos PRIMEROS, SIGUIENTES y PREDICCIÓN:

![Tablas Ejercicio 1](https://github.com/user-attachments/assets/7530ee4e-cbff-415e-9a1a-29a169934b81)

```
Exportado: Ejercicio 1.csv
```

### Ejercicio 2

Información de la gramática:

![Gramática Ejercicio 2](https://github.com/user-attachments/assets/08aefb5a-7f58-4486-b46d-17353434d18f)

Conjuntos PRIMEROS, SIGUIENTES y PREDICCIÓN:

![Tablas Ejercicio 2 — parte 1](https://github.com/user-attachments/assets/0f42d099-5116-4f15-9104-0a07cc5a1e31)

![Tablas Ejercicio 2 — parte 2](https://github.com/user-attachments/assets/7ae9e0cf-8bc2-4238-9ce7-29a18af5c64c)

```
Exportado: Ejercicio 2.csv
```
