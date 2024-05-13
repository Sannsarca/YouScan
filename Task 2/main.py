import os
from groq import Groq

import psycopg2
import re

# Create a Groq client instance
client = Groq(api_key='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')

def llm_prompt_get(prompt):
    """
    Send a prompt to the LLM and return its answer.
    
    Args:
        prompt (str): The prompt to send to the LLM
    
    Returns:
        str: The answer from the LLM
    """

    client = Groq(api_key='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')
    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", 
                   "content": prompt}],
        
        #Also tested model="llama3-8b-8192",
        model="llama3-70b-8192")
    
    return chat_completion.choices[0].message.content
    
from flask import Flask, render_template, request

app = Flask(__name__)

class User():
  def __init__(self, id, login, password):
    self.id=id
    self.login=login
    self.password=password

user = User(0, 0, 0)

def db_conn():
    """
    Connect to the PostgreSQL database and return the connection object.
    
    Returns:
        psycopg2.extensions.connection: The database connection object
    """
    # Replace the following placeholders with your actual values
    db_host = 'localhost'
    db_name = 'User_Notes'
    db_user = 'postgres'
    db_password = '5555'
    db_port = '5432'

    # Connect to the PostgreSQL database
    connection = psycopg2.connect(
        host = db_host,
        database = db_name,
        user = db_user,
        password = db_password,
        port = db_port
    )
    return connection

@app.route('/')
def index():
    """
    Render the index page.
    """
    return render_template('index.html', error=' ')

@app.route('/submit', methods=['POST'])
def submit():
    """
    Handle the login form submission.
    """
    global user
    try:
        conn = db_conn()
        cur = conn.cursor()
        login = request.form['login']
        password = request.form['password']

        cur.execute(f'''SELECT * FROM users WHERE user_login='{login}' AND user_password='{password}' ''')
        data = cur.fetchall()
        user = User(data[0][0], data[0][1], data[0][2])
        cur.close()
        conn.close()

        data = notes_extraction(user.id, 3)    
        return render_template('notekeeper.html', data=list(data))
    
    except: 
        return render_template('index.html', error='There is an error with login or password. Try again.')
    
    

@app.route('/save', methods=['POST'])
def save():
    """
    Handle the note saving form submission.
    """
    global user
    try:
        conn = db_conn()
        cur = conn.cursor()

        note = request.form['note']
        note = note.replace("'", "`")
        cur.execute(f'''INSERT INTO notes (user_id,note ) VALUES ({user.id}, '{note}');''')
        conn.commit()

        cur.close()
        conn.close()

        data = notes_extraction(user.id, 3)
        return render_template('notekeeper.html', data=list(data), error2="Saved!")
    
    except:
        data = notes_extraction(user.id, 3)
        return render_template('notekeeper.html', data=list(data), error2="Error")

@app.route('/show', methods=['POST'])
def show():
    """
    Handle the note showing form submission.
    """ 
    try:
        num = request.form['num']
        print(num)
        data = notes_extraction(user.id, num)
        return render_template('notekeeper.html', data=list(data), error1="Here!")
    except:
        data = notes_extraction(user.id, 3)
        return render_template('notekeeper.html', data=list(data), error1="Error")

@app.route('/llm', methods=['POST'])
def llm():
    """
    Handle the LLM form submission.
    """
    global user
    try:
        data = notes_extraction(user.id)
        all_data = notes_extraction(user.id, mode=2)

        prompt = "Forgot everything you know before. You are a notekeeping application. You give short answers on questions based on user`s notes. Those are notes user have:"

        for i in range(len(all_data)):
            prompt = prompt + f" {all_data[i][0]}) {all_data[i][1]}"

        question = request.form['ask']
        prompt = prompt + f". Now answer a question: {question}?"
        prompt_id = prompt + " Return only ID number you receive of relevant notes without any other numbers."
        
        answer = llm_prompt_get(prompt)
        possible_id = llm_prompt_get(prompt_id)
    
        id_s = re.findall(r'\d+', possible_id)
        id_s = ','.join(id_s)

        if not id_s:
            return render_template('notekeeper.html', data=list(data), answer=answer)
        relevant_data = notes_extraction(id_s, mode=3)
        return render_template('notekeeper.html', data=list(data), answer=answer, relevant=relevant_data)
    except:
        data = notes_extraction(user.id, 3)
        return render_template('notekeeper.html', data = list(data), answer="Error")
    
def notes_extraction(id, limit=3, mode=1):
    """
    Extract notes from the database.
    
    Args:
        id (int): The user ID
        limit (int): The number of notes to extract (default=3)
        mode (int): The extraction mode (default=1). 
            Mode 1 - extract notes with limit. 
            Mode 2 - extract all notes.
            Mode 3 - extract exact notes on id.
    
    Returns:
        list: A list of notes
    """
    conn = db_conn()
    cur = conn.cursor()
    if mode == 1:
        cur.execute(f'''SELECT note_id, note FROM notes WHERE user_id={id} ORDER BY note_id DESC LIMIT {limit};''')
    elif mode == 2:
            cur.execute(f'''SELECT note_id, note FROM notes WHERE user_id={id} ORDER BY note_id DESC;''')
    elif mode == 3:
            cur.execute(f'''SELECT note_id, note FROM notes WHERE note_id in ({id}) ORDER BY note_id DESC;''')

    conn.commit()

    data = cur.fetchall()

    cur.close()
    conn.close()    
    return data



if __name__ == "__main__":
    app.run(debug=True)