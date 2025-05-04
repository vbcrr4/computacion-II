✅ Tema 1: ¿Qué son las señales y por qué son importantes?
1. 📘 Explicación teórica
Las señales son un mecanismo de comunicación entre procesos (IPC, Inter-Process Communication) utilizado por los sistemas operativos Unix y POSIX. Permiten que un proceso (o el kernel) notifique a otro sobre un evento asincrónico.

📌 Características clave:
Asincronía: se envían en cualquier momento, incluso mientras el proceso está ejecutando otra cosa.

Ligereza: no requieren canales dedicados como pipes o sockets.

Interruptivas: pueden interrumpir el flujo normal del programa para ejecutar un manejador específico.

Limitadas: el número de señales estándar es pequeño y definido por el sistema.

📚 Analogía:
Pensá en las señales como una campanita de alerta. Si un proceso recibe SIGINT, es como si alguien tocara la campanita para decir “¡Interrumpí lo que estás haciendo!”.

2. 📐 Tipos de señales
Tipo	Descripción	Ejemplo
Síncronas	Generadas por el propio proceso, usualmente por errores	División por cero (SIGFPE), acceso inválido (SIGSEGV)
Asíncronas	Generadas desde otros procesos o el kernel	SIGINT por Ctrl+C, SIGTERM para terminar
Tiempo real (reales)	Introducidas en POSIX.1b. Permiten colas y datos	SIGRTMIN + n

Nota: Las señales de tiempo real se verán más adelante. Por ahora, nos enfocamos en las estándar.

3. 🔧 Instrucciones prácticas paso a paso
1. Abrí una terminal.
2. Ejecutá el comando:
bash
Copiar
Editar
kill -l
Eso lista todas las señales disponibles en tu sistema.

3. Ejecutá un proceso como:
bash
Copiar
Editar
sleep 1000
Dejalo corriendo, y en otra terminal buscá su PID:

bash
Copiar
Editar
ps aux | grep sleep
4. Enviá una señal:
bash
Copiar
Editar
kill -SIGINT <PID>
Esto simula que el usuario presionó Ctrl+C.

4. 🧪 Ejemplo básico en Python
python
Copiar
Editar
import os
import signal
import time

def handler(signum, frame):
    print(f"Recibida la señal: {signum}")

# Asociar SIGINT (Ctrl+C) al manejador
signal.signal(signal.SIGINT, handler)

print(f"PID del proceso: {os.getpid()}")
print("Esperando señales... (presioná Ctrl+C para probar)")
while True:
    time.sleep(1)
5. 🧠 Ejercicios prácticos
🟢 Básico
Ejecutá el código anterior y enviale señales con kill desde otra terminal.

Observá qué ocurre si presionás Ctrl+\ (SIGQUIT) en vez de Ctrl+C.

🟡 Medio
Modificá el handler para que ignore las primeras dos señales y recién en la tercera termine el proceso.

🔴 Avanzado
Usá signal.SIGUSR1 para comunicar entre dos procesos de Python (con os.fork() si sabés usarlo, o subprocess).

⏸️ Pausa para puesta en común
Antes de avanzar, hacé una pausa para compartir con la clase y tu profesor lo siguiente:

¿Lograste enviar y recibir señales entre terminales?

¿Probaste capturar SIGINT en tu código Python?

❓ Preguntas de comprensión
¿Qué diferencias hay entre señales síncronas y asíncronas?

¿Por qué las señales se consideran un mecanismo de comunicación asincrónico?

¿Cuál es el efecto de asociar un manejador con signal.signal()?

📌 Recordatorio: compartí tu código y observaciones con tu profesor antes de continuar.
Correcto, con un pequeño refinamiento:

Las síncronas ocurren como consecuencia directa de una instrucción que ejecuta el propio proceso (como una división por cero o una violación de segmento).

Las asíncronas llegan “desde afuera”, en cualquier momento, como cuando otro proceso usa kill() o el usuario presiona Ctrl+C.

Bien explicado:

Las señales son asincrónicas porque pueden interrumpir la ejecución del proceso en cualquier momento, sin necesidad de que el proceso lo espere o lo provoque.

Casi perfecto, pero importante aclarar:

Al asociar un manejador con signal.signal(SIGINT, handler), le estás diciendo al proceso: "Cuando recibas SIGINT (por ejemplo, al presionar Ctrl+C), no te mueras directamente, sino que ejecutá esta función (handler) primero."

