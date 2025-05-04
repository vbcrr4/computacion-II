🧩 SECCIÓN 1: ¿Qué son los FIFOs (Named Pipes)?
🧠 Teoría
Un FIFO (First In, First Out) o pipe con nombre es un tipo especial de archivo que permite la comunicación entre procesos. A diferencia de los pipes anónimos (os.pipe()), los FIFOs persisten en el sistema de archivos y pueden ser abiertos por procesos no emparentados.

🔑 Características clave:

Se crean con mkfifo (desde Bash) o os.mkfifo() (desde Python).

Aparecen como archivos especiales en el sistema (ls -l los muestra con una p).

Son bloqueantes por defecto: si un proceso intenta leer y no hay escritor, se bloquea (y viceversa).

Cada proceso tiene su propio descriptor de archivo, por lo que el cursor de lectura no se comparte entre procesos.

🛠️ Práctica: Crear y usar un FIFO desde la terminal
Abrí una terminal.

Creá un FIFO:

bash
Copiar
Editar
mkfifo mi_fifo
En una terminal, escribí en el FIFO:

bash
Copiar
Editar
echo "Hola desde el proceso A" > mi_fifo
En otra terminal, leé desde el FIFO:

bash
Copiar
Editar
cat < mi_fifo
El mensaje se transfiere. ¡Eso es una FIFO en acción!

⏸️ Pausa para puesta en común
📌 Antes de seguir, respondé estas preguntas:

¿En qué se diferencia un FIFO de un pipe anónimo?

¿Por qué decimos que un FIFO es “bloqueante” por defecto?

¿Qué pasa si tratás de leer un FIFO sin que nadie escriba?

👉 Compartí estas respuestas con tu profesor o compañeros.
✅ Correcto. A diferencia de los pipes anónimos, los FIFOs están disponibles en el sistema de archivos, lo que permite que procesos completamente independientes los usen para comunicarse.

✅ Sí. Este comportamiento bloqueante es parte del diseño: evita que un proceso continúe si no hay nadie al otro lado.

✅ Exactamente. El proceso queda bloqueado esperando que haya datos disponibles (o que alguien lo escriba).
--
🧩 SECCIÓN 2: Crear y usar FIFOs en Python
🧠 Teoría
En Python, podés crear y trabajar con FIFOs utilizando el módulo os. Algunos conceptos clave:

os.mkfifo(path): crea el FIFO en el sistema de archivos.

open(path, mode): se usa como con un archivo común, pero funciona de forma bloqueante si no hay proceso del otro lado.

Los modos más comunes:

'w' o 'wb': escritura (espera a que alguien abra para lectura).

'r' o 'rb': lectura (espera a que alguien abra para escritura).

🛠️ Práctica: Ejemplo básico en Python
Vamos a crear dos scripts: uno para escribir y otro para leer.

📄 escritor.py
python
Copiar
Editar
import os
import time

fifo_path = 'canal_fifo'

if not os.path.exists(fifo_path):
    os.mkfifo(fifo_path)

with open(fifo_path, 'w') as fifo:
    print("Escribiendo mensaje...")
    fifo.write("Hola lector\n")
    print("Mensaje enviado.")
📄 lector.py
python
Copiar
Editar
import os

fifo_path = 'canal_fifo'

with open(fifo_path, 'r') as fifo:
    print("Esperando mensaje...")
    mensaje = fifo.readline()
    print(f"Mensaje recibido: {mensaje}")
▶️ Instrucciones para ejecutar
Abrí dos terminales.

En la primera, ejecutá el lector:

bash
Copiar
Editar
python3 lector.py
En la segunda, ejecutá el escritor:

bash
Copiar
Editar
python3 escritor.py
Deberías ver el mensaje en la terminal del lector.

⏸️ Pausa para puesta en común
📌 Respondé estas preguntas antes de continuar:

¿Qué pasa si corrés primero el escritor y no hay lector todavía?

¿Qué función se usa en Python para crear un FIFO?

¿Por qué el with open(..., 'r') se bloquea si no hay escritor?
✅ Correcto. Si ejecutás el escritor antes de que haya un lector, se bloquea esperando que alguien abra el FIFO para lectura.

✅ Casi! Es cierto que se usa el módulo os, pero lo más específico sería:
🔍 La función exacta es os.mkfifo(path).
(Lo tuyo está bien para una respuesta oral, pero en el código es clave mencionar la función.)

