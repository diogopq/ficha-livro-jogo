from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QTextEdit, QListWidget, QInputDialog, QMessageBox, QProgressBar,
    QTableWidget, QTableWidgetItem, QComboBox
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QIcon, QFont
import sys, random, json, os

# -------------------- UTILIDADES --------------------
def resource_path(relative_path):
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# -------------------- CLASSE PRINCIPAL --------------------
class RPGFichaModerna(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ficha RPG Moderna")
        self.setMinimumSize(1400,750)
        self.ficha = {
            "nome":"Aventureiro","classe":"Guerreiro",
            "forca":10,"energia":20,"sorte":10,"ouro":0,
            "inventario":{"armas":[],"defesas":[],"itens":[]},"anotacoes":"","ultimo_dado":0
        }

        # Ícones
        self.icons = {
            "sword": QIcon(resource_path("icons/sword.png")),
            "dice": QIcon(resource_path("icons/dice.png")),
            "backpack": QIcon(resource_path("icons/backpack.png")),
            "coin": QIcon(resource_path("icons/coin.png"))
        }

        self.init_ui()

    # -------------------- INTERFACE --------------------
    def init_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setSpacing(15)

        # Colunas horizontais
        col1 = QVBoxLayout(); col1.setAlignment(Qt.AlignTop)
        col2 = QVBoxLayout(); col2.setAlignment(Qt.AlignTop)
        col3 = QVBoxLayout(); col3.setAlignment(Qt.AlignTop)

        # Construção das seções
        self.create_identity_card(col1)
        self.create_attributes_card(col1)
        self.create_inventory_card(col2)
        self.create_notes_card(col2)
        self.create_dice_card(col3)
        self.create_battle_card(col3)
        self.create_manage_card(col3)

        main_layout.addLayout(col1, 3)
        main_layout.addLayout(col2, 3)
        main_layout.addLayout(col3, 3)

    # -------------------- CARDS --------------------
    def create_identity_card(self, layout):
        card = QWidget()
        card.setStyleSheet("background:#2e2e3f; border-radius:12px; padding:15px;")
        vbox = QVBoxLayout(card)
        lbl_title = QLabel("IDENTIDADE"); lbl_title.setFont(QFont("Helvetica",16,QFont.Bold))
        lbl_title.setStyleSheet("color:#f1c40f;")
        vbox.addWidget(lbl_title)

        vbox.addWidget(QLabel("Nome:"))
        self.nome_entry = QLineEdit(self.ficha["nome"])
        self.nome_entry.setStyleSheet(
            "background:#1e1e2f; color:#ecf0f1; font-size:16px; padding:5px; border-radius:6px;"
        )
        self.nome_entry.setFixedHeight(35)
        vbox.addWidget(self.nome_entry)

        vbox.addWidget(QLabel("Classe:"))
        self.classe_entry = QLineEdit(self.ficha["classe"])
        self.classe_entry.setStyleSheet(
            "background:#1e1e2f; color:#ecf0f1; font-size:16px; padding:5px; border-radius:6px;"
        )
        self.classe_entry.setFixedHeight(35)
        vbox.addWidget(self.classe_entry)
        layout.addWidget(card)

    def create_attributes_card(self, layout):
        card = QWidget()
        card.setStyleSheet("background:#2e2e3f; border-radius:12px; padding:15px;")
        vbox = QVBoxLayout(card)
        lbl_title = QLabel("ATRIBUTOS"); lbl_title.setFont(QFont("Helvetica",16,QFont.Bold))
        lbl_title.setStyleSheet("color:#3498db;")
        vbox.addWidget(lbl_title)
        self.attr_widgets = {}
        for attr,color in [("forca","#3498db"),("energia","#e74c3c"),("sorte","#2ecc71"),("ouro","#f1c40f")]:
            row = QHBoxLayout()
            lbl = QLabel(attr.capitalize()+":"); lbl.setMinimumWidth(80); lbl.setStyleSheet("color:white;")
            val_lbl = QLabel(str(self.ficha[attr])); val_lbl.setFont(QFont("Helvetica",14))
            btn_inc = QPushButton("+"); btn_inc.setFixedWidth(35)
            btn_inc.setStyleSheet("background:#1abc9c; color:white; font-weight:bold;")
            btn_inc.clicked.connect(lambda checked, a=attr: self.change_attr(a,1))
            btn_dec = QPushButton("-"); btn_dec.setFixedWidth(35)
            btn_dec.setStyleSheet("background:#e67e22; color:white; font-weight:bold;")
            btn_dec.clicked.connect(lambda checked, a=attr: self.change_attr(a,-1))
            row.addWidget(lbl)
            row.addWidget(val_lbl)
            row.addWidget(btn_inc)
            row.addWidget(btn_dec)
            vbox.addLayout(row)
            self.attr_widgets[attr] = val_lbl
        layout.addWidget(card)

    def create_inventory_card(self, layout):
        card = QWidget(); card.setStyleSheet("background:#2e2e3f; border-radius:12px; padding:15px;")
        vbox = QVBoxLayout(card)
        lbl_title = QLabel("INVENTÁRIO"); lbl_title.setFont(QFont("Helvetica",16,QFont.Bold))
        lbl_title.setStyleSheet("color:#9b59b6;")
        vbox.addWidget(lbl_title)

        # Tabela armas
        lbl_armas = QLabel("ARMAS"); lbl_armas.setStyleSheet("color:#ecf0f1; font-weight:bold;")
        vbox.addWidget(lbl_armas)
        self.table_armas = QTableWidget(); self.table_armas.setColumnCount(2)
        self.table_armas.setHorizontalHeaderLabels(["Nome","Dano"])
        self.table_armas.setStyleSheet("background:#1e1e2f; color:#ecf0f1;")
        vbox.addWidget(self.table_armas)
        row_buttons = QHBoxLayout()
        btn_add_arma = QPushButton("Adicionar Arma"); btn_add_arma.clicked.connect(lambda:self.add_item_table("armas"))
        btn_add_arma.setStyleSheet("background:#1abc9c; color:white;")
        btn_rem_arma = QPushButton("Remover Arma"); btn_rem_arma.clicked.connect(lambda:self.remove_item_table("armas"))
        btn_rem_arma.setStyleSheet("background:#e74c3c; color:white;")
        row_buttons.addWidget(btn_add_arma); row_buttons.addWidget(btn_rem_arma)
        vbox.addLayout(row_buttons)

        # Tabela defesas
        lbl_def = QLabel("DEFESAS"); lbl_def.setStyleSheet("color:#ecf0f1; font-weight:bold;")
        vbox.addWidget(lbl_def)
        self.table_defesas = QTableWidget(); self.table_defesas.setColumnCount(2)
        self.table_defesas.setHorizontalHeaderLabels(["Nome","Defesa"])
        self.table_defesas.setStyleSheet("background:#1e1e2f; color:#ecf0f1;")
        vbox.addWidget(self.table_defesas)
        row_buttons_def = QHBoxLayout()
        btn_add_def = QPushButton("Adicionar Defesa"); btn_add_def.clicked.connect(lambda:self.add_item_table("defesas"))
        btn_add_def.setStyleSheet("background:#1abc9c; color:white;")
        btn_rem_def = QPushButton("Remover Defesa"); btn_rem_def.clicked.connect(lambda:self.remove_item_table("defesas"))
        btn_rem_def.setStyleSheet("background:#e74c3c; color:white;")
        row_buttons_def.addWidget(btn_add_def); row_buttons_def.addWidget(btn_rem_def)
        vbox.addLayout(row_buttons_def)

        # Lista itens
        lbl_itens = QLabel("ITENS"); lbl_itens.setStyleSheet("color:#ecf0f1; font-weight:bold;")
        vbox.addWidget(lbl_itens)
        self.list_itens = QListWidget(); self.list_itens.setStyleSheet("background:#1e1e2f; color:#ecf0f1;")
        vbox.addWidget(self.list_itens)
        row_buttons_itens = QHBoxLayout()
        btn_add_item = QPushButton("Adicionar Item"); btn_add_item.clicked.connect(lambda:self.add_item_generic("itens"))
        btn_add_item.setStyleSheet("background:#1abc9c; color:white;")
        btn_rem_item = QPushButton("Remover Item"); btn_rem_item.clicked.connect(lambda:self.remove_item_list("itens"))
        btn_rem_item.setStyleSheet("background:#e74c3c; color:white;")
        row_buttons_itens.addWidget(btn_add_item); row_buttons_itens.addWidget(btn_rem_item)
        vbox.addLayout(row_buttons_itens)

        # Combo para selecionar arma
        self.combo_armas = QComboBox(); self.combo_armas.setStyleSheet("background:#1e1e2f; color:#ecf0f1;")
        vbox.addWidget(self.combo_armas)

        layout.addWidget(card)

    # -------------------- NOTAS --------------------
    def create_notes_card(self, layout):
        card = QWidget(); card.setStyleSheet("background:#2e2e3f; border-radius:12px; padding:15px;")
        vbox = QVBoxLayout(card)
        lbl_title = QLabel("ANOTAÇÕES"); lbl_title.setFont(QFont("Helvetica",16,QFont.Bold))
        lbl_title.setStyleSheet("color:#e67e22;")
        vbox.addWidget(lbl_title)
        self.notes_text = QTextEdit(); self.notes_text.setText(self.ficha["anotacoes"])
        self.notes_text.setStyleSheet("background:#1e1e2f; color:#ecf0f1; border-radius:6px; padding:5px; font-size:14px;")
        vbox.addWidget(self.notes_text)
        layout.addWidget(card)

    # -------------------- DADOS --------------------
    def create_dice_card(self, layout):
        card = QWidget(); card.setStyleSheet("background:#2e2e3f; border-radius:12px; padding:15px;")
        vbox = QVBoxLayout(card)
        lbl_title = QLabel("ROLAGEM DE DADOS"); lbl_title.setFont(QFont("Helvetica",16,QFont.Bold))
        lbl_title.setStyleSheet("color:#1abc9c;")
        vbox.addWidget(lbl_title)
        self.dice_label = QLabel("🎲"); self.dice_label.setAlignment(Qt.AlignCenter); self.dice_label.setFont(QFont("Helvetica",40))
        vbox.addWidget(self.dice_label)
        btn_row = QHBoxLayout()
        for i in [1,2,3]:
            btn = QPushButton(f"{i}D6"); btn.clicked.connect(lambda checked, q=i: self.roll_dice(q))
            btn_row.addWidget(btn)
        vbox.addLayout(btn_row)
        layout.addWidget(card)

    def roll_dice(self,qtd):
        self.dice_value = 0
        self.roll_count = 0
        self.roll_total = qtd
        self.timer = QTimer(); self.timer.timeout.connect(self.update_dice_animation); self.timer.start(150)

    def update_dice_animation(self):
        self.roll_count += 1
        val = sum(random.randint(1,6) for _ in range(self.roll_total))
        self.dice_label.setText(f"{val} 🎲")
        if self.roll_count >=10:
            self.timer.stop()
            self.ficha["ultimo_dado"] = val

    # -------------------- BATALHA --------------------
    def create_battle_card(self, layout):
        card = QWidget()
        card.setStyleSheet("background:#2e2e3f; border-radius:12px; padding:15px;")  # Dark mode
        vbox = QVBoxLayout(card)
        lbl_title = QLabel("BATALHAS")
        lbl_title.setFont(QFont("Helvetica",16,QFont.Bold))
        lbl_title.setStyleSheet("color:#f39c12;")
        vbox.addWidget(lbl_title)

        # Labels e Inputs inimigo
        hbox1 = QHBoxLayout()
        
        col_name = QVBoxLayout()
        col_name.addWidget(QLabel("Nome")); self.enemy_name = QLineEdit(); self.enemy_name.setPlaceholderText("Nome do inimigo")
        col_name.addWidget(self.enemy_name)
        
        col_forca = QVBoxLayout()
        col_forca.addWidget(QLabel("Força")); self.enemy_forca = QLineEdit(); self.enemy_forca.setPlaceholderText("Força")
        col_forca.addWidget(self.enemy_forca)
        
        col_defesa = QVBoxLayout()
        col_defesa.addWidget(QLabel("Defesa")); self.enemy_defesa = QLineEdit(); self.enemy_defesa.setPlaceholderText("Defesa")
        col_defesa.addWidget(self.enemy_defesa)
        
        col_dano = QVBoxLayout()
        col_dano.addWidget(QLabel("Dano")); self.enemy_dano = QLineEdit(); self.enemy_dano.setPlaceholderText("Dano")
        col_dano.addWidget(self.enemy_dano)
        
        col_ene = QVBoxLayout()
        col_ene.addWidget(QLabel("Energia")); self.enemy_ene = QLineEdit(); self.enemy_ene.setPlaceholderText("Energia")
        col_ene.addWidget(self.enemy_ene)
        
        for w in [self.enemy_name,self.enemy_forca,self.enemy_defesa,self.enemy_dano,self.enemy_ene]:
            w.setStyleSheet("background:#1e1e2f; color:#ecf0f1; padding:5px; border-radius:6px;")
        
        hbox1.addLayout(col_name)
        hbox1.addLayout(col_forca)
        hbox1.addLayout(col_defesa)
        hbox1.addLayout(col_dano)
        hbox1.addLayout(col_ene)
        
        vbox.addLayout(hbox1)

        # Barra de energia inimigo
        self.enemy_bar = QProgressBar()
        self.enemy_bar.setMaximum(30)
        self.enemy_bar.setValue(0)
        self.enemy_bar.setStyleSheet("""
            QProgressBar {
                border:2px solid #7f8c8d;
                border-radius:5px;
                text-align:center;
                background:#34495e;
                color:#ecf0f1;
            }
            QProgressBar::chunk {background:#e74c3c;}
        """)
        vbox.addWidget(self.enemy_bar)

        # Histórico de combate
        self.battle_log = QTextEdit()
        self.battle_log.setReadOnly(True)
        self.battle_log.setStyleSheet("background:#1e1e2f; color:#ecf0f1; border-radius:6px; padding:5px; font-size:14px;")
        vbox.addWidget(self.battle_log)

        # Botões batalha
        hbox2 = QHBoxLayout()
        btn_start = QPushButton("Iniciar Combate")
        btn_start.setStyleSheet("background:#2980b9; color:white; font-weight:bold; border-radius:6px; padding:5px;")
        btn_start.clicked.connect(self.start_battle)
        
        btn_attack = QPushButton("Atacar")
        btn_attack.setStyleSheet("background:#c0392b; color:white; font-weight:bold; border-radius:6px; padding:5px;")
        btn_attack.clicked.connect(self.attack_enemy)
        
        hbox2.addWidget(btn_start)
        hbox2.addWidget(btn_attack)
        vbox.addLayout(hbox2)

        layout.addWidget(card)

    def start_battle(self):
        try:
            forca=int(self.enemy_forca.text()); defesa=int(self.enemy_defesa.text())
            ene=int(self.enemy_ene.text())
            self.enemy_max = ene
            self.enemy_bar.setMaximum(ene); self.enemy_bar.setValue(ene)
            self.enemy_bar.setFormat(f"{self.enemy_name.text()} : {ene}/{ene}")
            self.battle_log.clear()
            self.battle_log.append(f"=== Combate iniciado contra {self.enemy_name.text()} ===\n")
        except:
            QMessageBox.warning(self,"Erro","Preencha corretamente os dados do inimigo!")

    def attack_enemy(self):
        if not hasattr(self,"enemy_max") or not self.ficha["inventario"]["armas"]: 
            return
        
        arma_idx = self.combo_armas.currentIndex()
        arma = self.ficha["inventario"]["armas"][arma_idx]

        log = ""  # String para detalhar cada passo

        # Ataque do jogador
        atk = random.randint(1,6) * self.ficha["forca"]
        defesa_inimigo = random.randint(1,6) * int(self.enemy_defesa.text())
        log += f"=== ATAQUE DO JOGADOR ===\n"
        log += f"Ataque do jogador ({arma['nome']}): {atk}\n"
        log += f"Defesa do inimigo: {defesa_inimigo}\n"

        if atk > defesa_inimigo:
            dano_causado = arma["dano"]
            new_val = max(0, self.enemy_bar.value() - dano_causado)
            self.enemy_bar.setValue(new_val)
            self.enemy_bar.setFormat(f"{self.enemy_name.text()} : {new_val}/{self.enemy_max}")
            log += f"Resultado: Ataque bem-sucedido! Dano causado: {dano_causado}\n"
        else:
            log += "Resultado: Inimigo defendeu!\n"

        # Ataque do inimigo
        atk_inimigo = random.randint(1,6) * int(self.enemy_forca.text())
        defesa_jogador = random.randint(1,6) * self.ficha["forca"]
        log += f"\n=== ATAQUE DO INIMIGO ===\n"
        log += f"Ataque do inimigo: {atk_inimigo}\n"
        log += f"Defesa do jogador: {defesa_jogador}\n"

        if atk_inimigo > defesa_jogador:
            dano_recebido = int(self.enemy_dano.text())
            self.change_attr("energia", -dano_recebido)
            log += f"Resultado: Você sofreu dano! Energia perdida: {dano_recebido}\n"
        else:
            log += "Resultado: Inimigo errou!\n"

        # Resultado final da rodada
        log += f"\n=== ESTADO FINAL ===\n"
        log += f"Energia do jogador: {self.ficha['energia']}\n"
        log += f"Energia do inimigo: {self.enemy_bar.value()}/{self.enemy_max}\n"
        log += "---------------------------\n"

        # Adiciona ao histórico
        self.battle_log.append(log)

        # Checagem de vitória/derrota
        if self.enemy_bar.value() == 0:
            self.battle_log.append("Vitória! Inimigo derrotado!\n")
        if self.ficha["energia"] == 0:
            self.battle_log.append("Derrota! Você foi derrotado!\n")

    # -------------------- CONTROLE --------------------
    def create_manage_card(self, layout):
        card = QWidget(); card.setStyleSheet("background:#2e2e3f; border-radius:12px; padding:15px;")
        vbox = QVBoxLayout(card)
        lbl_title = QLabel("CONTROLE"); lbl_title.setFont(QFont("Helvetica",16,QFont.Bold))
        lbl_title.setStyleSheet("color:#e74c3c;")
        vbox.addWidget(lbl_title)
        btn_save = QPushButton("Salvar Ficha"); btn_save.clicked.connect(self.save_ficha)
        btn_save.setStyleSheet("background:#1abc9c; color:white;")
        btn_load = QPushButton("Carregar Ficha"); btn_load.clicked.connect(self.load_ficha)
        btn_load.setStyleSheet("background:#2980b9; color:white;")
        vbox.addWidget(btn_save); vbox.addWidget(btn_load)
        layout.addWidget(card)

    def save_ficha(self):
        self.ficha["nome"] = self.nome_entry.text()
        self.ficha["classe"] = self.classe_entry.text()
        self.ficha["anotacoes"] = self.notes_text.toPlainText()
        with open("ficha.json","w") as f: json.dump(self.ficha,f,indent=4)
        QMessageBox.information(self,"Salvo","Ficha salva com sucesso!")

    def load_ficha(self):
        try:
            with open("ficha.json","r") as f: self.ficha = json.load(f)
            self.nome_entry.setText(self.ficha["nome"]); self.classe_entry.setText(self.ficha["classe"])
            self.notes_text.setText(self.ficha["anotacoes"])
            for attr in ["forca","energia","sorte","ouro"]: self.attr_widgets[attr].setText(str(self.ficha[attr]))
            self.refresh_tables()
        except:
            QMessageBox.warning(self,"Erro","Não foi possível carregar a ficha!")

    # -------------------- UTILITÁRIOS --------------------
    def change_attr(self,attr,val):
        self.ficha[attr] += val; self.ficha[attr] = max(0,self.ficha[attr])
        self.attr_widgets[attr].setText(str(self.ficha[attr]))

    def add_item_table(self,tipo):
        nome,ok = QInputDialog.getText(self,"Adicionar","Nome:")
        if not ok or not nome: return
        dano,ok2 = QInputDialog.getInt(self,"Adicionar","Valor:",1,1,100)
        if not ok2: return
        self.ficha["inventario"][tipo].append({"nome":nome,"dano":dano})
        self.refresh_tables()

    def remove_item_table(self,tipo):
        table = self.table_armas if tipo=="armas" else self.table_defesas
        idx = table.currentRow(); 
        if idx>=0: del self.ficha["inventario"][tipo][idx]; self.refresh_tables()

    def add_item_generic(self,tipo):
        nome,ok = QInputDialog.getText(self,"Adicionar Item","Nome:")
        if not ok or not nome: return
        self.ficha["inventario"][tipo].append(nome)
        self.refresh_tables()

    def remove_item_list(self,tipo):
        listw = self.list_itens
        idx = listw.currentRow(); 
        if idx>=0: del self.ficha["inventario"][tipo][idx]; self.refresh_tables()

    def refresh_tables(self):
        # armas
        self.table_armas.setRowCount(len(self.ficha["inventario"]["armas"]))
        self.combo_armas.clear()
        for i,row in enumerate(self.ficha["inventario"]["armas"]):
            self.table_armas.setItem(i,0,QTableWidgetItem(row["nome"]))
            self.table_armas.setItem(i,1,QTableWidgetItem(str(row["dano"])))
            self.combo_armas.addItem(row["nome"])
        # defesas
        self.table_defesas.setRowCount(len(self.ficha["inventario"]["defesas"]))
        for i,row in enumerate(self.ficha["inventario"]["defesas"]):
            self.table_defesas.setItem(i,0,QTableWidgetItem(row["nome"]))
            self.table_defesas.setItem(i,1,QTableWidgetItem(str(row["dano"])))
        # itens
        self.list_itens.clear()
        for itm in self.ficha["inventario"]["itens"]: self.list_itens.addItem(itm)

# -------------------- EXECUÇÃO --------------------
if __name__=="__main__":
    app = QApplication(sys.argv)
    janela = RPGFichaModerna()
    janela.show()
    sys.exit(app.exec())