Esto no termina el proceso automáticamente, a menos que lo programes así en el manejador.
--
🔹 Tema 2: signal.signal() y funciones relacionadas en Python
¿Querés que avancemos con este tema ahora?







Dijiste:
avancemos


ChatGPT dijo:
Perfecto. Vamos con el segundo tema:

🔹 Tema 2: signal.signal() y funciones relacionadas en Python
1. 📘 Explicación teórica
Python, en sistemas tipo UNIX (como Linux o macOS), provee un módulo llamado signal que permite registrar funciones (handlers) para manejar señales específicas. Es una interfaz de alto nivel para trabajar con señales POSIX.

Las funciones más importantes son:
Función	Descripción
signal.signal(sig, handler)	Asocia una señal (sig) a un manejador (handler)
signal.getsignal(sig)	Consulta el manejador actual para una señal
signal.pause()	Suspende el proceso hasta que reciba una señal
signal.raise_signal(sig)	Envía una señal al proceso actual
os.kill(pid, sig)	Envía una señal al proceso con ID pid

2. 🔧 Instrucciones prácticas paso a paso
1. Abrí un archivo signal_demo.py.
2. Escribí este ejemplo base:
python
Copiar
Editar
import signal
import os
import time

def mi_manejador(signum, frame):
    print(f"Señal recibida: {signum}")

# Asociar SIGINT (Ctrl+C) a nuestro manejador
signal.signal(signal.SIGINT, mi_manejador)

print(f"PID: {os.getpid()}")
print("Esperando señales (Ctrl+C para probar)...")

# Loop infinito con pausa
while True:
    signal.pause()  # Espera una señal
3. Ejecutá el script y probá presionar Ctrl+C.
Debería imprimir el mensaje del manejador, pero no terminar el proceso.

4. Abrí otra terminal y ejecutá:
bash
Copiar
Editar
kill -SIGTERM <PID>
Como no registramos un handler para SIGTERM, el proceso termina por defecto.

3. 🧪 Código explicado y expandido
python
Copiar
Editar
import signal
import os
import time

def manejador(signum, frame):
    print(f"Recibí la señal {signum}, pero sigo ejecutando...")

# Asociamos SIGUSR1 (señal de usuario) a nuestro manejador
signal.signal(signal.SIGUSR1, manejador)

pid = os.getpid()
print(f"PID del proceso: {pid}")
print("Esperando SIGUSR1 (usá 'kill -SIGUSR1 {pid}')")

while True:
    time.sleep(1)
4. 🧪 Ejercicio adicional (nivel medio)
🔸 Objetivo: Ignorar SIGINT la primera vez y terminar al segundo intento.

python
Copiar
Editar
import signal
import os

contador = 0

def handler(signum, frame):
    global contador
    contador += 1
    if contador == 1:
        print("SIGINT ignorado una vez.")
    else:
        print("Segunda vez: terminando.")
        exit(0)

signal.signal(signal.SIGINT, handler)

print(f"PID: {os.getpid()}")
while True:
    signal.pause()
⏸️ Pausa para puesta en común
Antes de continuar, compartí tu código y resultados con tu profesor y compañeros.

❓ Preguntas de comprensión
¿Qué hace exactamente signal.signal() y qué tipo de argumento espera?

¿Cuál es la diferencia entre signal.pause() y time.sleep()?

¿Por qué usar os.kill() para enviar señales entre procesos?

📌 Recordatorio: compartí tu código y explicaciones antes de seguir al siguiente tema.
1. asocia signt y al apretar ctrl + c imprime un mensaje, pero no termina el proceso
2. signal.pause espera una senal y time.sleep no espera una senal sino que queda en sleep por un tiempo determinado
3. 	Envía una señal al proceso con ID pid
--
🔹 Tema 3: kill, sigqueue y sigaction (con referencia a C si es útil)
1. 📘 Explicación teórica
Aunque en Python no trabajamos directamente con sigqueue() ni sigaction(), es útil conocerlos porque forman parte del funcionamiento interno del sistema operativo.

🛠️ kill(pid, sig) — desde C y Python
Es la función más simple para enviar señales.

En Python usamos os.kill(pid, signal).

c
Copiar
Editar
// En C
kill(pid, SIGTERM);
python
Copiar
Editar
# En Python
import os, signal
os.kill(12345, signal.SIGUSR1)
📬 sigqueue(pid, sig, union sigval val) — solo en C
Permite enviar señales con datos (solo con señales en tiempo real).