✅ Exactamente. El open(..., 'r') se bloquea porque no hay nada del otro lado para leer, y los FIFOs no pueden leer “vacío” si no hay escritor.
🧩 SECCIÓN 3: Dos procesos leyendo el mismo FIFO (cursor independiente)
🧠 Teoría
En los FIFOs, cada proceso tiene su propio descriptor de archivo, por lo tanto:

El cursor de lectura no es compartido.

Si dos procesos leen el mismo FIFO al mismo tiempo, uno de ellos lee primero, el otro espera el siguiente mensaje.

No hay duplicación de datos, y no comparten posición del cursor.

Esto es importante para entender cómo se comporta un FIFO con múltiples lectores.

🛠️ Práctica: Múltiples lectores
📄 escritor_multi.py
python
Copiar
Editar
import os
import time

fifo_path = 'multi_fifo'

if not os.path.exists(fifo_path):
    os.mkfifo(fifo_path)

with open(fifo_path, 'w') as fifo:
    for i in range(3):
        mensaje = f"Mensaje {i + 1}\n"
        print(f"Enviando: {mensaje.strip()}")
        fifo.write(mensaje)
        fifo.flush()
        time.sleep(1)  # Simula mensajes separados
📄 lector_a.py
python
Copiar
Editar
import os

fifo_path = 'multi_fifo'

with open(fifo_path, 'r') as fifo:
    for _ in range(2):
        mensaje = fifo.readline()
        print(f"[Lector A] Recibido: {mensaje.strip()}")
📄 lector_b.py
python
Copiar
Editar
import os

fifo_path = 'multi_fifo'

with open(fifo_path, 'r') as fifo:
    for _ in range(2):
        mensaje = fifo.readline()
        print(f"[Lector B] Recibido: {mensaje.strip()}")
▶️ Cómo probarlo
Abrí tres terminales.

En dos de ellas, ejecutá lector_a.py y lector_b.py al mismo tiempo (lo más rápido que puedas).

En la tercera, ejecutá escritor_multi.py.

🔍 Observá cómo los lectores reciben mensajes diferentes, y no comparten el cursor.

⏸️ Pausa para puesta en común
📌 Preguntas de comprensión:

¿Por qué no reciben el mismo mensaje los dos lectores?

¿Qué demuestra este comportamiento sobre los descriptores de archivo?

¿Qué pasaría si agregás un tercer lector al mismo FIFO?
No exactamente. El hecho de que el mensaje diga "Mensaje {i+1}" no es la causa principal de que cada lector reciba mensajes distintos.
👉 La razón real: cada proceso que lee del FIFO obtiene su propio descriptor, y los datos que lee se consumen del FIFO. Por eso, si un lector lee un mensaje, el otro ya no lo verá.

✅ Correcto. Lo que observamos es que los lectores no comparten cursor. No es como un archivo donde dos procesos pueden leer desde la misma posición: en FIFOs, cada uno avanza por separado.

✅ Sí, funcionaría igual. Si agregás un tercer lector, también se le asignará su propio descriptor de lectura, y los mensajes se seguirán distribuyendo de manera secuencial (quien llegue primero, lee primero).
--
🧩 SECCIÓN 4: Chat bidireccional con FIFOs
🧠 Teoría
Para simular un chat entre dos procesos, necesitamos:

Un FIFO para los mensajes que van de A → B.

Otro FIFO para los mensajes que van de B → A.

Esto se llama canal bidireccional. Como los FIFOs son unidireccionales por diseño, debemos usar dos.

🛠️ Práctica: Chat entre dos usuarios
Usaremos los siguientes archivos:

fifo_A_B: para mensajes de A → B

fifo_B_A: para mensajes de B → A

📄 chat_usuario_a.py
python
Copiar
Editar
import os
import threading

fifo_ab = 'fifo_A_B'
fifo_ba = 'fifo_B_A'

for fifo in [fifo_ab, fifo_ba]:
    if not os.path.exists(fifo):
        os.mkfifo(fifo)

def recibir():
    with open(fifo_ba, 'r') as fifo:
        while True:
            mensaje = fifo.readline()
            if mensaje:
                print(f"[B → A] {mensaje.strip()}")

def enviar():
    with open(fifo_ab, 'w') as fifo:
        while True:
            mensaje = input("[A → B] > ")
            fifo.write(mensaje + '\n')
            fifo.flush()

