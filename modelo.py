class Estudiante:
    def __init__(self, nombre): #aqui se crea el atributo estudiante y asignaturas(esta se crea como una lista)
        self.nombre = nombre 
        self.asignaturas = [] 

    def agregar_asignatura(self, asignatura): #metodo para agregar las asignaturas a lalista
        self.asignaturas.append(asignatura) 

    def obtener_asignaturas(self): # metodo para obtener las asignaturas del estudiante.
        return self.asignaturas 

class Asignatura:
    def __init__(self, nombre): #atributo para estudiantes y nota(como lista)
        self.nombre = nombre 
        self.notas = []

    def agregar_notas(self, notas):#metodo para agregar notas a las asignaturas
        if len(notas) != 3:  
            raise ValueError("Debe proporcionar exactamente 3 notas.")
        if any(nota < 0 or nota > 5 for nota in notas): 
            raise ValueError("Todas las notas deben estar entre 0 y 5.")
        self.notas = notas

    def calcular_definitiva(self):#metodo para calcular la definitiva de la asignatura correspondiente
        if not self.notas:  # Si no hay notas registradas devuelve 0.
            return 0
        return sum(self.notas) / len(self.notas) 

    def calcular_nota_para_ganar(self, notas):#metodo para calcular cuanto tiene que sacar en la nota 3 para ganar
        if len(notas) != 2:  # Valida que se proporcionen exactamente 2 notas.
            raise ValueError("Se necesitan exactamente dos notas para calcular la tercera nota.")
        suma_actual = sum(notas)  
        nota_para_ganar = (3 * 3) - suma_actual 
        return nota_para_ganar
