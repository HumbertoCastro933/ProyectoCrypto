# ProyectoCrypto
# Proyecto Singularity Cipher

## Descripción
Implementacion de un algoritmo de cifrado por bloques tipo Feistel con funciones de caos (Singularity).

## Estructura
- `src/`: Codigo fuente.
- `sandbox/`: Directorio seguro para archivos de entrada/salida.
- `escrow/`: Almacenamiento de claves cifradas.

## Instalación
No requiere librerias externas (solo Python 3.8+).

## Uso

1. **Inicializar (Crear claves)**
   `python src/main.py init`

2. **Cifrar un archivo**
   (Colocar archivo en `sandbox/`)
   `python src/main.py encrypt secreto.txt secreto.enc`

3. **Descifrar un archivo**
   `python src/main.py decrypt secreto.enc recuperado.txt`

4. **Ver Métricas (Entropía/Avalancha)**
   `python src/main.py analyze secreto.txt`

5. **Correr Pruebas**
   `python src/main.py test`