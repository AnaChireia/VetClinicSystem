from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QTableWidget, QTableWidgetItem, QFormLayout, QLineEdit, 
                             QDialog, QDialogButtonBox, QMessageBox, QHeaderView)
from PyQt6.QtCore import pyqtSignal
import re
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.tutor import Tutor

class TutorDialog(QDialog):
    def __init__(self, tutor=None, parent=None):
        super().__init__(parent)
        self.tutor = tutor
        self.setWindowTitle("Cadastro de Tutor" if tutor is None else "Editar Tutor")
        self.setModal(True)
        self.resize(400, 300)
        
        self.init_ui()
        
        if tutor:
            self.load_tutor_data()

    def init_ui(self):
        layout = QVBoxLayout()
        
        # Formulário
        form_layout = QFormLayout()
        
        self.nome_edit = QLineEdit()
        self.cpf_edit = QLineEdit()
        self.cpf_edit.setInputMask("999.999.999-99")
        self.telefone_edit = QLineEdit()
        self.telefone_edit.setInputMask("(99) 99999-9999")
        self.email_edit = QLineEdit()
        
        form_layout.addRow("Nome:", self.nome_edit)
        form_layout.addRow("CPF:", self.cpf_edit)
        form_layout.addRow("Telefone:", self.telefone_edit)
        form_layout.addRow("Email:", self.email_edit)
        
        layout.addLayout(form_layout)
        
        # Botões
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | 
                                   QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        
        layout.addWidget(buttons)
        self.setLayout(layout)

    def load_tutor_data(self):
        self.nome_edit.setText(self.tutor.nome)
        self.cpf_edit.setText(self.tutor.cpf)
        self.telefone_edit.setText(self.tutor.telefone)
        self.email_edit.setText(self.tutor.email)

    def get_tutor_data(self):
        return {
            'nome': self.nome_edit.text().strip(),
            'cpf': re.sub(r'\D', '', self.cpf_edit.text()),
            'telefone': self.telefone_edit.text().strip(),
            'email': self.email_edit.text().strip()
        }

    def accept(self):
        data = self.get_tutor_data()
        
        # Validações
        if not data['nome']:
            QMessageBox.warning(self, "Erro", "Nome é obrigatório!")
            return
        
        if not Tutor.validar_cpf(data['cpf']):
            QMessageBox.warning(self, "Erro", "CPF inválido!")
            return
        
        if not Tutor.validar_email(data['email']):
            QMessageBox.warning(self, "Erro", "Email inválido!")
            return
        
        super().accept()

class TutorTab(QWidget):
    tutor_changed = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.load_tutores()

    def init_ui(self):
        layout = QVBoxLayout()
        
        # Botões
        button_layout = QHBoxLayout()
        
        self.add_button = QPushButton("Adicionar Tutor")
        self.edit_button = QPushButton("Editar")
        self.delete_button = QPushButton("Excluir")
        self.refresh_button = QPushButton("Atualizar")
        
        self.add_button.clicked.connect(self.add_tutor)
        self.edit_button.clicked.connect(self.edit_tutor)
        self.delete_button.clicked.connect(self.delete_tutor)
        self.refresh_button.clicked.connect(self.load_tutores)
        
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.edit_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.refresh_button)
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
        
        # Tabela
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Nome", "CPF", "Telefone", "Email"])
        
        # Configurar redimensionamento das colunas
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)
        
        layout.addWidget(self.table)
        self.setLayout(layout)

    def load_tutores(self):
        try:
            tutores = Tutor.buscar_todos()
            self.table.setRowCount(len(tutores))
            
            for i, tutor in enumerate(tutores):
                self.table.setItem(i, 0, QTableWidgetItem(str(tutor.id)))
                self.table.setItem(i, 1, QTableWidgetItem(tutor.nome))
                self.table.setItem(i, 2, QTableWidgetItem(tutor.cpf))
                self.table.setItem(i, 3, QTableWidgetItem(tutor.telefone))
                self.table.setItem(i, 4, QTableWidgetItem(tutor.email))
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao carregar tutores: {str(e)}")

    def add_tutor(self):
        dialog = TutorDialog(parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            try:
                data = dialog.get_tutor_data()
                tutor = Tutor(data['nome'], data['cpf'], data['telefone'], data['email'])
                tutor.salvar()
                self.load_tutores()
                self.tutor_changed.emit()
                QMessageBox.information(self, "Sucesso", "Tutor cadastrado com sucesso!")
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Erro ao salvar tutor: {str(e)}")

    def edit_tutor(self):
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Aviso", "Selecione um tutor para editar!")
            return
        
        tutor_id = int(self.table.item(current_row, 0).text())
        tutor = Tutor.buscar_por_id(tutor_id)
        
        if tutor:
            dialog = TutorDialog(tutor, parent=self)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                try:
                    data = dialog.get_tutor_data()
                    tutor.nome = data['nome']
                    tutor.cpf = data['cpf']
                    tutor.telefone = data['telefone']
                    tutor.email = data['email']
                    tutor.salvar()
                    self.load_tutores()
                    self.tutor_changed.emit()
                    QMessageBox.information(self, "Sucesso", "Tutor atualizado com sucesso!")
                except Exception as e:
                    QMessageBox.critical(self, "Erro", f"Erro ao atualizar tutor: {str(e)}")

    def delete_tutor(self):
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Aviso", "Selecione um tutor para excluir!")
            return
        
        tutor_id = int(self.table.item(current_row, 0).text())
        tutor_nome = self.table.item(current_row, 1).text()
        
        reply = QMessageBox.question(self, "Confirmar Exclusão", 
                                     f"Deseja realmente excluir o tutor '{tutor_nome}'?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                tutor = Tutor.buscar_por_id(tutor_id)
                if tutor:
                    tutor.deletar()
                    self.load_tutores()
                    self.tutor_changed.emit()
                    QMessageBox.information(self, "Sucesso", "Tutor excluído com sucesso!")
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Erro ao excluir tutor: {str(e)}")

