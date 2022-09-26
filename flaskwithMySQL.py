#importing the needed packages and modules
from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL
import yaml
app = Flask(__name__)

#Configure db
db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASS'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)

@app.route('/', methods=['GET','POST'])
def hello():
    if request.method == 'POST':
        #Fetch form data
        userDetails = request.form
        name = userDetails['name']
        email = userDetails['email']
        phonenumber = userDetails['phonenumber']
        gender = userDetails['gender']
        age = userDetails['age']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO details(name, email,phoneno,gender,age) VALUES(%s, %s, %s, %s, %s)",(name, email,phonenumber,gender,age))
        mysql.connection.commit()
        cur.close()
        return redirect('/users')
    return render_template('index.html')
 
@app.route('/update', methods=['GET','POST'])
def update():
    if request.method == 'POST':
        userDetails = request.form
        email = userDetails['email']
        age = userDetails['age']
        cur = mysql.connection.cursor()
        cur.execute("UPDATE details SET age = %s WHERE email = %s",(age,email))
        mysql.connection.commit()
        cur.close()
        return redirect('/users')
    return render_template('update.html')

@app.route('/delete',methods=['GET','POST'])
def delete():
    if request.method == 'POST':
        userDetails = request.form
        email = userDetails['email']
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM details WHERE email = %s",(email,))
        mysql.connection.commit()
        cur.close()
        return redirect('/users')
    return render_template('delete.html')


@app.route('/users')
def users():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM details")
    if resultValue > 0:
        userDetails = cur.fetchall()
        return render_template('users.html',userDetails=userDetails)

if __name__ == '__main__':
    app.run(debug=True, host='localhost')