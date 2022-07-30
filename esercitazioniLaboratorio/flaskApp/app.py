#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 14 11:43:31 2022

@author: apirodd
"""

# -*- coding: utf-8 -*-
#importiamo i moduli per gestire i template e i dati provenienti dal form html
from flask import Flask, render_template, request
import mysql.connector
import webbrowser

app = Flask(__name__)

#definiamo un dizionario con i dati di accesso al database MySQL
config = {
  'user': 'root',
  'password': 'root',
  'host': '127.0.0.1',
  'port': 8889,
  'database': 'BucketList',
  'raise_on_warnings': True
}

# gestisce le richieste indirizzate alla pagina index.html
@app.route('/')
def main():
     return render_template('index.html')

# gestisce le richieste di registrazione indirizzando l'utente su signup.html
@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')

# reindirizza lo studente ad una pagina in cui si comunica l'avvenuta registr.
@app.route('/Utente_ok')
def Utente_ok():
    return render_template('utente_ok.html')

# reindirizza lo studente ad una pagina in cui si comunica un errore
@app.route('/Errore_utente')
def Errore_utente():
    return render_template('errore_utente.html')

@app.route('/signUp',methods=['POST','GET'])
def signUp():
    try:
        # il codice per creare lo user si trova qui !!
        # legge i valori inseriti nel form di registrazione
        _name = request.form['inputName']
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']
        
        # valida i valori ricevuti
        if _name and _email and _password:
            # si connette al database MySQL
            cnx = mysql.connector.connect(**config)
            # attiva il cursore per scorrere il db
            cursor = cnx.cursor(dictionary=True)
           # chiama la stored procedure passandole i dati inseriti nel form
            cursor.callproc('sp_createUser',[_name,_email,_password])
        # assegna alla variabile data eventuali parti di stringa non inserite 
            data = cursor.fetchall()
     # se la variabile data è vuota allora l'inserimento è andato a buon fine 
            if len(data) == 0:
                cnx.commit() #salva il record nel db
                d={'message':'User created successfully !'}
                
                return d # restituisce un messaggio di successo

            else:
                d={'message':'errore inserimento'}
                
                return d
        else:
            
            d={'message':'errore inserimento'}
    except Exception as e:
        #return json.dumps({'error':str(e)})
        d={'message':str(e)}
        return d
    finally:
        if d['message']=='User created successfully !':
            webbrowser.open_new_tab('http://127.0.0.1:5000/Utente_ok')
        else:
            webbrowser.open_new_tab('http://127.0.0.1:5000/Errore_utente')
        cursor.close() 
        cnx.close()
    
if __name__ == '__main__':
     app.run(host='127.0.0.1', port=5000)