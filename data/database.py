
import sqlite3

DATABASE_NAME = 'vet_clinic.db'

def connect_db():
    return sqlite3.connect(DATABASE_NAME)

def create_tables():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tutores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            cpf TEXT UNIQUE NOT NULL,
            telefone TEXT,
            email TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            raca TEXT NOT NULL,
            tutor_id INTEGER NOT NULL,
            foto_path TEXT,
            FOREIGN KEY (tutor_id) REFERENCES tutores(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS atendimentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pet_id INTEGER NOT NULL,
            data_hora TEXT NOT NULL,
            descricao TEXT,
            FOREIGN KEY (pet_id) REFERENCES pets(id)
        )
    ''')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_tables()
    print('Tabelas criadas com sucesso!')


