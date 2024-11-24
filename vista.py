import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
from modelo import Asignatura
import openpyxl

class VistaPrincipal(ctk.CTk):
    def __init__(self, controlador):
        super().__init__()
        self.controlador = controlador  # controlador que maneja la lógica de la aplicación

        # configuración inicial de la ventana principal
        self.title("Sistema de Gestión de Notas") 
        self.geometry("800x600")

        # widgets para ingresar el nombre del estudiante
        self.label_nombre_estudiante = ctk.CTkLabel(self, text="Nombre del Estudiante:")
        self.label_nombre_estudiante.grid(row=0, column=0, padx=10, pady=10)

        self.entry_nombre_estudiante = ctk.CTkEntry(self, placeholder_text="Escribe el nombre del estudiante")
        self.entry_nombre_estudiante.grid(row=0, column=1, padx=10, pady=10)

        self.boton_guardar_nombre = ctk.CTkButton(self, text="Guardar Nombre", command=self.guardar_nombre_estudiante)
        self.boton_guardar_nombre.grid(row=0, column=2, padx=10, pady=10)

        # mostrar el nombre del estudiante actual
        self.label_estudiante_actual = ctk.CTkLabel(
            self, text=f"Estudiante: {self.controlador.obtener_nombre_estudiante()}"
        )
        self.label_estudiante_actual.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        #widgets para agregar asignaturas, generar reporte, ver estadisticas y el excel
        self.entry_asignatura = ctk.CTkEntry(self, placeholder_text="Nombre de la Asignatura")
        self.entry_asignatura.grid(row=2, column=0, padx=10, pady=10)

        self.boton_agregar_asignatura = ctk.CTkButton(self, text="Agregar Asignatura", command=self.agregar_asignatura)
        self.boton_agregar_asignatura.grid(row=2, column=1, padx=10, pady=10)

        self.lista_asignaturas = tk.Listbox(self, width=50, height=15, selectmode=tk.SINGLE)
        self.lista_asignaturas.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        self.boton_ingresar_notas = ctk.CTkButton(self, text="Ingresar Notas", command=self.abrir_ventana_notas)
        self.boton_ingresar_notas.grid(row=4, column=0, padx=10, pady=10)

        self.boton_resumen = ctk.CTkButton(self, text="Generar Resumen", command=self.mostrar_reporte)
        self.boton_resumen.grid(row=5, column=0, padx=10, pady=10)

        self.boton_estadisticas = ctk.CTkButton(self, text="Ver Estadísticas", command=self.mostrar_estadisticas)
        self.boton_estadisticas.grid(row=6, column=0, padx=10, pady=10)

        self.boton_generar_excel = ctk.CTkButton(self, text="Generar Excel", command=self.generar_excel)
        self.boton_generar_excel.grid(row=7, column=0, padx=10, pady=10)

        self.actualizar_lista_asignaturas()

    def guardar_nombre_estudiante(self):#metodo para guardar el nombre del estudiante
        nombre = self.entry_nombre_estudiante.get().strip()  # Obtiene y limpia el texto ingresado
        if not nombre:  # Valida que no esté vacío
            messagebox.showerror("Error", "El nombre del estudiante no puede estar vacío.")
            return
        self.controlador.establecer_nombre_estudiante(nombre)  # Envía el nombre al controlador
        self.label_estudiante_actual.configure(text=f"Estudiante: {nombre}")  # Actualiza la etiqueta
        self.entry_nombre_estudiante.delete(0, tk.END)  # Limpia el campo de entrada

    def agregar_asignatura(self):#metodo para agregar una asignatura
        nombre_asignatura = self.entry_asignatura.get().strip()  # Obtiene y limpia el texto ingresado
        if not nombre_asignatura:  # Valida que no esté vacío
            messagebox.showerror("Error", "El nombre de la asignatura no puede estar vacío.")
            return
        self.controlador.agregar_asignatura(nombre_asignatura)  # Envía la asignatura al controlador
        self.entry_asignatura.delete(0, tk.END)  # Limpia el campo de entrada
        self.actualizar_lista_asignaturas()  # Actualiza la lista de asignaturas

    def actualizar_lista_asignaturas(self):#metodo para actualizar la lista de asignaturas mostrada
        self.lista_asignaturas.delete(0, tk.END)  #limpia la lista actual
        asignaturas = self.controlador.obtener_asignaturas()  #obtiene las asignaturas del controlador
        for asignatura in asignaturas:  #agrega cada asignatura a la lista
            self.lista_asignaturas.insert(tk.END, asignatura.nombre)

    def abrir_ventana_notas(self):#metodo para abrir la ventana de notas
        seleccion = self.lista_asignaturas.curselection()  # verifica qué asignatura está seleccionada
        if not seleccion:  # valida que haya una asignatura seleccionada
            messagebox.showerror("Error", "Debe seleccionar una asignatura.")
            return
        indice = seleccion[0]  #obtiene el índice de la asignatura seleccionada
        asignatura = self.controlador.obtener_asignaturas()[indice]  #obtiene la asignatura específica
        VentanaNotas(self, asignatura, self.controlador)  #abre la ventana para ingresar notas

    def mostrar_reporte(self):#metodo para mostrar un reporte en una ventana emergente
        reporte = self.controlador.generar_reporte()  #genera el reporte desde el controlador
        VentanaResumen(self, reporte)  #muestra el reporte en una ventana nueva
    
    def mostrar_estadisticas(self):#metodo para mostrar estadísticas de las notas
        estadisticas = self.controlador.calcular_estadisticas()  #calcula las estadísticas desde el controlador
        VentanaResumen(self, estadisticas)  #muestra las estadísticas en una ventana nueva

    def generar_excel(self):#metodo para generar un archivo de excel
        try:
            #obtiene los datos necesarios para el reporte
            nombre_estudiante = self.controlador.obtener_nombre_estudiante()
            asignaturas = self.controlador.obtener_asignaturas()

            #crea un nuevo archivo de Excel
            wb = openpyxl.Workbook()
            ws = wb.active
            ws.title = "Reporte de Notas"

            #agrega encabezados y datos
            ws.append(["Nombre del Estudiante", nombre_estudiante])
            ws.append([])  # Fila vacía
            ws.append(["Asignatura", "Nota 1", "Nota 2", "Nota 3", "Promedio"])

            promedio_general = 0  #variable para calcular el promedio general
            for asignatura in asignaturas:
                notas = asignatura.notas
                promedio = sum(notas) / len(notas) if notas else 0
                promedio_general += promedio
                ws.append([asignatura.nombre, *notas, promedio])

            #calcula y agrega el promedio general
            if asignaturas:
                promedio_general /= len(asignaturas)
            ws.append([])  # Fila vacía
            ws.append(["Promedio General", promedio_general])

            #guarda el archivo
            nombre_archivo = f"Reporte_Notas_{nombre_estudiante}.xlsx"
            wb.save(nombre_archivo)

            #mensaje de éxito
            messagebox.showinfo("Éxito", f"Reporte generado con éxito: {nombre_archivo}")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al generar el Excel: {e}")



