from datetime import datetime

from cryptography.fernet import Fernet
import sqlite3

def create_database():
    conn = sqlite3.connect('password_manager.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS credentials (
                      id INTEGER PRIMARY KEY,
                      service_name TEXT NOT NULL,
                      username TEXT NOT NULL,
                      password TEXT NOT NULL,
                      creation_date TEXT)''')
    conn.commit()
    conn.close()


# Carica la chiave di cifratura
def load_key():
    return open("secret.key", "rb").read()

# Cifra la password
def encrypt_password(password, key):
    fernet = Fernet(key)
    encrypted = fernet.encrypt(password.encode())
    return encrypted

# Decifra la password
def decrypt_password(encrypted_password, key):
    fernet = Fernet(key)
    decrypted = fernet.decrypt(encrypted_password).decode()
    return decrypted

def add_credential(service_name, username, password, key):
    encrypted_password = encrypt_password(password, key)
    conn = sqlite3.connect('password_manager.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO credentials (service_name, username, password, creation_date) VALUES (?, ?, ?, ?)",
                   (service_name, username, encrypted_password, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()
    print("Credenziale aggiunta con successo!")

def view_credentials(key):
    conn = sqlite3.connect('password_manager.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, service_name, username, password FROM credentials")
    rows = cursor.fetchall()
    conn.close()
    
    for row in rows:
        decrypted_password = decrypt_password(row[3], key)
        print(f"ID: {row[0]}, Servizio: {row[1]}, Username: {row[2]}, Password: {decrypted_password}")

def delete_account(id):
    conn=sqlite3.connect("password_manager.db")
    cursor=conn.cursor()
    cursor.execute("DELETE FROM credentials WHERE ID=?",(id))
    conn.commit()
    conn.close()

def main():
    create_database()
    key=load_key()
    while True:
        print("\nPassword Manager")
        print("1. Aggiungi una nuova credenziale")
        print("2. Visualizza tutte le credenziali")
        print("3. Elimina account")
        choice = input("Scegli un'opzione: ")

        if choice == '1':
            service_name = input("Nome del servizio: ")
            username = input("Username: ")
            password = input("Password: ")
            add_credential(service_name, username, password, key)

        elif choice == '2':
            view_credentials(key)

        elif choice == '3':
             view_credentials(key)
             print(f"Scegli l id da eliminare")
             choice=input()
             delete_account(choice)
             
        
            
        else:
            print("Opzione non valida. Riprova.")


if __name__ == "__main__":
    main()