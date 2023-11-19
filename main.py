import tkinter as tk
import random

class MedianVisualizer:
    small_pad = 10

    def __init__(self, root, data):
        self.root = root
        self.root.title("Visualização do Algoritmo das Medianas")
        
        self.data = data
        self.rectangles = []
        self.texts = []

        self.criar_widgets()
        self.draw_data()

    def draw_data(self):
        data_len = len(self.data)
        rect_width = 300 // data_len if data_len > 0 else 0
        for i, value in enumerate(self.data):
            x1 = i * rect_width
            y1 = 200
            x2 = (i + 1) * rect_width
            y2 = 200 - value
            
            rect = self.canvas.create_rectangle(x1, y1, x2, y2, fill="blue")
            self.rectangles.append(rect)

            text_x = (x1 + x2) / 2
            text_y = (y1 + y2) / 2
            text = self.canvas.create_text(text_x, text_y, text=str(value), fill="white")
            self.texts.append(text)

    def update_visualization(self, pivot_idx):
        for i, (rect, text) in enumerate(zip(self.rectangles, self.texts)):
            color = "red" if i == pivot_idx else "blue"
            self.canvas.itemconfig(rect, fill=color)
            self.root.update_idletasks()
            self.root.after(500)

    def quick_select(self, l, r, k):
        if l == r:
            return l

        pivot_idx = self.partition(l, r)
        self.update_visualization(pivot_idx)

        if k == pivot_idx:
            return k
        elif k < pivot_idx:
            return self.quick_select(l, pivot_idx - 1, k)
        else:
            return self.quick_select(pivot_idx + 1, r, k)

    def partition(self, l, r):
        pivot_idx = random.randint(l, r)
        pivot_value = self.data[pivot_idx]

        self.update_visualization(pivot_idx)

        self.data[pivot_idx], self.data[r] = self.data[r], self.data[pivot_idx]

        i = l - 1
        for j in range(l, r):
            if self.data[j] <= pivot_value:
                i += 1
                self.data[i], self.data[j] = self.data[j], self.data[i]
        self.data[i + 1], self.data[r] = self.data[r], self.data[i + 1]

        return i + 1
    
    def encontrar_mediana(self):
        median_index = self.quick_select(0, len(self.data) - 1, len(self.data) // 2)
        mediana = self.canvas.itemcget(self.texts[median_index], 'text')
        self.mediana_label.config(text=f"A mediana é: {mediana}")

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
        data = [0 for _ in range(len(self.data))]
        self.data = data
        for rect in self.rectangles:
            self.canvas.delete(rect)
        for text in self.texts:
            self.canvas.delete(text)

        self.rectangles.clear()
        self.texts.clear()
        self.draw_data()

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
    data = [random.randint(50, 150) for _ in range(10)]

    MedianVisualizer(root, data)

    root.mainloop()

if __name__ == "__main__":
    main()