Python estándar no expone sigqueue directamente.

⚙️ sigaction() — manejo avanzado en C
Sustituye a signal() con más control.

Permite bloquear señales durante la ejecución del handler y recibir información más detallada (siginfo_t).

2. 🔧 Instrucciones prácticas con os.kill() en Python
1. Abrí dos terminales.
2. En la primera, creá un script receptor:
python
Copiar
Editar
# receptor.py
import signal
import os
import time

def handler(signum, frame):
    print(f"[Receptor] Señal recibida: {signum}")

signal.signal(signal.SIGUSR1, handler)

print(f"[Receptor] Esperando señales... PID: {os.getpid()}")
while True:
    time.sleep(1)
3. En otra terminal, creá un script emisor:
python
Copiar
Editar
# emisor.py
import os
import signal
import sys

if len(sys.argv) != 2:
    print("Uso: python emisor.py <PID>")
    exit(1)

pid = int(sys.argv[1])
print(f"[Emisor] Enviando SIGUSR1 a PID {pid}")
os.kill(pid, signal.SIGUSR1)
4. Ejecutá receptor.py y tomá nota del PID.
5. Desde otra terminal, ejecutá:
bash
Copiar
Editar
python emisor.py <PID_DEL_RECEPTOR>
📌 Eso simula cómo un proceso envía una señal a otro con kill.

3. 🧪 Ejercicio práctico medio
Modificá el receptor para que cuente cuántas señales ha recibido y termine cuando reciba 5:

python
Copiar
Editar
contador = 0

def handler(signum, frame):
    global contador
    contador += 1
    print(f"Señal {contador} recibida.")
    if contador >= 5:
        print("Recibidas 5 señales. Terminando.")
        exit(0)
⏸️ Pausa para puesta en común
Ahora es buen momento para mostrarle a tu profesor los dos scripts y verificar si lograste hacer la comunicación entre procesos correctamente.

❓ Preguntas de comprensión
¿Qué diferencia hay entre os.kill() en Python y kill() en C?

¿Por qué Python no tiene sigqueue() directamente?

¿Qué ventaja tiene usar sigaction() sobre signal() en C?

📌 Compartí tus observaciones y código antes de seguir.
--
🔹 signal.alarm() — Programar señales temporizadas
1. 📘 Explicación teórica
La función signal.alarm(segundos) programa que el proceso reciba la señal SIGALRM después de esa cantidad de segundos.

Es útil para:

Implementar timeouts (tiempos límite).

Cancelar procesos que tardan demasiado.

Crear sistemas de vigilancia (watchdog).

🧠 Importante: alarm() solo se puede usar una vez a la vez por proceso.

2. 🔧 Instrucciones paso a paso
Paso 1: Crear un manejador para SIGALRM
python
Copiar
Editar
import signal
import time

def alarma_handler(signum, frame):
    print("¡Se acabó el tiempo!")

signal.signal(signal.SIGALRM, alarma_handler)
Paso 2: Programar la alarma
python
Copiar
Editar
print("Esperando 5 segundos antes de recibir SIGALRM...")
signal.alarm(5)  # En 5 segundos se enviará SIGALRM

# Hacemos algo que puede demorar
try:
    while True:
        print("Trabajando...")
        time.sleep(1)
except KeyboardInterrupt:
    print("Interrumpido por el usuario.")
📌 La señal SIGALRM interrumpirá sleep() o cualquier otra operación bloqueante cuando llegue.

3. 🧪 Ejercicio práctico
🔸 Objetivo: Crear un pequeño temporizador que avise si un usuario tarda más de 10 segundos en responder.

python
Copiar
Editar
import signal

def timeout(signum, frame):
    print("\n⏰ ¡Demoraste demasiado!")
    exit(1)

signal.signal(signal.SIGALRM, timeout)
signal.alarm(10)  # 10 segundos para responder

respuesta = input("¿Cuál es la capital de Francia? (tenés 10 segundos): ")
signal.alarm(0)  # Cancelar alarma si respondió a tiempo

print(f"Tu respuesta fue: {respuesta}")
⏸️ Pausa para puesta en común
Compartí este ejercicio con tu profesor y explicá qué hace signal.alarm() y cómo interactúa con input() o sleep().

