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

        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        self.root = ctk.CTk()
        self.root.title("Visor Interactivo N-Reinas")
        self.root.geometry(f"{self.canvas_size + 100}x{self.canvas_size + 180}")
        self.root.resizable(False, False)

        self.lbl_info = ctk.CTkLabel(self.root, text="", font=("Roboto", 20, "bold"))
        self.lbl_info.pack(pady=(20, 10))

        self.canvas = tk.Canvas(self.root, width=self.canvas_size, height=self.canvas_size, 
                                bg="#2b2b2b", highlightthickness=0)
        self.canvas.pack(pady=10)

        btn_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        btn_frame.pack(pady=10)

        self.btn_prev = ctk.CTkButton(btn_frame, text="⬅️ Anterior", command=self.prev_solucion, 
                                      width=120, height=35, font=("Roboto", 14))
        self.btn_prev.pack(side="left", padx=20)

        self.btn_next = ctk.CTkButton(btn_frame, text="Siguiente ➡️", command=self.next_solucion, 
                                      width=120, height=35, font=("Roboto", 14))
        self.btn_next.pack(side="right", padx=20)

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
                
                color = color_claro if (row + col) % 2 == 0 else color_oscuro
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")

        if self.soluciones:
            queens = self.soluciones[self.indice_actual]
            for row, col in queens:
                x1 = col * self.cell_size + 8
                y1 = row * self.cell_size + 8
                x2 = (col + 1) * self.cell_size - 8
                y2 = (row + 1) * self.cell_size - 8
                self.canvas.create_oval(x1, y1, x2, y2, fill="#FF4B4B", outline="#8B0000", width=2)

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

def iniciar_visor(all_solutions, n):
    VisorCustomTkinter(all_solutions, n)
