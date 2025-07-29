import re
from data.database import connect_db

class Tutor:
    def __init__(self, nome, cpf, telefone, email, id=None):
        self.id = id
        self.nome = nome
        self.cpf = cpf
        self.telefone = telefone
        self.email = email

    @staticmethod
    def validar_cpf(cpf):
        # Remove caracteres não numéricos
        cpf = re.sub(r'\D', '', cpf)
        return len(cpf) == 11 and cpf.isdigit()

    @staticmethod
    def validar_email(email):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    def salvar(self):
        if not self.validar_cpf(self.cpf):
            raise ValueError("CPF inválido")
        if not self.validar_email(self.email):
            raise ValueError("Email inválido")

        conn = connect_db()
        cursor = conn.cursor()

        if self.id is None:
            cursor.execute('''
                INSERT INTO tutores (nome, cpf, telefone, email)
                VALUES (?, ?, ?, ?)
            ''', (self.nome, self.cpf, self.telefone, self.email))
            self.id = cursor.lastrowid
        else:
            cursor.execute('''
                UPDATE tutores SET nome=?, cpf=?, telefone=?, email=?
                WHERE id=?
            ''', (self.nome, self.cpf, self.telefone, self.email, self.id))

        conn.commit()
        conn.close()

    @staticmethod
    def buscar_todos():
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tutores')
        rows = cursor.fetchall()
        conn.close()

        tutores = []
        for row in rows:
            tutor = Tutor(row[1], row[2], row[3], row[4], row[0])
            tutores.append(tutor)
        return tutores

    @staticmethod
    def buscar_por_id(id):
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tutores WHERE id=?', (id,))
        row = cursor.fetchone()
        conn.close()

        if row:
            return Tutor(row[1], row[2], row[3], row[4], row[0])
        return None

    def deletar(self):
        # Verificar se há pets vinculados
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM pets WHERE tutor_id=?', (self.id,))
        count = cursor.fetchone()[0]

        if count > 0:
            conn.close()
            raise ValueError("Não é possível excluir tutor com pets vinculados")

        cursor.execute('DELETE FROM tutores WHERE id=?', (self.id,))
        conn.commit()
        conn.close()