threading.Thread(target=recibir, daemon=True).start()
enviar()
📄 chat_usuario_b.py
python
Copiar
Editar
import os
import threading

fifo_ab = 'fifo_A_B'
fifo_ba = 'fifo_B_A'

for fifo in [fifo_ab, fifo_ba]:
    if not os.path.exists(fifo):
        os.mkfifo(fifo)

def recibir():
    with open(fifo_ab, 'r') as fifo:
        while True:
            mensaje = fifo.readline()
            if mensaje:
                print(f"[A → B] {mensaje.strip()}")

def enviar():
    with open(fifo_ba, 'w') as fifo:
        while True:
            mensaje = input("[B → A] > ")
            fifo.write(mensaje + '\n')
            fifo.flush()

threading.Thread(target=recibir, daemon=True).start()
enviar()
▶️ Cómo probarlo
Abrí dos terminales.

En una, ejecutá:

bash
Copiar
Editar
python3 chat_usuario_a.py
En la otra, ejecutá:

bash
Copiar
Editar
python3 chat_usuario_b.py
Probá enviar mensajes entre ambos usuarios.

⏸️ Pausa final de comprensión
📌 Preguntas para repasar:

¿Por qué usamos dos FIFOs en este chat?

¿Qué función permite que el usuario escriba sin bloquear la lectura?

¿Qué pasaría si se intenta abrir un FIFO para escritura y no hay lector?
--
✔ Correcto. Usamos dos FIFOs porque los FIFOs son unidireccionales, y en un chat necesitamos comunicación en ambos sentidos.
👉 Entonces: fifo_A_B sirve para A → B, y fifo_B_A para B → A.

⚠️ Casi, pero no del todo claro.
La respuesta esperada era:
👉 Usamos threading en Python para poder leer en paralelo mientras el usuario escribe.

La función input() bloquea la terminal, por eso usamos un hilo separado para recibir().

✔ Correcto. Si un proceso intenta abrir un FIFO para escritura y no hay lector, se bloquea hasta que alguien lo abra para lectura.
(Esto evita escribir datos que nadie va a consumir.)
--
🧩 SECCIÓN 5: Logger centralizado con FIFO
🧠 Teoría
Este patrón se usa en muchos sistemas reales:

Varios procesos productores (apps, scripts, servicios) escriben mensajes a un FIFO.

Un proceso consumidor (el logger) lee los mensajes y los guarda en un archivo de log.

🔍 Lo importante acá es:

Muchos escritores pueden usar el mismo FIFO.

El lector único consume todo lo que se escribe, y el FIFO se vacía.

Los escritores no tienen que estar ejecutándose al mismo tiempo que el lector, pero si escriben sin lector presente, el proceso se bloquea.

🛠️ Práctica: Logger y escritores
📄 logger.py
python
Copiar
Editar
import os

fifo_path = 'log_fifo'

if not os.path.exists(fifo_path):
    os.mkfifo(fifo_path)

with open(fifo_path, 'r') as fifo, open('registro.log', 'a') as log_file:
    print("Logger iniciado. Esperando mensajes...")
    while True:
        mensaje = fifo.readline()
        if mensaje:
            log_file.write(mensaje)
            log_file.flush()
            print(f"[LOG] {mensaje.strip()}")
📄 escritor_log.py
python
Copiar
Editar
import os
import sys

fifo_path = 'log_fifo'

if not os.path.exists(fifo_path):
    print("FIFO no encontrada. Asegurate de que el logger esté corriendo.")
    sys.exit(1)

with open(fifo_path, 'w') as fifo:
    mensaje = input("Mensaje a loguear: ")
    fifo.write(mensaje + '\n')
    fifo.flush()
    print("Mensaje enviado.")
▶️ Cómo probarlo
Ejecutá logger.py en una terminal.

En otra terminal, corré escritor_log.py varias veces.

Verificá que:

Los mensajes aparecen en pantalla en el logger.

Se escriben en el archivo registro.log.

⏸️ Pausa de puesta en común
📌 Preguntas de comprensión:

¿Qué pasaría si ejecutás el escritor sin que el logger esté corriendo?

¿Cuántos procesos pueden escribir al FIFO al mismo tiempo?

