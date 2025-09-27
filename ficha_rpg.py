import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import messagebox, simpledialog
import json
import random

class RPGFichaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ficha de RPG - Livro Jogo")
        self.root.geometry("600x700")

        # Tema escuro
        self.style = tb.Style(theme="darkly")

        # Ficha inicial
        self.ficha = {
            "nome": "Aventureiro",
            "classe": "Guerreiro",
            "habilidade": 10,
            "energia": 20,
            "sorte": 10,
            "ouro": 0,
            "inventario": [],
            "anotacoes": ""
        }

        self.create_widgets()

    def create_widgets(self):
        # Frame principal com padding
        main_frame = tb.Frame(self.root, padding=15, bootstyle="secondary")
        main_frame.pack(fill="both", expand=True)

        # Seção: Identidade
        tb.Label(main_frame, text="IDENTIDADE", font=("Helvetica", 14, "bold"), bootstyle="info").grid(row=0, column=0, columnspan=3, pady=5)
        tb.Label(main_frame, text="Nome:").grid(row=1, column=0, sticky="w", pady=2)
        self.nome_entry = tb.Entry(main_frame)
        self.nome_entry.insert(0, self.ficha["nome"])
        self.nome_entry.grid(row=1, column=1, columnspan=2, sticky="we", pady=2)

        tb.Label(main_frame, text="Classe:").grid(row=2, column=0, sticky="w", pady=2)
        self.classe_entry = tb.Entry(main_frame)
        self.classe_entry.insert(0, self.ficha["classe"])
        self.classe_entry.grid(row=2, column=1, columnspan=2, sticky="we", pady=2)

        # Seção: Atributos
        tb.Label(main_frame, text="ATRIBUTOS", font=("Helvetica", 14, "bold"), bootstyle="info").grid(row=3, column=0, columnspan=3, pady=5)
        self.hab_label = tb.Label(main_frame, text=f"Habilidade: {self.ficha['habilidade']}", bootstyle="primary")
        self.hab_label.grid(row=4, column=0, sticky="w", pady=2)
        tb.Button(main_frame, text="+", bootstyle=SUCCESS, command=lambda: self.change_attr("habilidade", 1)).grid(row=4, column=1)
        tb.Button(main_frame, text="-", bootstyle=DANGER, command=lambda: self.change_attr("habilidade", -1)).grid(row=4, column=2)

        self.ene_label = tb.Label(main_frame, text=f"Energia: {self.ficha['energia']}", bootstyle="primary")
        self.ene_label.grid(row=5, column=0, sticky="w", pady=2)
        tb.Button(main_frame, text="+", bootstyle=SUCCESS, command=lambda: self.change_attr("energia", 1)).grid(row=5, column=1)
        tb.Button(main_frame, text="-", bootstyle=DANGER, command=lambda: self.change_attr("energia", -1)).grid(row=5, column=2)

        self.sor_label = tb.Label(main_frame, text=f"Sorte: {self.ficha['sorte']}", bootstyle="primary")
        self.sor_label.grid(row=6, column=0, sticky="w", pady=2)
        tb.Button(main_frame, text="+", bootstyle=SUCCESS, command=lambda: self.change_attr("sorte", 1)).grid(row=6, column=1)
        tb.Button(main_frame, text="-", bootstyle=DANGER, command=lambda: self.change_attr("sorte", -1)).grid(row=6, column=2)

        self.ouro_label = tb.Label(main_frame, text=f"Ouro: {self.ficha['ouro']}", bootstyle="primary")
        self.ouro_label.grid(row=7, column=0, sticky="w", pady=2)
        tb.Button(main_frame, text="+", bootstyle=SUCCESS, command=lambda: self.change_attr("ouro", 1)).grid(row=7, column=1)
        tb.Button(main_frame, text="-", bootstyle=DANGER, command=lambda: self.change_attr("ouro", -1)).grid(row=7, column=2)

        # Seção: Inventário
        tb.Label(main_frame, text="INVENTÁRIO", font=("Helvetica", 14, "bold"), bootstyle="warning").grid(row=8, column=0, columnspan=3, pady=5)
        self.inventario_listbox = tb.Listbox(main_frame, height=6, bootstyle="secondary")
        self.inventario_listbox.grid(row=9, column=0, columnspan=2, sticky="we", pady=2)
        tb.Button(main_frame, text="Adicionar Item", bootstyle=INFO, command=self.add_item).grid(row=9, column=2, pady=2)
        tb.Button(main_frame, text="Remover Item", bootstyle=WARNING, command=self.remove_item).grid(row=10, column=2, pady=2)

        # Seção: Anotações
        tb.Label(main_frame, text="ANOTAÇÕES", font=("Helvetica", 14, "bold"), bootstyle="secondary").grid(row=11, column=0, columnspan=3, pady=5)
        self.anotacoes_text = tb.Text(main_frame, height=6, width=50, bg="#fdf6e3", fg="#000000", relief="solid", borderwidth=2)
        self.anotacoes_text.insert("1.0", self.ficha["anotacoes"])
        self.anotacoes_text.grid(row=12, column=0, columnspan=3, pady=5)

        # Seção: Dados e Combate
        tb.Label(main_frame, text="AÇÃO", font=("Helvetica", 14, "bold"), bootstyle="danger").grid(row=13, column=0, columnspan=3, pady=5)
        tb.Button(main_frame, text="Rolar 1D6", bootstyle=SECONDARY, command=lambda: self.roll_dice(1)).grid(row=14, column=0, pady=3)
        tb.Button(main_frame, text="Rolar 2D6", bootstyle=SECONDARY, command=lambda: self.roll_dice(2)).grid(row=14, column=1, pady=3)
        tb.Button(main_frame, text="Combate!", bootstyle=DANGER, command=self.combat).grid(row=14, column=2, pady=3)

        # Seção: Salvar / Carregar
        tb.Label(main_frame, text="GERENCIAR FICHA", font=("Helvetica", 14, "bold"), bootstyle="info").grid(row=15, column=0, columnspan=3, pady=5)
        tb.Button(main_frame, text="Salvar Ficha", bootstyle=SUCCESS, command=self.save_ficha).grid(row=16, column=0, pady=5)
        tb.Button(main_frame, text="Carregar Ficha", bootstyle=INFO, command=self.load_ficha).grid(row=16, column=1, pady=5)

    # Funções do jogo
    def change_attr(self, attr, value):
        self.ficha[attr] += value
        if attr == "habilidade": self.hab_label.config(text=f"Habilidade: {self.ficha['habilidade']}")
        elif attr == "energia": self.ene_label.config(text=f"Energia: {self.ficha['energia']}")
        elif attr == "sorte": self.sor_label.config(text=f"Sorte: {self.ficha['sorte']}")
        elif attr == "ouro": self.ouro_label.config(text=f"Ouro: {self.ficha['ouro']}")

    def add_item(self):
        item = simpledialog.askstring("Inventário", "Digite o nome do item:")
        if item:
            self.ficha["inventario"].append(item)
            self.inventario_listbox.insert(END, item)

    def remove_item(self):
        sel = self.inventario_listbox.curselection()
        if sel:
            idx = sel[0]
            item = self.inventario_listbox.get(idx)
            self.ficha["inventario"].remove(item)
            self.inventario_listbox.delete(idx)

    def roll_dice(self, qtd):
        resultado = sum(random.randint(1,6) for _ in range(qtd))
        messagebox.showinfo("Dado", f"Você rolou {qtd}D6 e obteve: {resultado}")
        return resultado

    def combat(self):
        inimigo_hab = simpledialog.askinteger("Combate", "Habilidade do inimigo:", minvalue=1, maxvalue=12)
        if inimigo_hab is None: return
        inimigo_ene = simpledialog.askinteger("Combate", "Energia do inimigo:", minvalue=1, maxvalue=30)
        if inimigo_ene is None: return
        while inimigo_ene > 0 and self.ficha["energia"] > 0:
            atk_j = self.roll_dice(2) + self.ficha["habilidade"]
            atk_i = self.roll_dice(2) + inimigo_hab
            if atk_j > atk_i: inimigo_ene -= 2; messagebox.showinfo("Combate", f"Você atingiu o inimigo! Energia do inimigo: {inimigo_ene}")
            elif atk_i > atk_j: self.ficha["energia"] -= 2; self.ene_label.config(text=f"Energia: {self.ficha['energia']}"); messagebox.showinfo("Combate", f"O inimigo atingiu você! Sua Energia: {self.ficha['energia']}")
            else: messagebox.showinfo("Combate", "Empate! Ninguém foi ferido.")
        if self.ficha["energia"] <= 0: messagebox.showerror("Derrota", "Você foi derrotado!")
        else: messagebox.showinfo("Vitória", "Você derrotou o inimigo!")

    def save_ficha(self):
        self.ficha["nome"] = self.nome_entry.get()
        self.ficha["classe"] = self.classe_entry.get()
        self.ficha["anotacoes"] = self.anotacoes_text.get("1.0", "end").strip()
        with open("ficha.json","w",encoding="utf-8") as f:
            json.dump(self.ficha,f,indent=4,ensure_ascii=False)
        messagebox.showinfo("Salvar","Ficha salva em ficha.json")

    def load_ficha(self):
        try:
            with open("ficha.json","r",encoding="utf-8") as f:
                self.ficha = json.load(f)
            self.nome_entry.delete(0,"end"); self.nome_entry.insert(0,self.ficha["nome"])
            self.classe_entry.delete(0,"end"); self.classe_entry.insert(0,self.ficha["classe"])
            self.hab_label.config(text=f"Habilidade: {self.ficha['habilidade']}")
            self.ene_label.config(text=f"Energia: {self.ficha['energia']}")
            self.sor_label.config(text=f"Sorte: {self.ficha['sorte']}")
            self.ouro_label.config(text=f"Ouro: {self.ficha['ouro']}")
            self.inventario_listbox.delete(0,"end")
            for item in self.ficha["inventario"]: self.inventario_listbox.insert("end",item)
            self.anotacoes_text.delete("1.0","end")
            self.anotacoes_text.insert("1.0",self.ficha["anotacoes"])
            messagebox.showinfo("Carregar","Ficha carregada com sucesso!")
        except FileNotFoundError:
            messagebox.showerror("Erro","Nenhum arquivo de ficha encontrado.")


if __name__ == "__main__":
    root = tb.Window()
    app = RPGFichaApp(root)
    root.mainloop()
