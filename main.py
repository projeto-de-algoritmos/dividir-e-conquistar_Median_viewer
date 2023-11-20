import tkinter as tk
import random
from dataclasses import dataclass
from time import sleep

@dataclass
class Item:
    text: int
    rectangle: int
    value: int

    def __lt__(self, other):
        return self.value < other.value
    
    def __eq__(self, other):
        return self.value == other.value

class MedianVisualizer:
    small_pad = 10

    def __init__(self, root, data):
        self.root = root
        self.root.title("Visualização do Algoritmo das Medianas")
        self.data = data
        self.last_rect = 0
        self.items = []
        self.criar_widgets()
        self.draw_data()

    def draw_data(self):
        data_len = len(self.data)
        canvas_width = 300
        rect_width = canvas_width // data_len if data_len > 0 else 0

        max_value = max(self.data)
        
        for i, value in enumerate(self.data):
            scaled_value = (value / max_value) * 200 

            x1 = i * rect_width
            y1 = 200
            x2 = (i + 1) * rect_width
            y2 = 200 - scaled_value

            rect = self.canvas.create_rectangle(x1, y1, x2, y2, fill="blue")

            text_x = (x1 + x2) / 2
            text_y = y1 + 10
            text = self.canvas.create_text(text_x, text_y, text=str(value), fill="black")

            item = Item(text, rect, value)
            self.items.append(item)

    def update_visualization(self, pivot):
        self.canvas.itemconfig(self.last_rect, fill="blue")
        self.canvas.itemconfig(pivot.rectangle, fill="red")
        self.last_rect = pivot.rectangle
        self.root.update_idletasks()
        self.root.after(500)
        sleep(2)

    def select_pivot(self, arr, k):
        chunks = [arr[i : i+5] for i in range(0, len(arr), 5)]

        sorted_chunks = [sorted(chunk) for chunk in chunks]
        medians = [chunk[len(chunk) // 2] for chunk in sorted_chunks]

        if len(medians) <= 5:
            pivot = sorted(medians)[len(medians) // 2]
        else:
            pivot = self.select_pivot(len(medians) // 2)

        self.update_visualization(pivot)
        p = self.partition(arr, pivot)

        if k == p:
            return pivot

        if k < p:
            return self.select_pivot(arr[0:p], k)
        else:
            return self.select_pivot(arr[p+1:len(arr)], k - p - 1)

    def partition(self, arr, pivot):
        left = 0
        right = len(arr) - 1
        i = 0

        while i <= right:
            if arr[i] == pivot:
                i += 1

            elif arr[i] < pivot:
                arr[left], arr[i] = arr[i], arr[left]
                left += 1
                i += 1
            else:
                arr[right], arr[i] = arr[i], arr[right]
                right -= 1

        return left
        
    def encontrar_mediana(self):
            mediana = self.select_pivot(self.items, len(self.data)//2)
            self.canvas.itemconfig(mediana.rectangle, fill="green")
            self.mediana_label.config(text=f"A mediana é: {mediana.value}")

    def criar_janelas(self):
        esquerda = tk.Frame(self.root)
        esquerda.pack(
            side="left", padx=self.small_pad, pady=self.small_pad, expand=True
        )

        direita = tk.Frame(self.root, height=400, width=650)
        direita.pack(
            side="right", padx=self.small_pad, pady=self.small_pad, expand=True
        )

        return esquerda, direita
    
    def criar_array(self):
        nums = self.entrada.get("1.0", "end-1c").split()
        try:
            nums = [int(num) for num in nums]
            self.mensagem_erro_label.config(text="") 
        except ValueError:
            self.mensagem_erro_label.config(text="Erro: Por favor, insira apenas números.")
            return
        self.limpar_array()
        self.data = nums
        self.draw_data()
    
    def limpar_array(self):
        self.data.clear()
        self.canvas.delete("all")

        self.items.clear()

    def criar_widgets(self):
        janela_esq, janela_dir = self.criar_janelas()
        
        self.canvas = tk.Canvas(janela_dir)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        entrada_label = tk.Label(janela_esq, text="Digite os items do seu array separados por espaço:")
        entrada_label.pack()
        self.mensagem_erro_label = tk.Label(janela_esq, text="", fg="red")
        self.mensagem_erro_label.pack()

        self.entrada = tk.Text(janela_esq, wrap=tk.WORD, height=2, width=40)
        self.entrada.pack()

        botao_frame = tk.Frame(janela_esq)
        botao_frame.pack(pady=self.small_pad)

        criar_botao = tk.Button(
            botao_frame, text="Criar", command=self.criar_array
        )
        criar_botao.pack(side="top", padx=self.small_pad,  fill="both", expand=True)


        limpar_botao = tk.Button(
            botao_frame, text="Limpar", command=self.limpar_array
        )
        limpar_botao.pack(side="left", padx=self.small_pad,  fill="both", expand=True)

        mediana_botao = tk.Button(
            botao_frame, text="Encontrar mediana", command=self.encontrar_mediana
        )
        mediana_botao.pack(side="left", padx=self.small_pad, fill="both", expand=True)

        self.mediana_label = tk.Label(janela_esq, text="A mediana é:")
        self.mediana_label.pack()

def main():
    root = tk.Tk()
    data = [random.randint(50, 150) for _ in range(9)]

    MedianVisualizer(root, data)

    root.mainloop()

if __name__ == "__main__":
    main()
