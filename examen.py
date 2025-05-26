#importamos las librerias necesarias
import tkinter as tk
from tkinter import messagebox
import random
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import csv



def registro_produccion():

    ventana_registro = tk.Toplevel(ventana)
    ventana_registro.title("Registro de Producción")
    ventana_registro.geometry("400x400")
    tk.Label(ventana_registro, text="Nombre del operario:").pack(pady=5)
    entrada_nombre = tk.Entry(ventana_registro)
    entrada_nombre.pack(pady=5)
    tk.Label(ventana_registro, text="Cantidad de pan frances:").pack(pady=5)
    entrada_cantidad_frances = tk.Entry(ventana_registro)
    entrada_cantidad_frances.pack(pady=5)
    tk.Label(ventana_registro, text="Cantidad de pan de queso:").pack(pady=5)
    entrada_cantidad_queso = tk.Entry(ventana_registro)
    entrada_cantidad_queso.pack(pady=5)
    tk.Label(ventana_registro, text="Cantidad de croissant:").pack(pady=5)
    entrada_cantidad_croissant = tk.Entry(ventana_registro)
    entrada_cantidad_croissant.pack(pady=5)


    def guardar_datos():
        try:
            nombre = entrada_nombre.get().strip()
            pan_frances = int(entrada_cantidad_frances.get())
            pan_queso = int(entrada_cantidad_queso.get())
            croissant = int(entrada_cantidad_croissant.get())
            if not (0 <= pan_frances <= 500 and 0 <= pan_queso <= 500 and 0 <= croissant <= 500):
                messagebox.showerror("Error", "Las cantidades deben estar entre 0 y 500.")
                return
            
            comple_pan_frances = random.uniform(1.0, 1.5)
            comple_pan_queso = random.uniform(1.0, 1.5)
            comple_croissant = random.uniform(1.0, 1.5)


            numerador = (pan_frances * comple_pan_frances + pan_queso * comple_pan_queso + croissant * comple_croissant)
            denominador = (comple_pan_frances + comple_pan_queso + comple_croissant)
            eficiencia = round(numerador / denominador)

            estado = "cumple" if eficiencia >= 300 else "no cumple"

            with open("panes.csv", "a", newline="") as archivo:
                escritor = csv.writer(archivo)
                escritor.writerow([nombre, pan_frances, pan_queso, croissant, eficiencia, estado])
                
            messagebox.showinfo("Éxito", f"Producción registrada.\nEficiencia: {eficiencia}\nEstado: {estado}")
            ventana_registro.destroy()

        except ValueError:
            messagebox.showerror("Error", "ingrese valores válidos.")

    boton_guardar = tk.Button(ventana_registro, text="Guardar", command=guardar_datos)
    boton_guardar.pack(pady=10)

def reporte_general():

    try:
        datos = pd.read_csv("panes.csv", names=["Nombre", "Pan Frances", "Pan Queso", "Croissant", "Eficiencia", "Estado"])

        if datos.empty:
            messagebox.showinfo("Reporte General", "No hay datos registrados.")

            return
        reporte = datos[["Nombre", "Eficiencia", "Estado"]]
        texto_reporte = "Reporte General:\n\n"

        for index, fila in reporte.iterrows():
            texto_reporte += f"Nombre: {fila['Nombre']}, Eficiencia: {fila['Eficiencia']}, Estado: {fila['Estado']}\n"
        promedio_eficiencia = datos["Eficiencia"].mean()

        estadisticas = datos.describe()
        texto_reporte += f"\nPromedio de Eficiencia: {promedio_eficiencia:.2f}\n\n"
        texto_reporte += f"Estadísticas:\n{estadisticas}"
        messagebox.showinfo("Reporte General", texto_reporte)


        conteo_estado = datos["Estado"].value_counts()


        plt.figure()
        plt.pie(conteo_estado, labels=conteo_estado.index, startangle=90)
        plt.title("Cumplimiento de la Meta")
        plt.show()


        correlacion = datos[["Pan Frances", "Pan Queso", "Croissant"]].corr()


        plt.figure(figsize=(5, 4))
        sns.heatmap(correlacion, annot=True, cmap="coolwarm")
        plt.title("Matriz de Correlación entre Productos")
        plt.show()


    except FileNotFoundError:
        messagebox.showerror("Error", "No se encontraron datos registrados.")


    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")

