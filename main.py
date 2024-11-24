import customtkinter as ctk  
from vista import VistaPrincipal  
from controlador import Controlador  

if __name__ == "__main__": #aqui indico que este es el archivo principal y el codigo se ejecuta solo con este archivo

    ctk.set_appearance_mode("dark")

    ctk.set_default_color_theme("blue")

    # aqui se instancia el objeto "arranque" y se le asigna la vistaprincipal, la cual pasa al controlador e inicia el programa
    arranque = VistaPrincipal(Controlador())

    # Este aqui se mantiene activo el programa y responde a las iteraciones del usuario
    arranque.mainloop()
