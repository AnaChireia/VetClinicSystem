from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QTableWidget, QTableWidgetItem, QFormLayout, QLineEdit, 
                             QDialog, QDialogButtonBox, QMessageBox, QHeaderView,
                             QComboBox, QDateTimeEdit, QTextEdit)
from PyQt6.QtCore import pyqtSignal, QDateTime
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.atendimento import Atendimento
from models.pet import Pet

class AtendimentoDialog(QDialog):
    def __init__(self, atendimento=None, parent=None):
        super().__init__(parent)
        self.atendimento = atendimento
        self.setWindowTitle("Agendar Atendimento" if atendimento is None else "Editar Atendimento")
        self.setModal(True)
        self.resize(500, 400)
        
        self.init_ui()
        self.load_pets()
        
        if atendimento:
            self.load_atendimento_data()

    def init_ui(self):
        layout = QVBoxLayout()
        
        # Formulário
        form_layout = QFormLayout()
        
        self.pet_combo = QComboBox()
        
        self.data_hora_edit = QDateTimeEdit()
        self.data_hora_edit.setDateTime(QDateTime.currentDateTime())
        self.data_hora_edit.setDisplayFormat("dd/MM/yyyy hh:mm")
        
        self.descricao_edit = QTextEdit()
        self.descricao_edit.setMaximumHeight(100)
        
        form_layout.addRow("Pet:", self.pet_combo)
        form_layout.addRow("Data/Hora:", self.data_hora_edit)
        form_layout.addRow("Descrição:", self.descricao_edit)
        
        layout.addLayout(form_layout)
        
        # Botões
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | 
                                   QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        
        layout.addWidget(buttons)
        self.setLayout(layout)

    def load_pets(self):
        try:
            pets = Pet.buscar_todos()
            self.pet_combo.clear()
            for pet in pets:
                self.pet_combo.addItem(f"{pet.nome} - {pet.tutor_nome}", pet.id)
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao carregar pets: {str(e)}")

    def load_atendimento_data(self):
        # Selecionar pet
        for i in range(self.pet_combo.count()):
            if self.pet_combo.itemData(i) == self.atendimento.pet_id:
                self.pet_combo.setCurrentIndex(i)
                break
        
        # Data/hora
        data_hora = QDateTime.fromString(self.atendimento.data_hora, "yyyy-MM-dd hh:mm:ss")
        self.data_hora_edit.setDateTime(data_hora)
        
        # Descrição
        self.descricao_edit.setPlainText(self.atendimento.descricao)

    def get_atendimento_data(self):
        return {
            'pet_id': self.pet_combo.currentData(),
            'data_hora': self.data_hora_edit.dateTime().toString("yyyy-MM-dd hh:mm:ss"),
            'descricao': self.descricao_edit.toPlainText().strip()
        }

    def accept(self):
        data = self.get_atendimento_data()
        
        # Validações
        if not data['pet_id']:
            QMessageBox.warning(self, "Erro", "Selecione um pet!")
            return
        
        super().accept()