def reporte_individual():
    def mostrar_reporte():
        nombre_buscar = entrada_nombre.get().strip()


        if not nombre_buscar:
            messagebox.showerror("Error", "Ingresa un nombre.")
            return
        
        try:
            datos = pd.read_csv("panes.csv", names=["Nombre", "Pan Frances", "Pan Queso", "Croissant", "Eficiencia", "Estado"])
            datos_operario = datos[datos["Nombre"] == nombre_buscar]


            if datos_operario.empty:
                messagebox.showinfo("Reporte Individual", f"No se encontraron datos para el operario {nombre_buscar}.")
                return
            

            eficiencia = datos_operario["Eficiencia"].values[-1]
            estado = datos_operario["Estado"].values[-1]
            texto = f"Nombre: {nombre_buscar}\nEficiencia final: {eficiencia}\nEstado: {estado}"


            messagebox.showinfo("Reporte Individual", texto)
            plt.figure()


            datos_pan = datos_operario[["Pan Frances", "Pan Queso", "Croissant"]].iloc[-1]
            datos_pan.plot(kind="bar")


            plt.title("Producción por tipo de pan")
            plt.ylabel("Unidades")
            plt.xlabel("Tipo de pan")
            plt.show()

            complejidades = {"Pan Frances": random.uniform(1.0, 1.5),"Pan Queso": random.uniform(1.0, 1.5),"Croissant": random.uniform(1.0, 1.5)}


            plt.figure()
            pd.Series(complejidades).plot(kind="bar", color="orange")
            plt.title("Complejidad aplicada por tipo de pan (aleatoria)")
            plt.ylabel("Complejidad")
            plt.xlabel("Tipo de pan")
            plt.show()


            eficiencia_ponderada = {}


            for pan, comp in complejidades.items():
                cantidad = datos_operario[pan].values[-1]
                eficiencia_ponderada[pan] = cantidad * comp

            plt.figure()
            pd.Series(eficiencia_ponderada).plot(kind="bar", color="green")
            plt.title("Eficiencia ponderada por tipo de pan")
            plt.ylabel("Eficiencia ponderada")
            plt.xlabel("Tipo de pan")
            plt.show()

        except FileNotFoundError:
            messagebox.showerror("Error", "No se encontraron datos registrados.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")

    ventana_individual = tk.Toplevel(ventana)
    ventana_individual.title("Reporte Individual")
    ventana_individual.geometry("300x150")
    tk.Label(ventana_individual, text="Nombre del operario:").pack(pady=5)
    entrada_nombre = tk.Entry(ventana_individual)
    entrada_nombre.pack(pady=5)
    tk.Button(ventana_individual, text="Mostrar Reporte", command=mostrar_reporte).pack(pady=10)

ventana = tk.Tk()
ventana.title("sistema de produccion")
ventana.geometry("500x400")
etiqueta = tk.Label(ventana, text="Bienvenido al Sistema de Producción", font=("Arial", 16))
etiqueta.pack(pady=20)


#botones
boton_registrar = tk.Button(ventana, text="1. Registrar produccion diaria", command=registro_produccion, width=35, height=2)
boton_registrar.pack(pady=10)
boton_reporte_general = tk.Button(ventana, text="2. Reporte General", command=reporte_general, width=35, height=2)
boton_reporte_general.pack(pady=10)
boton_reporte_individual = tk.Button(ventana, text="3. Reporte Individual", command=reporte_individual, width=35, height=2)
boton_reporte_individual.pack(pady=10)
boton_salir = tk.Button(ventana, text="4. Salir", command=ventana.quit, width=35, height=2)
boton_salir.pack(pady=10)


ventana.mainloop()

