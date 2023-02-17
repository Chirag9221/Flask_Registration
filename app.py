from flask import Flask,render_template,request
import re
import sqlite3

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

def check(email):
    regexp = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if re.match(regexp,email):
        return True
    else:
        return False

@app.route('/register',methods=['POST','GET'])
def register():
    if request.method == 'POST':
        team_name = request.form['team_name']
        team_email = request.form['team_email']
        name_par1 = request.form['name_par1']
        email_par1 = request.form['email_par1']
        phone_par1 = request.form['phone_par1']
        branch_par1 = request.form['branch_par1']
        college_par1 = request.form['college_par1']
        name_par2 = request.form['name_par2']
        email_par2 = request.form['email_par2']
        phone_par2 = request.form['phone_par2']
        branch_par2= request.form['branch_par2']
        college_par2 = request.form['college_par2']
        mail_check = check(team_email)
        mail_check = check(email_par1)
        mail_check = check(email_par2)

        database_connection = sqlite3.connect('Registration.db')
        database_cursor = database_connection.cursor()
        data = database_cursor.execute("SELECT * FROM Register WHERE EXISTS(SELECT Name_of_Team FROM Register WHERE Name_of_Team=?)",(team_name,))
        data = data.fetchone()
        if data is not None or mail_check==False:
            if mail_check==False:
                mssge = 'Enter Valid Mail IDs'
                database_connection.commit()
                database_connection.close()
                return render_template('home_after_error.html',mssge=mssge)
            else:
                database_connection.commit()
                database_connection.close()
                mssge = 'Team Name has to be unique'
                return render_template('home_after_error.html',mssge=mssge)
        else:
            database_cursor.execute('INSERT INTO Register(EmailID_of_Team,Name_of_Team,Name_Participant1,Email_Participant1,Phone_Participant1,Branch_Year,College_Name,Name_Participant2,Email_Participant2,Phone_Participant2,Branch_Year_2,College_Name_2) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)',(team_email,team_name,name_par1,email_par1,phone_par1,branch_par1,college_par1,name_par2,email_par2,phone_par2,branch_par2,college_par2))
            database_connection.commit()
            database_connection.close()
            return '<h1>Your Data Has been added to the Database</h1>'


if __name__ == '__main__':
    app.run(debug=True)