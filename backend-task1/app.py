from flask import Flask, jsonify, request, render_template
from flask_mysqldb import MySQL
from flask import Flask, jsonify, render_template, request
#from flask_mysqldb import MySQL
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_HOST'] = 'aashu'
app.config['MYSQL_USER'] = 'aashutosh'
app.config['MYSQL_PASSWORD'] = 'My$3cr3tP@$$w0rd'
app.config['MYSQL_DB'] = 'mydbnew'

mysql = MySQL(app)

def check_mysql_connection():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT 1')
        cursor.close()
        return True
    except:
        return False
    
# Word model
class WordForm(FlaskForm):
     word = StringField('Word', validators=[DataRequired()])
     submit = SubmitField('Submit')


# API endpoint to retrieve the word
@app.route('/api/get_word', methods=['GET'])
def get_word():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT word FROM words LIMIT 1')
    word = cursor.fetchone()[0]
    cursor.close()
    return jsonify({'word': word})

# @app.route('/api/word', methods=['GET'])
# def get_word():
#     cur = mysql.connection.cursor()
#     cur.execute('SELECT word FROM words')
#     word = cur.fetchone()[0]
#     cur.close()
#     return jsonify({'word': word})

# Admin portal to update the word
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    form = WordForm()
    if form.validate_on_submit():
        word = form.word.data
        cursor = mysql.connection.cursor()
        cursor.execute('UPDATE words SET word = %s', (word,))
        mysql.connection.commit()
        cursor.close()
        return 'Word updated successfully!'
    return render_template('admin.htm', form=form)


# @app.route('/admin', methods=['GET', 'POST'])
# def admin():
#     if request.method == 'POST':
#         new_word = request.form['word']
#         cur = mysql.connection.cursor()
#         cur.execute('UPDATE words SET word = %s', (new_word,))
#         mysql.connection.commit()
#         cur.close()
#     cur = mysql.connection.cursor()
#     cur.execute('SELECT word FROM words')
#     word = cur.fetchone()[0]
#     cur.close()
#     return render_template('admin.html', word=word)


if __name__ == '__main__':
    app.run(debug=True, port=8000)
else:
        print('Failed to connect to MySQL database.')








