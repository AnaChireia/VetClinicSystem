from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QTableWidget, QTableWidgetItem, QFormLayout, QLineEdit, 
                             QDialog, QDialogButtonBox, QMessageBox, QHeaderView,
                             QComboBox, QFileDialog, QLabel)
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QPixmap
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.pet import Pet
from models.tutor import Tutor

class PetDialog(QDialog):
    def __init__(self, pet=None, parent=None):
        super().__init__(parent)
        self.pet = pet
        self.foto_path = None
        self.setWindowTitle("Cadastro de Pet" if pet is None else "Editar Pet")
        self.setModal(True)
        self.resize(400, 400)
        
        self.init_ui()
        self.load_tutores()
        
        if pet:
            self.load_pet_data()

    def init_ui(self):
        layout = QVBoxLayout()
        
        # Formulário
        form_layout = QFormLayout()
        
        self.nome_edit = QLineEdit()
        
        self.raca_combo = QComboBox()
        self.raca_combo.addItems(Pet.get_racas())
        
        self.tutor_combo = QComboBox()
        
        # Foto
        foto_layout = QHBoxLayout()
        self.foto_button = QPushButton("Selecionar Foto")
        self.foto_label = QLabel("Nenhuma foto selecionada")
        self.foto_button.clicked.connect(self.select_foto)
        foto_layout.addWidget(self.foto_button)
        foto_layout.addWidget(self.foto_label)
        
        form_layout.addRow("Nome:", self.nome_edit)
        form_layout.addRow("Raça:", self.raca_combo)
        form_layout.addRow("Tutor:", self.tutor_combo)
        form_layout.addRow("Foto:", foto_layout)
        
        layout.addLayout(form_layout)
        
        # Botões
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | 
                                   QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        
        layout.addWidget(buttons)
        self.setLayout(layout)

    def load_tutores(self):
        try:
            tutores = Tutor.buscar_todos()
            self.tutor_combo.clear()
            for tutor in tutores:
                self.tutor_combo.addItem(f"{tutor.nome} (ID: {tutor.id})", tutor.id)
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao carregar tutores: {str(e)}")

    def load_pet_data(self):
        self.nome_edit.setText(self.pet.nome)
        
        # Selecionar raça
        index = self.raca_combo.findText(self.pet.raca)
        if index >= 0:
            self.raca_combo.setCurrentIndex(index)
        
        # Selecionar tutor
        for i in range(self.tutor_combo.count()):
            if self.tutor_combo.itemData(i) == self.pet.tutor_id:
                self.tutor_combo.setCurrentIndex(i)
                break
        
        # Foto
        if self.pet.foto_path:
            self.foto_path = self.pet.foto_path
            self.foto_label.setText(os.path.basename(self.foto_path))

    def select_foto(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Selecionar Foto", "", 
            "Imagens (*.png *.jpg *.jpeg *.bmp *.gif)"
        )
        if file_path:
            self.foto_path = file_path
            self.foto_label.setText(os.path.basename(file_path))

    def get_pet_data(self):
        return {
            'nome': self.nome_edit.text().strip(),
            'raca': self.raca_combo.currentText(),
            'tutor_id': self.tutor_combo.currentData(),
            'foto_path': self.foto_path
        }

    def accept(self):
        data = self.get_pet_data()
        
        # Validações
        if not data['nome']:
            QMessageBox.warning(self, "Erro", "Nome é obrigatório!")
            return
        
        if not data['tutor_id']:
            QMessageBox.warning(self, "Erro", "Selecione um tutor!")
            return
        
        super().accept()

class PetTab(QWidget):
    pet_changed = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.load_pets()

    def init_ui(self):
        layout = QVBoxLayout()
        
        # Botões
        button_layout = QHBoxLayout()
        
        self.add_button = QPushButton("Adicionar Pet")
        self.edit_button = QPushButton("Editar")
        self.delete_button = QPushButton("Excluir")
        self.refresh_button = QPushButton("Atualizar")
        
        self.add_button.clicked.connect(self.add_pet)
        self.edit_button.clicked.connect(self.edit_pet)
        self.delete_button.clicked.connect(self.delete_pet)
        self.refresh_button.clicked.connect(self.load_pets)
        
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.edit_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.refresh_button)
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
        
        # Tabela
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Nome", "Raça", "Tutor", "Foto"])
        
        # Configurar redimensionamento das colunas
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        
        layout.addWidget(self.table)
        self.setLayout(layout)

    def load_pets(self):
        try:
            pets = Pet.buscar_todos()
            self.table.setRowCount(len(pets))
            
            for i, pet in enumerate(pets):
                self.table.setItem(i, 0, QTableWidgetItem(str(pet.id)))
                self.table.setItem(i, 1, QTableWidgetItem(pet.nome))
                self.table.setItem(i, 2, QTableWidgetItem(pet.raca))
                self.table.setItem(i, 3, QTableWidgetItem(pet.tutor_nome))
                foto_text = "Sim" if pet.foto_path else "Não"
                self.table.setItem(i, 4, QTableWidgetItem(foto_text))
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao carregar pets: {str(e)}")

    def refresh_tutores(self):
        # Método chamado quando tutores são alterados
        pass

    def add_pet(self):
        dialog = PetDialog(parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            try:
                data = dialog.get_pet_data()
                pet = Pet(data['nome'], data['raca'], data['tutor_id'], data['foto_path'])
                pet.salvar()
                self.load_pets()
                self.pet_changed.emit()
                QMessageBox.information(self, "Sucesso", "Pet cadastrado com sucesso!")
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Erro ao salvar pet: {str(e)}")

    def edit_pet(self):
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Aviso", "Selecione um pet para editar!")
            return
        
        pet_id = int(self.table.item(current_row, 0).text())
        pet = Pet.buscar_por_id(pet_id)
        
        if pet:
            dialog = PetDialog(pet, parent=self)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                try:
                    data = dialog.get_pet_data()
                    pet.nome = data['nome']
                    pet.raca = data['raca']
                    pet.tutor_id = data['tutor_id']
                    pet.foto_path = data['foto_path']
                    pet.salvar()
                    self.load_pets()
                    self.pet_changed.emit()
                    QMessageBox.information(self, "Sucesso", "Pet atualizado com sucesso!")
                except Exception as e:
                    QMessageBox.critical(self, "Erro", f"Erro ao atualizar pet: {str(e)}")

    def delete_pet(self):
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Aviso", "Selecione um pet para excluir!")
            return
        
        pet_id = int(self.table.item(current_row, 0).text())
        pet_nome = self.table.item(current_row, 1).text()
        
        reply = QMessageBox.question(self, "Confirmar Exclusão", 
                                     f"Deseja realmente excluir o pet '{pet_nome}'?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                pet = Pet.buscar_por_id(pet_id)
                if pet:
                    pet.deletar()
                    self.load_pets()
                    self.pet_changed.emit()
                    QMessageBox.information(self, "Sucesso", "Pet excluído com sucesso!")
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Erro ao excluir pet: {str(e)}")

