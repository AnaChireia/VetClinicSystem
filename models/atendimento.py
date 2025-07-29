from datetime import datetime
from data.database import connect_db

class Atendimento:
    def __init__(self, pet_id, data_hora, descricao="", id=None):
        self.id = id
        self.pet_id = pet_id
        self.data_hora = data_hora
        self.descricao = descricao

    def salvar(self):
        # Verificar se já existe agendamento para o mesmo pet no mesmo horário
        if self.verificar_conflito():
            raise ValueError("Já existe um agendamento para este pet neste horário")

        conn = connect_db()
        cursor = conn.cursor()

        if self.id is None:
            cursor.execute('''
                INSERT INTO atendimentos (pet_id, data_hora, descricao)
                VALUES (?, ?, ?)
            ''', (self.pet_id, self.data_hora, self.descricao))
            self.id = cursor.lastrowid
        else:
            cursor.execute('''
                UPDATE atendimentos SET pet_id=?, data_hora=?, descricao=?
                WHERE id=?
            ''', (self.pet_id, self.data_hora, self.descricao, self.id))

        conn.commit()
        conn.close()

    def verificar_conflito(self):
        conn = connect_db()
        cursor = conn.cursor()
        
        if self.id is None:
            cursor.execute('''
                SELECT COUNT(*) FROM atendimentos 
                WHERE pet_id=? AND data_hora=?
            ''', (self.pet_id, self.data_hora))
        else:
            cursor.execute('''
                SELECT COUNT(*) FROM atendimentos 
                WHERE pet_id=? AND data_hora=? AND id!=?
            ''', (self.pet_id, self.data_hora, self.id))
        
        count = cursor.fetchone()[0]
        conn.close()
        return count > 0

    @staticmethod
    def buscar_todos():
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT a.*, p.nome as pet_nome, t.nome as tutor_nome
            FROM atendimentos a
            JOIN pets p ON a.pet_id = p.id
            JOIN tutores t ON p.tutor_id = t.id
            ORDER BY a.data_hora
        ''')
        rows = cursor.fetchall()
        conn.close()

        atendimentos = []
        for row in rows:
            atendimento = Atendimento(row[1], row[2], row[3], row[0])
            atendimento.pet_nome = row[4]
            atendimento.tutor_nome = row[5]
            atendimentos.append(atendimento)
        return atendimentos

    @staticmethod
    def buscar_por_pet(pet_id):
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM atendimentos 
            WHERE pet_id=? 
            ORDER BY data_hora DESC
        ''', (pet_id,))
        rows = cursor.fetchall()
        conn.close()

        atendimentos = []
        for row in rows:
            atendimento = Atendimento(row[1], row[2], row[3], row[0])
            atendimentos.append(atendimento)
        return atendimentos

    @staticmethod
    def buscar_por_id(id):
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM atendimentos WHERE id=?', (id,))
        row = cursor.fetchone()
        conn.close()

        if row:
            return Atendimento(row[1], row[2], row[3], row[0])
        return None

    def deletar(self):
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM atendimentos WHERE id=?', (self.id,))
        conn.commit()
        conn.close()