❓ Preguntas de comprensión
¿Qué hace exactamente signal.alarm(n)?
signal.alarm(n) programa una señal SIGALRM que será enviada al proceso dentro de n segundos. Si ya había una alarma programada, la reemplaza. Si pasás 0, cancela cualquier alarma pendiente.
¿Por qué necesitamos un handler para SIGALRM?
Porque sin un handler personalizado, cuando se reciba SIGALRM, el proceso terminará por defecto. Si queremos realizar una acción específica (mostrar un mensaje, interrumpir una tarea, etc.), debemos registrar un handler con signal.signal(signal.SIGALRM, handler).
¿Qué pasa si llamo signal.alarm(0)?
Se cancela cualquier alarma pendiente. No se enviará SIGALRM y el contador de alarma se reinicia. Es útil si querés anular el temporizador porque la tarea se completó antes de tiempo.
--
🔹 Tema 4: Uso de señales para sincronizar procesos
1. 📘 Explicación teórica
Las señales se pueden usar para coordinar o sincronizar procesos entre sí. Por ejemplo:

Un proceso puede notificar a otro que cierto evento ocurrió.

Podés usar señales para que un proceso “despierte” a otro.

No transportan datos (a menos que se usen señales de tiempo real), pero sí sirven para transmitir eventos o interrupciones.

Esto es útil cuando no se necesita compartir datos, solo desencadenar una acción remota (por ejemplo, que el hijo le avise al padre que terminó su trabajo).

🧠 Importante:
Las señales son asíncronas: el proceso receptor puede estar en cualquier parte de su ejecución.

El proceso debe tener definido un handler para poder reaccionar correctamente.

2. 🔧 Instrucciones paso a paso para sincronizar
Vamos a hacer un ejemplo donde:

El padre crea un hijo.

El hijo hace algo (por ejemplo, dormir unos segundos).

Al terminar, el hijo le envía una señal al padre para avisar que terminó.

👨‍👦 Código de ejemplo en Python (padre e hijo con fork)
python
Copiar
Editar
# sincronizar.py
import os
import signal
import time
import sys

# Handler que se ejecuta cuando el padre recibe SIGUSR1
def handler(signum, frame):
    print(f"[PADRE] Recibí señal {signum} del hijo. ¡Hijo terminó!")

# Registrar handler
signal.signal(signal.SIGUSR1, handler)

pid = os.fork()

if pid == 0:
    # Proceso hijo
    print("[HIJO] Haciendo trabajo...")
    time.sleep(3)
    print("[HIJO] Trabajo terminado. Enviando señal al padre...")
    os.kill(os.getppid(), signal.SIGUSR1)
    sys.exit(0)
else:
    print(f"[PADRE] Esperando señal del hijo (PID hijo: {pid})...")
    signal.pause()  # Espera activa hasta recibir señal
    print("[PADRE] Fin del programa.")
3. 🧪 Ejercicios propuestos
🟢 Nivel básico
Modificar el código anterior para que el hijo envíe la señal SIGUSR2 y el padre la maneje.

🟡 Nivel intermedio
Crear dos hijos que trabajen en paralelo y cada uno avise al padre con una señal diferente (SIGUSR1, SIGUSR2).

🔴 Nivel avanzado
Agregar un contador en el padre para que espere señales de ambos hijos y no finalice hasta que ambos hayan enviado la suya.

⏸️ Pausa para puesta en común
Mostrale este código a tu profesor y explicá en tus palabras cómo los procesos se sincronizan con señales.

❓ Preguntas de comprensión
¿Qué hace os.fork() y cómo lo usás para crear procesos relacionados?

¿Por qué usamos os.kill() en el hijo?

¿Por qué signal.pause() es útil en el padre?
1. os.fork() crea un nuevo proceso duplicando el proceso actual. Retorna 0 en el proceso hijo y el PID del hijo en el proceso padre.
2. El hijo puede usar os.kill(ppid, señal) para enviar una señal al proceso padre (por ejemplo, signal.SIGUSR1).
Esto permite sincronización: el hijo le avisa al padre que terminó o que ocurrió un evento importante.
3. signal.pause() bloquea al padre hasta que recibe una señal.
Es útil para sincronizar: el padre espera sin hacer busy waiting, y reacciona cuando el hijo le manda una señal.
--
🔹 Tema 5: Manejo seguro y funciones async-signal-safe
1. 📘 Explicación teórica
Cuando una señal llega, interrumpe lo que esté haciendo el proceso y ejecuta su handler. Este handler puede ejecutarse en medio de cualquier instrucción o syscall, lo cual es riesgoso.

