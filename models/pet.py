from data.database import connect_db

class Pet:
    def __init__(self, nome, raca, tutor_id, foto_path=None, id=None):
        self.id = id
        self.nome = nome
        self.raca = raca
        self.tutor_id = tutor_id
        self.foto_path = foto_path

    def salvar(self):
        conn = connect_db()
        cursor = conn.cursor()

        if self.id is None:
            cursor.execute('''
                INSERT INTO pets (nome, raca, tutor_id, foto_path)
                VALUES (?, ?, ?, ?)
            ''', (self.nome, self.raca, self.tutor_id, self.foto_path))
            self.id = cursor.lastrowid
        else:
            cursor.execute('''
                UPDATE pets SET nome=?, raca=?, tutor_id=?, foto_path=?
                WHERE id=?
            ''', (self.nome, self.raca, self.tutor_id, self.foto_path, self.id))

        conn.commit()
        conn.close()

    @staticmethod
    def buscar_todos():
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT p.*, t.nome as tutor_nome 
            FROM pets p 
            JOIN tutores t ON p.tutor_id = t.id
        ''')
        rows = cursor.fetchall()
        conn.close()

        pets = []
        for row in rows:
            pet = Pet(row[1], row[2], row[3], row[4], row[0])
            pet.tutor_nome = row[5]
            pets.append(pet)
        return pets

    @staticmethod
    def buscar_por_tutor(tutor_id):
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM pets WHERE tutor_id=?', (tutor_id,))
        rows = cursor.fetchall()
        conn.close()

        pets = []
        for row in rows:
            pet = Pet(row[1], row[2], row[3], row[4], row[0])
            pets.append(pet)
        return pets

    @staticmethod
    def buscar_por_id(id):
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM pets WHERE id=?', (id,))
        row = cursor.fetchone()
        conn.close()

        if row:
            return Pet(row[1], row[2], row[3], row[4], row[0])
        return None

    def deletar(self):
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM pets WHERE id=?', (self.id,))
        conn.commit()
        conn.close()

    @staticmethod
    def get_racas():
        return [
            "Cão - Labrador",
            "Cão - Golden Retriever",
            "Cão - Bulldog",
            "Cão - Pastor Alemão",
            "Cão - Poodle",
            "Cão - Beagle",
            "Cão - Rottweiler",
            "Cão - Yorkshire",
            "Cão - Chihuahua",
            "Cão - Dachshund",
            "Gato - Persa",
            "Gato - Siamês",
            "Gato - Maine Coon",
            "Gato - Ragdoll",
            "Gato - British Shorthair",
            "Gato - Abissínio",
            "Gato - Bengala",
            "Gato - Sphynx",
            "Outro"
        ]

