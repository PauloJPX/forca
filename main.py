import tkinter as tk
from tkinter import messagebox
import random
from PIL import Image, ImageTk

class ForcaApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("400x450")
        self.root.title("Jogo da Forca")

        # Variáveis
        self.palavras = self.carregar_palavras("palavras.txt")
        self.nivel = tk.IntVar(value=1)  # 1: Fácil, 2: Médio, 3: Difícil
        self.palavra_atual = ""
        self.letras_adivinhadas = []
        self.letras_erradas = ""
        self.tentativas = 0
        self.max_tentativas = 6

        # Frame principal
        self.frame = tk.Frame(root)
        #self.frame.pack(pady=20)
        self.frame.grid(row=0, column=0, padx=20, pady=20)

        # Seleção de dificuldade
        self.dificuldade_frame = tk.LabelFrame(self.frame, text="Escolha a dificuldade")
        #self.dificuldade_frame.pack(pady=10)
        self.dificuldade_frame.grid(row=0, column=0, pady=10)
        for nivel, texto in zip([1, 2, 3, 4], ["Fácil", "Médio", "Difícil","Complicado"]):
            tk.Radiobutton(self.dificuldade_frame, text=texto, variable=self.nivel, value=nivel).pack(side=tk.LEFT)

        # Imagem do boneco
        self.boneco_label = tk.Label(self.frame)
        self.boneco_label.grid(row=1, column=0)
        self.imagens = []
        for i in range(9):
            img = Image.open(f"img/img{i}.png")
            img = img.resize((250, 250))  # Reduzir a imagem para o tamanho desejado
            self.imagens.append(ImageTk.PhotoImage(img))
        self.boneco_label.config(image=self.imagens[0])

        # Espaços da palavra
        self.palavra_label = tk.Label(self.frame, font=("Courier", 24))
        #self.palavra_label.pack(pady=10)
        self.palavra_label.grid(row=2, column=0, pady=10)

        # Entrada de letra
        self.letra_entry = tk.Entry(self.frame, font=("Courier", 16),width=1)
        #self.letra_entry.pack(pady=10)
        self.letra_entry.grid(row=1, column=1, pady=10)
        self.letra_entry.bind("<KeyRelease>", self.verificar_letra)

        # Botão para iniciar
        self.iniciar_button = tk.Button(self.frame, text="Iniciar Jogo", command=self.iniciar_jogo)
        #self.iniciar_button.pack(pady=20)
        self.iniciar_button.grid(row=0, column=2, pady=20)

        # letras digitadas
        self.letrasDigitas = tk.Label(self.frame,text="", bg="green", fg="red",font=("Arial", 12,'bold'))
        self.letrasDigitas.grid(row=3,column=0)


    def carregar_palavras(self, arquivo):
        palavras = {1: [], 2: [], 3: [],4: []}
        with open(arquivo, 'r') as f:
            for linha in f:
                palavra, dificuldade = linha.strip().split(',')
                palavras[int(dificuldade)].append(palavra.lower())
        return palavras

    def iniciar_jogo(self):
        self.tentativas = 0
        self.boneco_label.config(image=self.imagens[self.tentativas])
        self.palavra_atual = random.choice(self.palavras[self.nivel.get()])
        self.letras_adivinhadas = ["_"] * len(self.palavra_atual)
        self.letras_erradas = ''
        self.letrasDigitas.config(text='')
        self.atualizar_palavra()
        # Coloca o foco no campo de entrada da letra
        self.letra_entry.focus_set()

    def atualizar_palavra(self):
        self.palavra_label.config(text=" ".join(self.letras_adivinhadas))

    def verificar_letra(self, event=None):
        letra = event.char.lower()  # Obtém a letra pressionada (do evento)

        # Garante que apenas letras sejam processadas
        if not letra.isalpha() or len(letra) != 1:
            return  # Não faz nada se não for uma letra válida
        if letra in self.letras_erradas:
            return # essa letra errada ja foi escolhida

        if letra in self.palavra_atual:
            for idx, char in enumerate(self.palavra_atual):
                if char == letra:
                    self.letras_adivinhadas[idx] = letra
            self.atualizar_palavra()
            if "_" not in self.letras_adivinhadas:
                #messagebox.showinfo("Parabéns", "Você venceu!")
                self.boneco_label.config(image=self.imagens[7])
                #self.iniciar_jogo()

        else:
            self.tentativas += 1
            self.letras_erradas += ' '+letra
            self.letrasDigitas.config(text=self.letras_erradas)
            self.boneco_label.config(image=self.imagens[self.tentativas])
            if self.tentativas == self.max_tentativas:
                #messagebox.showerror("Game Over", f"Você perdeu! A palavra era: {self.palavra_atual}")
                self.boneco_label.config(image=self.imagens[8])
                self.palavra_label.config(text=self.palavra_atual)
                #self.iniciar_jogo()


if __name__ == "__main__":
    root = tk.Tk()
    app = ForcaApp(root)
    root.mainloop()