⚠️ Problema:
Si dentro del handler se ejecutan funciones que no son seguras, el proceso puede quedar en un estado inconsistente (por ejemplo, un malloc() interrumpido).

🧠 ¿Qué significa async-signal-safe?
Una función es async-signal-safe si se puede invocar dentro de un handler de señal sin riesgo de corrupción.

🔒 En general:

✅ Son seguras: write(), getpid(), signal(), kill(), exit()

❌ No son seguras: printf(), malloc(), sleep(), input(), open()

📌 En Python, esto es menos crítico que en C, pero sigue siendo buena práctica mantener los handlers simples, rápidos y seguros.

2. 🔧 Buenas prácticas para handlers en Python
✔️ Hacer solo acciones mínimas:

python
Copiar
Editar
import signal
import os

def handler(signum, frame):
    os.write(1, b"¡Señal recibida!\n")  # write() es async-signal-safe
🚫 Evitá esto:

python
Copiar
Editar
def handler(signum, frame):
    print("¡Señal recibida!")  # printf en C o print en Python = no seguro
💡 En Python no suele corromper el proceso, pero puede fallar en casos extremos, como si interrumpe a input() o print() mientras están en uso.

3. 🧪 Ejercicio práctico
Reescribí el ejemplo anterior de sincronización entre procesos usando os.write() en el handler del padre, en lugar de print().

🔸 Recordá: os.write(fd, b"texto") escribe directo al descriptor de archivo.

⏸️ Pausa para puesta en común
Comentá esto con el profesor y el grupo:

¿Por qué es peligroso usar funciones comunes como print() dentro de un handler?

¿Qué alternativas existen en Python y C?

¿Por qué la función write() sí es segura?

❓ Preguntas de comprensión
¿Qué problemas puede causar usar funciones no async-signal-safe dentro de un handler?

¿Qué funciones están permitidas dentro de un handler de señal?

¿Qué ventajas tiene os.write() en comparación con print() en este contexto?
1. Usar funciones no async-signal-safe (como print(), malloc(), etc.) en un handler de señal puede causar condiciones de carrera, bloqueos o comportamiento indefinido, porque esas funciones no están garantizadas para ser seguras si se interrumpen por señales.
El handler podría ejecutarse en medio de otra llamada a esa función, rompiendo su estado interno.
2. Solo las funciones llamadas async-signal-safe, que son garantizadas por POSIX para ser seguras dentro de handlers.
3. os.write() es async-signal-safe, mientras que print() no lo es.

os.write() va directo al descriptor de archivo (como la terminal), sin pasar por buffers de Python o libc.

En un handler de señal, os.write() evita errores o bloqueos que podrían ocurrir con print().
--
🔹 Tema 6: Señales en sistemas multihilo
1. 📘 Explicación teórica
En programas con múltiples hilos de ejecución (threads), las señales se vuelven más complejas.

📌 En un proceso con varios hilos:

Las señales se envían al proceso, no a un hilo específico.

Pero solo uno de los hilos va a recibir y manejar la señal.

Esto puede generar problemas de sincronización si no está claro qué hilo manejará la señal.

🔑 Cosas importantes:
Cada hilo puede bloquear o desbloquear señales usando pthread_sigmask() (en C).

En Python, no hay control explícito de esto (por ahora).

Solo el hilo principal puede registrar y manejar señales en Python estándar (CPython).

En Python, si usás threading, los handlers deben ir siempre en el hilo principal.

🧠 ¿Por qué esto es importante?
Si tenés un programa concurrente (con hilos), debés:

Registrar señales en el hilo principal.

Usar mecanismos como Event, Queue o Pipe para comunicar desde el handler al resto de los hilos.

2. 🧪 Ejemplo simple (Python con threading)
python
Copiar
Editar
import threading
import signal
import time
import os

# Evento global para comunicación entre hilos
evento = threading.Event()

def handler(signum, frame):
    print(f"[MainThread] Señal {signum} recibida.")
    evento.set()  # avisamos al hilo

def hilo_trabajo():
    print("[Hilo] Esperando evento...")
    evento.wait()
    print("[Hilo] Señal detectada. Continuando trabajo...")

# Registro de la señal solo en el hilo principal
signal.signal(signal.SIGUSR1, handler)

# Creamos un hilo secundario
t = threading.Thread(target=hilo_trabajo)
t.start()

