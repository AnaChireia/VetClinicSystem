import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QTabWidget, QMessageBox)
from PyQt6.QtCore import Qt
from views.tutor_tab import TutorTab
from views.pet_tab import PetTab
from views.atendimento_tab import AtendimentoTab
from data.database import create_tables

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Gestão - Clínica Veterinária")
        self.setGeometry(100, 100, 1000, 700)
        
        # Criar tabelas do banco de dados
        create_tables()
        
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        # Criar abas
        tab_widget = QTabWidget()
        
        # Aba de Tutores
        self.tutor_tab = TutorTab()
        tab_widget.addTab(self.tutor_tab, "Tutores")
        
        # Aba de Pets
        self.pet_tab = PetTab()
        tab_widget.addTab(self.pet_tab, "Pets")
        
        # Aba de Atendimentos
        self.atendimento_tab = AtendimentoTab()
        tab_widget.addTab(self.atendimento_tab, "Atendimentos")
        
        layout.addWidget(tab_widget)
        
        # Conectar sinais para atualizar abas quando necessário
        self.tutor_tab.tutor_changed.connect(self.pet_tab.refresh_tutores)
        self.pet_tab.pet_changed.connect(self.atendimento_tab.refresh_pets)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()

