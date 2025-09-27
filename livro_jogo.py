import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import messagebox
from PIL import Image, ImageTk
import random, sys, os

def resource_path(relative_path):
    """Retorna o caminho absoluto para recursos, funciona no PyInstaller."""
    try:
        # Quando executável gerado pelo PyInstaller
        base_path = sys._MEIPASS
    except Exception:
        # Quando rodando como script Python
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def load_icon(path):
    """Carrega ícone de arquivo e redimensiona para 25x25."""
    image = Image.open(path)
    return ImageTk.PhotoImage(image.resize((25, 25)))

class LivroJogoRPG:

    def __init__(self, root):
        self.root = root
        self.root.title("Livro-Jogo RPG Épico")
        self.root.geometry("800x950")
        self.style = tb.Style(theme="darkly")

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

        # Carregar ícones usando resource_path
        self.load_icons(
            sword_path=resource_path("icons/sword.png"),
            dice_path=resource_path("icons/dice.png"),
            backpack_path=resource_path("icons/backpack.png"),
            coin_path=resource_path("icons/coin.png")
        )

        self.create_widgets()
        self.story_index = 0
        self.story_steps = self.create_story()
        self.show_story()

    def load_icons(self, sword_path, dice_path, backpack_path, coin_path):
        self.icone_espada = load_icon(sword_path)
        self.icone_dado = load_icon(dice_path)
        self.icone_mochila = load_icon(backpack_path)
        self.icone_ouro = load_icon(coin_path)

    def create_widgets(self):
        self.main = tb.Frame(self.root, padding=10, bootstyle="secondary")
        self.main.pack(fill="both", expand=True)

        tb.Label(self.main, text="FICHA", font=("Helvetica", 16, "bold"), bootstyle="info").grid(row=0, column=0, columnspan=5, pady=5)
        tb.Label(self.main, text="Nome:").grid(row=1, column=0, sticky="w")
        self.nome_entry = tb.Entry(self.main)
        self.nome_entry.insert(0, self.ficha["nome"])
        self.nome_entry.grid(row=1, column=1, columnspan=2, sticky="we")
        tb.Label(self.main, text="Classe:").grid(row=2, column=0, sticky="w")
        self.classe_entry = tb.Entry(self.main)
        self.classe_entry.insert(0, self.ficha["classe"])
        self.classe_entry.grid(row=2, column=1, columnspan=2, sticky="we")

        self.create_attr("Habilidade", "habilidade", 3, SUCCESS)
        self.create_attr("Energia", "energia", 4, DANGER)
        self.create_attr("Sorte", "sorte", 5, PRIMARY)
        self.create_attr("Ouro", "ouro", 6, WARNING)

        tb.Label(self.main, text="HISTÓRIA", font=("Helvetica", 16, "bold"), bootstyle="secondary").grid(row=7, column=0, columnspan=5, pady=5)
        self.story_text = tb.Text(self.main, height=14, width=90, bg="#fdf6e3", fg="#000", relief="solid", borderwidth=2)
        self.story_text.grid(row=8, column=0, columnspan=5, pady=5)

        self.choice_frame = tb.Frame(self.main)
        self.choice_frame.grid(row=9, column=0, columnspan=5, pady=5)

    def create_attr(self, label, attr, row, color):
        tb.Label(self.main, text=label + ":").grid(row=row, column=0, sticky="w")
        bar = tb.Progressbar(self.main, length=220, bootstyle=color, maximum=30 if attr=="energia" else 20)
        bar['value'] = self.ficha[attr]
        bar.grid(row=row, column=1, columnspan=2)
        tb.Button(self.main, text="+", bootstyle=SUCCESS, command=lambda: self.change_attr(attr, 1)).grid(row=row, column=3)
        tb.Button(self.main, text="-", bootstyle=DANGER, command=lambda: self.change_attr(attr, -1)).grid(row=row, column=4)
        setattr(self, f"{attr}_bar", bar)

    def change_attr(self, attr, value):
        self.ficha[attr] += value
        getattr(self, f"{attr}_bar")['value'] = self.ficha[attr]

    def create_story(self):
        steps = []
        for i in range(50):
            steps.append({"texto": f"Seção {i+1}: Um desafio ou oportunidade aparece.", "choices": [("Continuar", "next:{}".format(i+1 if i<49 else "end"))]})
        steps[2]["choices"] = [("Combater Goblin", "combat:goblin:8:6:next:3"), ("Fugir", "next:3")]
        steps[5]["choices"] = [("Abrir baú", "treasure:ouro:20:next:6"), ("Ignorar", "next:6")]
        steps[10]["choices"] = [("Rolar sorte", "roll:sorte:4:success:11:fail:12")]
        steps[15]["choices"] = [("Descansar", "heal:5:next:16"), ("Seguir viagem", "next:16")]
        steps[20]["choices"] = [("Combater Bandido", "combat:bandido:10:8:next:21"), ("Negociar", "roll:sorte:3:success:21:fail:22")]
        steps[30]["choices"] = [("Encontrar Artefato", "treasure:item:Poção Mágica:next:31"), ("Ignorar", "next:31")]
        steps[49]["choices"] = [("Fim da aventura", "end")]
        return steps

    def show_story(self):
        step = self.story_steps[self.story_index]
        self.story_text.delete("1.0", "end")
        self.story_text.insert("1.0", step["texto"])
        for widget in self.choice_frame.winfo_children(): widget.destroy()
        for i, (label, action) in enumerate(step["choices"]):
            tb.Button(self.choice_frame, text=label, bootstyle=INFO, command=lambda a=action: self.process_action(a)).grid(row=0, column=i, padx=5)

    def process_action(self, action):
        parts = action.split(":")
        cmd = parts[0]
        if cmd == "next":
            self.story_index = int(parts[1])
            self.show_story()
        elif cmd == "end":
            messagebox.showinfo("Fim", "Parabéns! Você concluiu a aventura!")
        elif cmd == "heal":
            amt = int(parts[1])
            self.ficha["energia"] += amt
            self.energia_bar['value'] = self.ficha["energia"]
            self.story_index = int(parts[2])
            self.show_story()
        elif cmd == "treasure":
            if parts[1] == "ouro":
                val = int(parts[2])
                self.ficha["ouro"] += val
                self.ouro_bar['value'] = self.ficha["ouro"]
            elif parts[1] == "item":
                item = parts[2]
                self.ficha["inventario"].append(item)
            self.story_index = int(parts[-1])
            self.show_story()
        elif cmd == "roll":
            attr = parts[1]
            target = int(parts[2])
            success = int(parts[4])
            fail = int(parts[6])
            roll = random.randint(1, 6) + self.ficha[attr]
            self.story_index = success if roll >= target else fail
            self.show_story()
        elif cmd == "combat":
            inim = parts[1]
            hab = int(parts[2])
            ene = int(parts[3])
            nxt = int(parts[5])
            atk_j = random.randint(1, 6) + self.ficha["habilidade"]
            atk_i = random.randint(1, 6) + hab
            if atk_j >= atk_i:
                messagebox.showinfo("Combate", f"Você derrotou o {inim}!")
            else:
                self.ficha["energia"] -= 2
                self.energia_bar['value'] = self.ficha["energia"]
            self.story_index = nxt
            self.show_story()


if __name__ == "__main__":
    root = tb.Window()
    app = LivroJogoRPG(root)
    root.mainloop()