print(f"[MainThread] PID: {os.getpid()}")
print("[MainThread] Esperando señal (enviá con kill)...")

# Esperamos a que el hilo termine
t.join()
🔧 Desde otra terminal podés enviar la señal con:

bash
Copiar
Editar
kill -SIGUSR1 <PID>
3. 🧪 Ejercicio propuesto
🔴 Avanzado
Modificar el ejemplo para tener dos hilos esperando eventos distintos, activados por señales distintas (SIGUSR1, SIGUSR2).

⏸️ Pausa para puesta en común
Comentá con tu profesor:

¿Por qué en Python solo el hilo principal puede manejar señales?

¿Qué rol cumplen las estructuras como Event() en la comunicación?

¿Qué harías si quisieras que un hilo reaccione directamente a una señal?

❓ Preguntas de comprensión
¿Quién maneja las señales en un programa multihilo en Python?

¿Qué problema habría si varios hilos pudieran manejar señales simultáneamente?

¿Cómo se puede comunicar un handler de señal con otros hilos?
1. En Python, solo el hilo principal puede recibir y manejar señales. Esto es una restricción del intérprete de Python (CPython), no solo del sistema operativo.
2. Podría haber condiciones de carrera, comportamientos no deterministas y errores difíciles de depurar.
Ejemplo: dos hilos respondiendo a la misma señal al mismo tiempo podrían interferir entre sí, especialmente si usan recursos compartidos o funciones no thread-safe.
3. Usando mecanismos seguros como:

Variables compartidas con locks

Queues (queue.Queue)

Eventos (threading.Event)

Por ejemplo, el handler puede poner un mensaje en una Queue, y otro hilo puede leerlo y actuar en consecuencia.
--
🔹 Tema 7: Comparaciones con otros mecanismos de IPC
1. 📘 Explicación teórica
Las señales son solo una de las muchas formas de comunicación entre procesos (IPC). Vamos a compararlas brevemente con otros mecanismos:

Mecanismo	Dirección	Datos	Sincronización	Velocidad	Complejidad
Señales	1 a 1 (proceso a proceso)	No (solo número)	Sí (notificación)	Muy alta	Baja
Pipes/FIFOs	1 a 1	Sí	Implícita	Alta	Media
Sockets	1 a 1 o 1 a n	Sí	Implícita	Media	Alta
Shared memory	1 a 1 o 1 a n	Sí	No (requiere control)	Muy alta	Alta
Queues (POSIX o Python)	1 a 1 o 1 a n	Sí	Implícita	Media	Media

🧠 Entonces, ¿cuándo usar señales?
Usá señales cuando necesites:

Notificar rápidamente un evento o interrupción (ej: Ctrl+C, terminar proceso, sincronizar).

No requieras enviar datos complejos.

Tener reacción inmediata, pero con lógica mínima en el handler.

2. 🧪 Ejercicio final
Elegí un caso de uso (por ejemplo, “padre espera que el hijo termine un cálculo”) y describí dos maneras de implementarlo:

Una usando señales.

Otra usando una queue o pipe.

Compará ventajas y desventajas.

⏸️ Pausa para cierre
Comentá con tu profesor y grupo:

¿Qué lugar ocupan las señales dentro del conjunto de herramientas IPC?

¿Por qué elegirías señales en vez de una cola o pipe?

¿Qué desventajas importantes tienen las señales?

❓ Preguntas finales de comprensión
¿Qué diferencia principal hay entre una señal y un pipe?

¿Por qué las señales no permiten enviar datos complejos?

¿Qué otros mecanismos IPC usarías para enviar estructuras de datos entre procesos?
1. Una señal es una notificación simple entre procesos, como una alerta (ej: SIGUSR1), sin contenido adicional.

Un pipe es un canal de comunicación que permite enviar datos reales (bytes) entre procesos relacionados.
2. Porque las señales están diseñadas para ser ligeras, rápidas y asincrónicas.
Solo indican que algo ocurrió, sin ocupar memoria o gestionar buffers. Incluir datos complejos rompería esa simplicidad y seguridad.
3. Pipes con pickle o json para serializar estructuras.

FIFOs (named pipes) para comunicación entre procesos no relacionados.

Sockets para comunicación local o en red.

Shared memory (memoria compartida) con sincronización adecuada.

Multiprocessing.Queue en Python, que usa pipes y locks por debajo.