¿Qué ventaja tiene este sistema sobre escribir directamente a un archivo desde cada proceso?
✔ Correcto y bien expresado.
Si no hay lector presente, el escritor se bloquea al intentar abrir el FIFO para escritura. Esto evita perder mensajes que nadie procesaría.

✔ Correcto.
El FIFO puede tener múltiples procesos escribiendo. Internamente, el sistema operativo garantiza que cada write() es atómica si no supera PIPE_BUF (~4 KB en la mayoría de sistemas), por lo que no se mezclan.

⚠️ Correcto, pero incompleto.
La ventaja principal de usar un FIFO con un logger centralizado, en lugar de escribir directamente desde cada proceso, es:

Evitar conflictos de concurrencia sobre el archivo (problemas de acceso simultáneo).

Permitir centralizar el formato, timestamp y lógica de logeo.

El archivo solo lo escribe un proceso, lo que mejora la integridad y coherencia del log.
--
🧩 SECCIÓN 6: Varios productores, un consumidor con FIFO
🧠 Teoría
Este patrón se usa para modelar un sistema productor-consumidor, donde:

Productores generan mensajes (ej.: sensores, usuarios, tareas).

Un consumidor los procesa (ej.: servicio, logger, monitor).

👉 En este caso:

Todos los productores escriben en un mismo FIFO.

El consumidor lee de ese FIFO y muestra el contenido.

🔍 Este patrón permite:

Aislar responsabilidades (producir vs. procesar).

Simular una cola básica de mensajes.

🛠️ Práctica: Productores múltiples
📄 consumidor.py
python
Copiar
Editar
import os

fifo_path = 'cola_fifo'

if not os.path.exists(fifo_path):
    os.mkfifo(fifo_path)

print("Consumidor esperando mensajes...\n")

with open(fifo_path, 'r') as fifo:
    while True:
        mensaje = fifo.readline()
        if mensaje:
            print(f"[CONSUMIDOR] Recibido: {mensaje.strip()}")
📄 productor.py
python
Copiar
Editar
import os
import sys
import time
import random

fifo_path = 'cola_fifo'

if not os.path.exists(fifo_path):
    print("FIFO no encontrada. Asegurate de que el consumidor esté corriendo.")
    sys.exit(1)

nombres = ['SensorA', 'SensorB', 'ProcesoX', 'App1', 'ScriptZ']
nombre = random.choice(nombres)

with open(fifo_path, 'w') as fifo:
    for i in range(5):
        mensaje = f"{nombre}: evento #{i+1}"
        fifo.write(mensaje + '\n')
        fifo.flush()
        time.sleep(random.uniform(0.5, 1.5))

print(f"[{nombre}] Terminó de enviar.")
▶️ Cómo probarlo
Ejecutá el consumidor:

bash
Copiar
Editar
python3 consumidor.py
En otras 2 o 3 terminales, ejecutá varias veces:

bash
Copiar
Editar
python3 productor.py
📌 Observá cómo los mensajes llegan mezclados pero bien formateados, sin solaparse.

⏸️ Última pausa de puesta en común
📌 Preguntas finales de comprensión:

¿Qué garantiza que los mensajes no se mezclen en el FIFO?

¿Qué pasaría si dos productores escriben mensajes muy grandes al mismo tiempo?

¿Cómo podrías hacer que el consumidor también registre los mensajes en un archivo?
¿Qué garantiza que los mensajes no se mezclen en el FIFO?

👉 El sistema operativo garantiza que cada write() menor o igual a PIPE_BUF (normalmente 4096 bytes) es atómico.
Esto significa que si cada productor escribe menos de ese tamaño en una sola llamada a write(), los mensajes no se intercalan ni se mezclan.

¿Qué pasaría si dos productores escriben mensajes muy grandes al mismo tiempo?

👉 Si los mensajes superan PIPE_BUF, ya no se garantiza atomicidad.
Eso significa que el FIFO puede intercalar partes de un mensaje con partes de otro, produciendo resultados corruptos o mezclados.

Solución: usar mensajes pequeños o implementar delimitadores y parsing en el consumidor.

¿Cómo podrías hacer que el consumidor también registre los mensajes en un archivo?

👉 Modificando consumidor.py para abrir un archivo en modo append ('a') y escribir cada mensaje que recibe:

python
Copiar
Editar
with open('log_mensajes.txt', 'a') as archivo_log:
    archivo_log.write(mensaje)
    archivo_log.flush()
De esa forma, además de imprimir los mensajes, también los guarda.
