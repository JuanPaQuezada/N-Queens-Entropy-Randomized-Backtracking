import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import math
import customtkinter as ctk
import tkinter as tk
def plot_board(queens, n, all_solutions):
    total=len(all_solutions)
    col=10
    row=math.ceil(total/col)
    dx, dy=0.015, 0.05
    P=np.arange(-0.5,5.0,dx)
    Q=np.arange(-0.5,5.0,dy)
    X,Y=np.meshgrid(P,Q)
    fig, ax=plt.subplots(row,col,figsize=(15,15))
    axes=ax.flatten()
    min_max=np.min(P), np.max(P),np.min(Q),np.max(Q)
    res=np.add.outer(range(n),range(n))%2
    for i, ax in enumerate(axes):
        if i<total:
            ax.imshow(res,cmap="binary_r")
            queens=all_solutions[i]
            xcoords=[q[0] for q in queens]
            ycoords=[q[1] for q in queens]
            ax.scatter(xcoords,ycoords,c="red",s=100,zorder=5)
            ax.set_title(f"Solución {i+1}", fontsize=8)
        plt.xticks([])
        plt.yticks([])
    plt.title("Tablero de ajedrez")
    plt.tight_layout()
    plt.show()
class VisorCustomTkinter:
    def __init__(self, all_solutions, n):
        self.soluciones = all_solutions
        self.n = n
        self.indice_actual = 0
        self.cell_size = 50
        self.canvas_size = self.n * self.cell_size
        self.mapa_calor = np.zeros((self.n, self.n))
        self.modo_calor=False
        self.modo_juego=False
        self.reinas_usuario=[]
        for solution in self.soluciones:
            for row, col in solution:
                self.mapa_calor[row][col]+=1

        self.max_frecuencia = np.max(self.mapa_calor)

        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        self.root = ctk.CTk()
        self.root.title("Visor Interactivo N-Reinas")
        self.root.geometry(f"{self.canvas_size + 100}x{self.canvas_size + 220}")
        self.root.resizable(False, False)

        self.lbl_info = ctk.CTkLabel(self.root, text="", font=("Roboto", 20, "bold"))
        self.lbl_info.pack(pady=(20, 10))

        self.canvas = tk.Canvas(self.root, width=self.canvas_size, height=self.canvas_size, 
                                bg="#2b2b2b", highlightthickness=0)
        self.canvas.pack(pady=10)

        btn_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        btn_frame.pack(pady=10)

        self.btn_prev = ctk.CTkButton(btn_frame, text="Anterior", command=self.prev_solucion, 
                                      width=120, height=35, font=("Roboto", 14))
        self.btn_prev.pack(side="left", padx=20)

        self.btn_next = ctk.CTkButton(btn_frame, text="Siguiente", command=self.next_solucion, 
                                      width=120, height=35, font=("Roboto", 14))
        self.btn_next.pack(side="right", padx=20)

        self.btn_mapaCalor = ctk.CTkButton(self.root, text="Mapa de calor", command=self.toggle_calor, 
                                           width=120, height=35, font=("Roboto", 14))
        self.btn_mapaCalor.pack(padx=20)

        self.btn_jugar_usuario = ctk.CTkButton(self.root,text="Jugar", command=self.jugar_usuario_tablero, width=120, height=35, font=("Roboto", 14))
        self.btn_jugar_usuario.pack(padx=30, pady=10)

        self.root.bind("<Right>", lambda event: self.next_solucion())
        self.root.bind("<Left>", lambda event: self.prev_solucion())

        self.dibujar_tablero()
        self.root.mainloop()
    def dibujar_tablero(self):
        self.canvas.delete("all")
        color_claro = "#DDE3E6"
        color_oscuro = "#5C7599" 
        for row in range(self.n):
            for col in range(self.n):
                x1 = col * self.cell_size
                y1 = row * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                if self.modo_calor:
                    frecuencia = self.mapa_calor[row][col]
                    if frecuencia > 0:
                        porcentaje = frecuencia / self.max_frecuencia
                        intensity = int(255 * porcentaje)
                        color = f'#{intensity:02x}0000'

                    else: 
                        color="#444444"
                else:
                    color = color_claro if (row + col) % 2 == 0 else color_oscuro
                    borde=""
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")

        if self.modo_juego:
            queens=self.reinas_usuario
        elif self.soluciones:
            queens=self.soluciones[self.indice_actual]
        else:
            queens=[]

        for row, col in queens:
            x1 = col * self.cell_size + 8
            y1 = row * self.cell_size + 8
            x2 = (col + 1) * self.cell_size - 8
            y2 = (row + 1) * self.cell_size - 8
            self.canvas.create_oval(x1, y1, x2, y2, fill="#FF4B4B", outline="#8B0000", width=2)
        if self.modo_juego:
            self.lbl_info.configure(text=f"Modo Libre: Coloca hasta {self.n} reinas")
        elif self.modo_calor:
            self.lbl_info.configure(text=f"Mapa de calor: {self.max_frecuencia} apariciones máximas")
        else:
            total = len(self.soluciones)
            self.lbl_info.configure(text=f"Solución {self.indice_actual + 1} de {total}")

    def next_solucion(self):
        if self.soluciones:
            self.indice_actual = (self.indice_actual + 1) % len(self.soluciones)
            self.dibujar_tablero()
    def prev_solucion(self):
        if self.soluciones:
            self.indice_actual = (self.indice_actual - 1) % len(self.soluciones)
            self.dibujar_tablero()
    def toggle_calor(self):
        self.modo_calor = not self.modo_calor
        self.dibujar_tablero()
    def jugar_usuario_tablero(self):
        boton_activo=self.btn_jugar_usuario.cget("text")
        if boton_activo=="Jugar":
            self.modo_juego=True
            self.btn_jugar_usuario.configure(text="Soluciones")
            self.canvas.bind("<Button-1>", self.colocar_reina)
            self.reinas_usuario=[]
            self.btn_prev.configure(state="disabled")
            self.btn_next.configure(state="disabled")
        else:
            self.modo_juego=False
            self.btn_jugar_usuario.configure(text="Jugar")
            self.canvas.unbind("<Button-1>")
            self.btn_prev.configure(state="normal")
            self.btn_next.configure(state="normal")
        self.dibujar_tablero()
    def colocar_reina(self, event):
        col = event.x // self.cell_size
        row = event.y // self.cell_size
        if (row, col) in self.reinas_usuario:
            self.reinas_usuario.remove((row,col))
        elif len(self.reinas_usuario) < self.n:
            self.reinas_usuario.append((row, col))
        self.dibujar_tablero()
        if len(self.reinas_usuario)==self.n:
            reinas_ordenadas=sorted(self.reinas_usuario)
            if reinas_ordenadas in self.soluciones:
                self.lbl_info.configure(text="Has encontrado una solución")
            else:
                self.lbl_info.configure(text="No es una solución válida")

        
def iniciar_visor(all_solutions, n):
    VisorCustomTkinter(all_solutions, n)



