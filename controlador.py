from modelo import Estudiante, Asignatura

class Controlador:
    def __init__(self):
        self.estudiante = Estudiante("")  #aqui se crea el atributo estudiante y se inicia en vacio(ya que no sabemos el nombre del estudiante que se va a registrar)

    def obtener_nombre_estudiante(self):
        return self.estudiante.nombre #metodo get para obtener el nombre

    def establecer_nombre_estudiante(self, nombre):
        self.estudiante.nombre = nombre #metodo set para actualizar el nombre

    def agregar_asignatura(self, nombre_asignatura): #aqui se agregan las asignaturas para el estuiante
        nueva_asignatura = Asignatura(nombre_asignatura)  # Crea una nueva asignatura.
        self.estudiante.agregar_asignatura(nueva_asignatura)  # La asignatura se añade al estudiante.

    def obtener_asignaturas(self):
        return self.estudiante.obtener_asignaturas() #aqui se obtiene las asignaturas del estudiante

    def guardar_notas(self, nombre_asignatura, notas):#Guarda las notas en la asignatura corresponiente.
        # Busca la asignatura en la lista de asignaturas del estudiante.
        asignatura = next(
            (a for a in self.estudiante.obtener_asignaturas() if a.nombre == nombre_asignatura), None
        )
        if not asignatura:  # Si no se encuentra la asignatura, lanza un error.
            raise ValueError(f"No se encontró la asignatura '{nombre_asignatura}'.")
        asignatura.agregar_notas(notas)# Guarda las notas en la asignatura encontrada.

    def generar_reporte(self):#Genera un reporte con las asignaturas, notas y las definitivas del estudiante.
        resumen = f"Estudiante: {self.estudiante.nombre}\n"
        resumen += "Asignaturas y Notas:\n"
        for asignatura in self.estudiante.obtener_asignaturas():  # un ciclo para obtener todas las asignaturas
            notas = asignatura.notas 
            definitiva = asignatura.calcular_definitiva() 
            # Agrega información sobre cada asignatura al reporte.
            resumen += f"  - {asignatura.nombre}:\n"
            resumen += f"    Notas: {', '.join(map(str, notas))}\n"
            resumen += f"    Nota Definitiva: {definitiva:.2f}\n"

        return resumen

    def calcular_estadisticas(self):#Calcula las estadísticas de forma general para las notas del estudiante
        asignaturas = self.estudiante.obtener_asignaturas()  # Obtiene todas las asignaturas del estudiante.
        if not asignaturas:  # Si no hay asignaturas, devuelve un mensaje.
            return "No hay asignaturas registradas."

        # Calcula las definitivas de todas las asignaturas.
        definitivas = [asignatura.calcular_definitiva() for asignatura in asignaturas]
        promedio_general = sum(definitivas) / len(definitivas)
        max_nota = max(definitivas)
        min_nota = min(definitivas) 

        # muestra las estadisticas generales
        estadisticas = (
            f"Promedio General: {promedio_general:.2f}\n"
            f"Máxima Nota Definitiva: {max_nota:.2f}\n"
            f"Mínima Nota Definitiva: {min_nota:.2f}\n"
            f"Número de Asignaturas: {len(definitivas)}"
        )
        return estadisticas
