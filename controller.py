from flask import Flask, render_template, request, redirect, url_for
from model import User, UserRepository

app = Flask(__name__)
app.config['DEBUG'] = True

class UserController:
    def __init__(self):
        UserRepository.create_table()  # Crée la table des devoirs lors de l'initialisation du contrôleur

    def display_user_details(self):
        users = UserRepository.get_all_users()  # Récupère tous les devoirs depuis le référentiel
        users = sorted(users, key=lambda user: user.get_date())  # Trie les devoirs par dates
        return render_template('page_tache.html', users=users)  # Affiche les détails des devoirs dans le template 'page_tache.html'

    def create_user(self):
        if request.method == 'POST':
            date = request.form['date']
            Matière = request.form['Matière']
            Description = request.form['Description']

            UserRepository.create_user(date, Matière, Description)  # Crée un nouveau devoir avec les données du formulaire

            return redirect(url_for('display_user_details'))  # Redirige vers l'affichage des détails des devoirs
        elif request.method == 'GET':
            return render_template('créer_tache.html')  # Affiche le formulaire de création des devoirs

    def delete_user(self, user_id):
        UserRepository.delete_user(user_id)  # Supprime le devoir avec l'identifiant spécifié
        return redirect(url_for('display_user_details'))  # Redirige vers l'affichage des détails des devoirs

    def toggle_completion(self, user_id):
        user = UserRepository.get_user_by_id(user_id)  # Récupère le devoir avec l'identifiant 
        if user:
            user.toggle_completion()  # Bascule l'état de complétion de le devoir
        return redirect(url_for('display_user_details'))  # Envoi vers l'affichage des détails des devoirs

controller = UserController()  # Créer le contrôleur des devoirs

# Routes
@app.route('/')
def display_user_details():
    return controller.display_user_details()  # Affiche les détails des devoirs

@app.route('/create', methods=['GET', 'POST'])
def create_user():
    return controller.create_user()  # Crée un nouveau devoir

@app.route('/delete/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    return controller.delete_user(user_id)  # Supprime le devoir

@app.route('/toggle_completion/<int:user_id>', methods=['POST'])
def toggle_completion(user_id):
    return controller.toggle_completion(user_id)  # Bascule l'état de complétion de le devoir

if __name__ == '__main__':
    app.run()  # Lance l'application Flask