class AtendimentoTab(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.load_atendimentos()

    def init_ui(self):
        layout = QVBoxLayout()
        
        # Botões
        button_layout = QHBoxLayout()
        
        self.add_button = QPushButton("Agendar Atendimento")
        self.edit_button = QPushButton("Editar")
        self.delete_button = QPushButton("Excluir")
        self.refresh_button = QPushButton("Atualizar")
        self.historico_button = QPushButton("Ver Histórico do Pet")
        
        self.add_button.clicked.connect(self.add_atendimento)
        self.edit_button.clicked.connect(self.edit_atendimento)
        self.delete_button.clicked.connect(self.delete_atendimento)
        self.refresh_button.clicked.connect(self.load_atendimentos)
        self.historico_button.clicked.connect(self.show_historico)
        
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.edit_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.refresh_button)
        button_layout.addWidget(self.historico_button)
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
        
        # Tabela
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Pet", "Tutor", "Data/Hora", "Descrição"])
        
        # Configurar redimensionamento das colunas
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)
        
        layout.addWidget(self.table)
        self.setLayout(layout)

    def load_atendimentos(self):
        try:
            atendimentos = Atendimento.buscar_todos()
            self.table.setRowCount(len(atendimentos))
            
            for i, atendimento in enumerate(atendimentos):
                self.table.setItem(i, 0, QTableWidgetItem(str(atendimento.id)))
                self.table.setItem(i, 1, QTableWidgetItem(atendimento.pet_nome))
                self.table.setItem(i, 2, QTableWidgetItem(atendimento.tutor_nome))
                
                # Formatar data/hora
                data_hora = QDateTime.fromString(atendimento.data_hora, "yyyy-MM-dd hh:mm:ss")
                data_hora_str = data_hora.toString("dd/MM/yyyy hh:mm")
                self.table.setItem(i, 3, QTableWidgetItem(data_hora_str))
                
                self.table.setItem(i, 4, QTableWidgetItem(atendimento.descricao))
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao carregar atendimentos: {str(e)}")

    def refresh_pets(self):
        # Método chamado quando pets são alterados
        pass

    def add_atendimento(self):
        dialog = AtendimentoDialog(parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            try:
                data = dialog.get_atendimento_data()
                atendimento = Atendimento(data['pet_id'], data['data_hora'], data['descricao'])
                atendimento.salvar()
                self.load_atendimentos()
                QMessageBox.information(self, "Sucesso", "Atendimento agendado com sucesso!")
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Erro ao agendar atendimento: {str(e)}")

    def edit_atendimento(self):
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Aviso", "Selecione um atendimento para editar!")
            return
        
        atendimento_id = int(self.table.item(current_row, 0).text())
        atendimento = Atendimento.buscar_por_id(atendimento_id)
        
        if atendimento:
            dialog = AtendimentoDialog(atendimento, parent=self)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                try:
                    data = dialog.get_atendimento_data()
                    atendimento.pet_id = data['pet_id']
                    atendimento.data_hora = data['data_hora']
                    atendimento.descricao = data['descricao']
                    atendimento.salvar()
                    self.load_atendimentos()
                    QMessageBox.information(self, "Sucesso", "Atendimento atualizado com sucesso!")
                except Exception as e:
                    QMessageBox.critical(self, "Erro", f"Erro ao atualizar atendimento: {str(e)}")

    def delete_atendimento(self):
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Aviso", "Selecione um atendimento para excluir!")
            return
        
        atendimento_id = int(self.table.item(current_row, 0).text())
        pet_nome = self.table.item(current_row, 1).text()
        data_hora = self.table.item(current_row, 3).text()
        
        reply = QMessageBox.question(self, "Confirmar Exclusão", 
                                     f"Deseja realmente excluir o atendimento do pet '{pet_nome}' em {data_hora}?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                atendimento = Atendimento.buscar_por_id(atendimento_id)
                if atendimento:
                    atendimento.deletar()
                    self.load_atendimentos()
                    QMessageBox.information(self, "Sucesso", "Atendimento excluído com sucesso!")
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Erro ao excluir atendimento: {str(e)}")

    def show_historico(self):
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Aviso", "Selecione um atendimento para ver o histórico do pet!")
            return
        
        # Obter pet_id do atendimento selecionado
        atendimento_id = int(self.table.item(current_row, 0).text())
        atendimento = Atendimento.buscar_por_id(atendimento_id)
        
        if atendimento:
            try:
                historico = Atendimento.buscar_por_pet(atendimento.pet_id)
                pet = Pet.buscar_por_id(atendimento.pet_id)
                
                if historico:
                    historico_text = f"Histórico de Atendimentos - {pet.nome}\n\n"
                    for item in historico:
                        data_hora = QDateTime.fromString(item.data_hora, "yyyy-MM-dd hh:mm:ss")
                        data_hora_str = data_hora.toString("dd/MM/yyyy hh:mm")
                        historico_text += f"Data: {data_hora_str}\n"
                        historico_text += f"Descrição: {item.descricao}\n"
                        historico_text += "-" * 50 + "\n"
                    
                    QMessageBox.information(self, "Histórico do Pet", historico_text)
                else:
                    QMessageBox.information(self, "Histórico do Pet", "Nenhum atendimento encontrado para este pet.")
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Erro ao buscar histórico: {str(e)}")