class VentanaNotas(ctk.CTkToplevel):#Clase VentanaNotas para gestionar la entrada y cálculo de notas
    def __init__(self, parent, asignatura, controlador):
        super().__init__(parent)
        self.title(f"Ingresar Notas: {asignatura.nombre}")  # Título de la ventana, con el nombre de la asignatura
        self.geometry("600x500") 
        self.asignatura = asignatura  
        self.controlador = controlador 

        # mensaje de instruccion para que el usuario digite las notas
        self.label_instruccion = ctk.CTkLabel(self, text="Ingrese las 3 notas de la asignatura:")
        self.label_instruccion.pack(pady=10) 

        #primera nota
        self.entry_nota1 = ctk.CTkEntry(self, placeholder_text="Nota 1")
        self.entry_nota1.pack(pady=5)  # Margen vertical

        #segunda nota
        self.entry_nota2 = ctk.CTkEntry(self, placeholder_text="Nota 2")
        self.entry_nota2.pack(pady=5)

        #tercera nota
        self.entry_nota3 = ctk.CTkEntry(self, placeholder_text="Nota 3")
        self.entry_nota3.pack(pady=5)

        #etiqueta que muestra la minima para ganar
        self.label_nota_ganar = ctk.CTkLabel(self, text="Nota minima para ganar: ")
        self.label_nota_ganar.pack(pady=10)

        #boton para calcular la minima
        self.boton_calcular = ctk.CTkButton(
            self, text="Calcular Nota para Ganar", command=self.mostrar_nota_para_ganar
        )
        self.boton_calcular.pack(pady=10)

        #boton para guardar las notas ingresadas
        self.boton_guardar = ctk.CTkButton(self, text="Guardar Notas", command=self.guardar_notas)
        self.boton_guardar.pack(pady=10)

    # Método para calcular y mostrar la nota mínima para ganar
    def mostrar_nota_para_ganar(self):
        try:
            #aqui se obtienen las dos primeras notas que estan escritas en los dos primeros campos
            nota1 = float(self.entry_nota1.get())
            nota2 = float(self.entry_nota2.get())

            #aqui se verifica si las notas estan entre 0 y 5
            if not (0 <= nota1 <= 5 and 0 <= nota2 <= 5):
                raise ValueError("Las notas deben estar entre 0 y 5.")

            #calcula la nota minima para ganar prestando la asignatura
            nota_para_ganar = self.asignatura.calcular_nota_para_ganar([nota1, nota2])

            #selecciona un mensaje dependiendo de que nota necesita para ganar
            if nota_para_ganar > 5:
                mensaje = "(Mejor busca las esferas del dragón)" #pobre condenado
            elif 0 <= nota_para_ganar <= 1.0:
                mensaje = "(Estás volando)"
            elif 1.1 <= nota_para_ganar <= 2.9:
                mensaje = "(No te relajes, papi)" 
            elif 3.0 <= nota_para_ganar <= 5.0:
                mensaje = "(Ve rezándole al de arriba)" 
            else:
                mensaje = "" 

            # muestra la minima
            self.label_nota_ganar.configure(
                text=f"Nota mínima para ganar: {nota_para_ganar:.2f} {mensaje}"
            )
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def guardar_notas(self):#metodo para guardar las notas
        try:
            notas = [
                float(self.entry_nota1.get()),  
                float(self.entry_nota2.get()),  
                float(self.entry_nota3.get()),  
            ]

            #condicion para que las notas ingresadas esten entre 0 y 5
            if any(nota < 0 or nota > 5 for nota in notas):
                raise ValueError("Todas las notas deben estar entre 0 y 5.")

            #llama al controlador para guardar las notas de la asignatura
            self.controlador.guardar_notas(self.asignatura.nombre, notas)

            messagebox.showinfo("Éxito", "Notas guardadas correctamente.")
            self.destroy() 
        except ValueError as e:
            messagebox.showerror("Error", str(e))

class VentanaResumen(ctk.CTkToplevel):#ventana tanto para el resumen de las notas como para las estadisticas
    def __init__(self, parent, contenido):
        super().__init__(parent)  
        self.title("Resumen") 
        self.geometry("600x400")
        self.texto_resumen = tk.Text(
            self, wrap=tk.WORD  #usa el ajuste automatico para cada palabra
        )
        self.texto_resumen.insert(
            tk.END, contenido
        )  #coloca el contenido del resumen al final del cuadro de texto
        self.texto_resumen.config(
            state=tk.DISABLED
        )  #esto permite desactivar la edicion del cuadro ya que solo queremos mostrar mas no editar
        self.texto_resumen.pack(
            pady=10, padx=10
        )  #los margenes para que se vea mas minimalista