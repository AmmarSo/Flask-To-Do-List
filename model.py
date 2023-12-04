import sqlite3

class User:
    def __init__(self, id, date, Matière, Description, completion):
        self.id = id  # Identifiant de le devoir
        self.date = date  # Date de la tâche
        self.Matière = Matière  # Matière de la tâche
        self.Description = Description  # Description de la tâche
        self.completion = completion  # État de complétion de la tâche (0 ou 1)

    def get_id(self):
        return self.id

    def get_date(self):
        return self.date

    def get_Matière(self):
        return self.Matière

    def get_Description(self):
        return self.Description

    def is_completed(self):
        return self.completion == 1

    def toggle_completion(self):
        self.completion = 1 - self.completion  # Basculer l'état de complétion entre 0 et 1 (fameux boolean)
        conn = sqlite3.connect('tache.db')  # Se connecter à la base de données
        cursor = conn.cursor()
        cursor.execute('UPDATE users SET completion = ? WHERE id = ?', (self.completion, self.id))  # Mettre à jour l'état de complétion dans la base de données
        conn.commit()  # Valider les modifications
        conn.close()  # Fermer la connexion à la base de données

class UserRepository:
    @staticmethod
    def create_table():
        conn = sqlite3.connect('tache.db')  # Se connecter à la base de données
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Identifiant de le devoir (clé primaire auto-incrémentée)
                date TEXT,  -- Date de la tâche (texte)
                Matière TEXT,  -- Matière de la tâche (texte)
                Description TEXT,  -- Description de la tâche (texte)
                completion INTEGER DEFAULT 0  -- État de complétion de la tâche (0 par défaut)
            )
        ''')

        conn.commit()  # Valider les modifications
        conn.close()  # Fermer la connexion à la base de données

    @staticmethod
    def get_all_users():
        conn = sqlite3.connect('tache.db')  # Se connecter à la base de données
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM users')  # Récupérer tous les devoirs de la table
        rows = cursor.fetchall()  # Récupérer toutes les lignes résultantes

        users = []
        for row in rows:
            user = User(row[0], row[1], row[2], row[3], row[4])  # Créer un objet User à partir des données de la ligne
            users.append(user)  # Ajouter le devoir à la liste

        conn.close()  # Fermer la connexion à la base de données

        return users  # Afficher la liste des devoirs

    @staticmethod
    def get_user_by_id(user_id):
        conn = sqlite3.connect('tache.db')  # Se connecter à la base de données
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))  # Récupérer le devoir avec l'identifiant 
        row = cursor.fetchone()  # Récupérer la première ligne 

        if row:
            user = User(row[0], row[1], row[2], row[3], row[4])  # Créer un objet User à partir des données de la ligne
        else:
            user = None

        conn.close()  # Fermer la connexion à la base de données

        return user  # Afficher le devoir

    @staticmethod
    def create_user(date, Matière, Description):
        conn = sqlite3.connect('tache.db')  # Se connecter à la base de données
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO users (date, Matière, Description)
            VALUES (?, ?, ?)
        ''', (date, Matière, Description))  # Insérer un nouvel utilisateur avec les valeurs du formulaire html

        conn.commit()  # Valider les modifications
        conn.close()  # Fermer la connexion à la base de données

    @staticmethod
    def delete_user(user_id):
        conn = sqlite3.connect('tache.db')  # Se connecter à la base de données
        cursor = conn.cursor()

        cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))  # Supprimer le devoir avec l'identifiant 

        conn.commit()  # Valider les modifications
        conn.close()  # Fermer la connexion à la base de données
