import signal
import time
def timeout(signum, frame):
    print("\n⏰ ¡Demoraste demasiado!")
    exit(1)

signal.signal(signal.SIGALRM, timeout)
signal.alarm(10)  # 10 segundos para responder

respuesta = input("¿Cuál es la capital de Francia? (tenés 10 segundos): ")
signal.alarm(0)  # Cancelar alarma si respondió a tiempo

print(f"Tu respuesta fue: {respuesta}")