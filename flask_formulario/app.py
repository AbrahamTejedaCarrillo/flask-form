from flask import Flask, render_template, request,redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)


#coneccion a sql
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flaskcontacts1'
mysql = MySQL(app)

#configuraciones
app.secret_key = 'mysecretkey'

@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts')
    data = cur.fetchall()
    return render_template('index.html', contacts = data)

@app.route('/add_contact', methods=['POST'])
def Add_contact():
    if request.method == 'POST':
        fullname = request.form['fullname'].strip()
        phone = request.form['phone'].strip()
        email = request.form['email'].strip()

        if not fullname or not phone or not email:
            flash('Todos los campos son obligatorios, completa la informacion')
            return redirect(url_for('Index'))
        
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO contacts (fullname, phone, email) VALUES(%s, %s, %s)', (fullname, phone, email))
        mysql.connection.commit()
        flash('Contacto agregado satisfactoriamente')
        return redirect(url_for('Index'))


@app.route('/edit/<id>')
def Get_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts WHERE id = %s', (id,))
    data = cur.fetchall()
    print(data[0])
    return render_template('edit_contact.html', contact = data[0])

@app.route('/update/<id>', methods = ['POST'])
def Update(id):
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute('''
                    UPDATE contacts
                    SET fullname = %s,
                        email = %s,
                        phone = %s
                    WHERE id = %s
                    ''', (fullname, email, phone, id))
        mysql.connection.commit()
        flash('Contacto actualizado satisfactoriamente')
    return redirect(url_for('Index'))

@app.route('/delete/<string:id>')
def Delete_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM contacts WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Contacto eliminado satisfactoriamente')
    return redirect(url_for('Index'))

if __name__ == '__main__':
    app.run(port = 3000, debug = True)

