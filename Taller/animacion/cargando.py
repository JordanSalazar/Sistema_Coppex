import time
import sys
import threading

class anima:

    # Función para mostrar la animación de "cargando"
    def mostrar_cargando(self, stop_event, texto):
        while not stop_event.is_set():
            for i in range(4):
                if stop_event.is_set():
                    break
                sys.stdout.write(f'\r{texto}' + '.' * i + ' ' * (3 - i))
                sys.stdout.flush()
                time.sleep(0.5)
        sys.stdout.write('\r' + ' ' * 20 + '\r')  # Limpiar la línea después de detener la animación
        sys.stdout.flush()

    # Función principal que ejecuta una tarea simulada y usa la animación de "cargando"
    def iniciar_animacion(self, texto):
        stop_event = threading.Event()
        animacion_thread = threading.Thread(target=self.mostrar_cargando, args=(stop_event, texto))
        animacion_thread.start()
        
        try:
            time.sleep(5) 
        finally:
            stop_event.set()
            animacion_thread.join()

