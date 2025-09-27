import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import random


class RPGFichaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ficha de RPG - Livro Jogo")

        # Atributos iniciais
        self.ficha = {
            "nome": "Aventureiro",
            "habilidade": 10,
            "energia": 20,
            "sorte": 10,
            "ouro": 0,
            "inventario": [],
            "anotacoes": ""
        }

        # Interface
        self.create_widgets()

    def create_widgets(self):
        # Nome
        tk.Label(self.root, text="Nome:").grid(row=0, column=0, sticky="w")
        self.nome_entry = tk.Entry(self.root)
        self.nome_entry.insert(0, self.ficha["nome"])
        self.nome_entry.grid(row=0, column=1, columnspan=2, sticky="we")

        # Atributos
        self.hab_label = tk.Label(self.root, text=f"Habilidade: {self.ficha['habilidade']}")
        self.hab_label.grid(row=1, column=0, sticky="w")
        tk.Button(self.root, text="+", command=lambda: self.change_attr("habilidade", 1)).grid(row=1, column=1)
        tk.Button(self.root, text="-", command=lambda: self.change_attr("habilidade", -1)).grid(row=1, column=2)

        self.ene_label = tk.Label(self.root, text=f"Energia: {self.ficha['energia']}")
        self.ene_label.grid(row=2, column=0, sticky="w")
        tk.Button(self.root, text="+", command=lambda: self.change_attr("energia", 1)).grid(row=2, column=1)
        tk.Button(self.root, text="-", command=lambda: self.change_attr("energia", -1)).grid(row=2, column=2)

        self.sor_label = tk.Label(self.root, text=f"Sorte: {self.ficha['sorte']}")
        self.sor_label.grid(row=3, column=0, sticky="w")
        tk.Button(self.root, text="+", command=lambda: self.change_attr("sorte", 1)).grid(row=3, column=1)
        tk.Button(self.root, text="-", command=lambda: self.change_attr("sorte", -1)).grid(row=3, column=2)

        self.ouro_label = tk.Label(self.root, text=f"Ouro: {self.ficha['ouro']}")
        self.ouro_label.grid(row=4, column=0, sticky="w")
        tk.Button(self.root, text="+", command=lambda: self.change_attr("ouro", 1)).grid(row=4, column=1)
        tk.Button(self.root, text="-", command=lambda: self.change_attr("ouro", -1)).grid(row=4, column=2)

        # Inventário
        tk.Label(self.root, text="Inventário:").grid(row=5, column=0, sticky="w")
        self.inventario_listbox = tk.Listbox(self.root, height=6)
        self.inventario_listbox.grid(row=6, column=0, columnspan=2, sticky="we")
        tk.Button(self.root, text="Adicionar Item", command=self.add_item).grid(row=6, column=2)
        tk.Button(self.root, text="Remover Item", command=self.remove_item).grid(row=7, column=2)

        # Anotações
        tk.Label(self.root, text="Anotações:").grid(row=8, column=0, sticky="w")
        self.anotacoes_text = tk.Text(self.root, height=5, width=40)
        self.anotacoes_text.insert("1.0", self.ficha["anotacoes"])
        self.anotacoes_text.grid(row=9, column=0, columnspan=3)

        # Dados
        tk.Button(self.root, text="Rolar 1D6", command=lambda: self.roll_dice(1)).grid(row=10, column=0)
        tk.Button(self.root, text="Rolar 2D6", command=lambda: self.roll_dice(2)).grid(row=10, column=1)

        # Combate
        tk.Button(self.root, text="Combate!", command=self.combat).grid(row=10, column=2)

        # Salvar / Carregar
        tk.Button(self.root, text="Salvar Ficha", command=self.save_ficha).grid(row=11, column=0)
        tk.Button(self.root, text="Carregar Ficha", command=self.load_ficha).grid(row=11, column=1)

    def change_attr(self, attr, value):
        self.ficha[attr] += value
        if attr == "habilidade":
            self.hab_label.config(text=f"Habilidade: {self.ficha['habilidade']}")
        elif attr == "energia":
            self.ene_label.config(text=f"Energia: {self.ficha['energia']}")
        elif attr == "sorte":
            self.sor_label.config(text=f"Sorte: {self.ficha['sorte']}")
        elif attr == "ouro":
            self.ouro_label.config(text=f"Ouro: {self.ficha['ouro']}")

    def add_item(self):
        item = simpledialog.askstring("Inventário", "Digite o nome do item:")
        if item:
            self.ficha["inventario"].append(item)
            self.inventario_listbox.insert(tk.END, item)

    def remove_item(self):
        selecionado = self.inventario_listbox.curselection()
        if selecionado:
            idx = selecionado[0]
            item = self.inventario_listbox.get(idx)
            self.ficha["inventario"].remove(item)
            self.inventario_listbox.delete(idx)

    def roll_dice(self, qtd):
        resultado = sum(random.randint(1, 6) for _ in range(qtd))
        messagebox.showinfo("Dado", f"Você rolou {qtd}D6 e obteve: {resultado}")
        return resultado

    def combat(self):
        inimigo_hab = simpledialog.askinteger("Combate", "Habilidade do inimigo:", minvalue=1, maxvalue=12)
        if inimigo_hab is None:
            return
        inimigo_ene = simpledialog.askinteger("Combate", "Energia do inimigo:", minvalue=1, maxvalue=30)
        if inimigo_ene is None:
            return

        while inimigo_ene > 0 and self.ficha["energia"] > 0:
            atk_jogador = self.roll_dice(2) + self.ficha["habilidade"]
            atk_inimigo = self.roll_dice(2) + inimigo_hab

            if atk_jogador > atk_inimigo:
                inimigo_ene -= 2
                messagebox.showinfo("Combate", f"Você atingiu o inimigo! Energia do inimigo: {inimigo_ene}")
            elif atk_inimigo > atk_jogador:
                self.ficha["energia"] -= 2
                self.ene_label.config(text=f"Energia: {self.ficha['energia']}")
                messagebox.showinfo("Combate", f"O inimigo atingiu você! Sua Energia: {self.ficha['energia']}")
            else:
                messagebox.showinfo("Combate", "Empate! Ninguém foi ferido.")

        if self.ficha["energia"] <= 0:
            messagebox.showerror("Derrota", "Você foi derrotado!")
        else:
            messagebox.showinfo("Vitória", "Você derrotou o inimigo!")

    def save_ficha(self):
        self.ficha["nome"] = self.nome_entry.get()
        self.ficha["anotacoes"] = self.anotacoes_text.get("1.0", tk.END).strip()
        with open("ficha.json", "w", encoding="utf-8") as f:
            json.dump(self.ficha, f, indent=4, ensure_ascii=False)
        messagebox.showinfo("Salvar", "Ficha salva em ficha.json")

    def load_ficha(self):
        try:
            with open("ficha.json", "r", encoding="utf-8") as f:
                self.ficha = json.load(f)

            # Atualizar interface
            self.nome_entry.delete(0, tk.END)
            self.nome_entry.insert(0, self.ficha["nome"])
            self.hab_label.config(text=f"Habilidade: {self.ficha['habilidade']}")
            self.ene_label.config(text=f"Energia: {self.ficha['energia']}")
            self.sor_label.config(text=f"Sorte: {self.ficha['sorte']}")
            self.ouro_label.config(text=f"Ouro: {self.ficha['ouro']}")

            self.inventario_listbox.delete(0, tk.END)
            for item in self.ficha["inventario"]:
                self.inventario_listbox.insert(tk.END, item)

            self.anotacoes_text.delete("1.0", tk.END)
            self.anotacoes_text.insert("1.0", self.ficha["anotacoes"])

            messagebox.showinfo("Carregar", "Ficha carregada com sucesso!")
        except FileNotFoundError:
            messagebox.showerror("Erro", "Nenhum arquivo de ficha encontrado.")


if __name__ == "__main__":
    root = tk.Tk()
    app = RPGFichaApp(root)
    root.mainloop()
