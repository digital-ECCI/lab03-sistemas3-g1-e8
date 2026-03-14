import matplotlib.pyplot as plt
import time
import random
import subprocess

class MonitorVariables:
    def __init__(self, duracion_max=60, intervalo=0.5):
        self.duracion_max = duracion_max
        self.intervalo = intervalo
        self.tiempos = []
        self.temperaturas = []
        self.datos = []
        self.inicio = time.time()

        plt.ion()
        self.fig, self.ax = plt.subplots()

    def datos_aleatorios(self):
        try: 
            valor = random.uniform(35,50)
            return float(valor)
        except Exception as e:
            print("Error leyendo temperatura:", e)
            return None
        
    def leer_temperatura(self):
        try:
            salida = subprocess.check_output(["vcgencmd", "measure_temp"]).decode("utf-8")
            temp_str = salida.strip().replace("temp=", "").replace("'C", "")
            return float(temp_str)
        except Exception as e:
            print("Error leyendo temperatura:", e)
            return None

    def actualizar_datos(self):
        ahora = time.time() - self.inicio
        dato = self.datos_aleatorios()
        temp = self.leer_temperatura()
        if dato is not None:
            self.tiempos.append(ahora)
            self.datos.append(dato)
            self.temperaturas.append(temp)

            while self.tiempos and self.tiempos[0] < ahora - self.duracion_max:
                self.tiempos.pop(0)
                self.temperaturas.pop(0)

    def graficarDatos(self):
        self.ax.clear()
        self.ax.plot(self.tiempos, self.datos, color='red')
        self.ax.plot(self.tiempos, self.temperaturas, color='green')
        self.ax.set_title("Datos aleatorios y temperatura:")
        self.ax.set_xlabel("Tiempo transcurrido (s)")
        self.ax.set_ylabel("Variable (#)")
        self.ax.grid(True)
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    def ejecutar(self):
        try:
            while plt.fignum_exists(self.fig.number):
                self.actualizar_datos()
                self.graficarDatos()
                time.sleep(self.intervalo)

        except KeyboardInterrupt:
            print("Monitoreo interrumpido por el usuario.")

        finally:
            print("Monitoreo finalizado.")
            plt.ioff()
            plt.close(self.fig)


if __name__ == "__main__":
    monitor = MonitorVariables()
    monitor.ejecutar()