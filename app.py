from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///firstapp.db"


with app.app_context():
    db = SQLAlchemy(app)


class FirstApp(db.Model):
    sno = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fname = db.Column(db.String(100), nullable=False)
    lname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"{self.sno} - {self.fname}"


@app.route('/', methods=['GET', 'POST']) 
def hello_world():
    if request.method == 'POST': 
        
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        email = request.form.get('email')

        
        if fname and lname and email:
            firstapp = FirstApp(fname=fname, lname=lname, email=email)
            with app.app_context():
                db.session.add(firstapp)
                db.session.commit()

    with app.app_context(): #
        allpeople = FirstApp.query.all()

    return render_template('index.html', allpeople=allpeople)

@app.route("/delete/<int:sno>") 
def delete(sno):
    with app.app_context(): 
        firstapp = FirstApp.query.filter_by(sno=sno).first() 
        db.session.delete(firstapp) 
        db.session.commit() 
    return redirect("/") 

@app.route("/update/<int:sno>", methods=['GET', 'POST'])
def update(sno):
    with app.app_context():
        firstapp = FirstApp.query.filter_by(sno=sno).first()

        if request.method == "POST":
            firstapp.fname = request.form['fname']
            firstapp.lname = request.form['lname']
            firstapp.email = request.form['email']

            db.session.commit()  
            return redirect("/")

        return render_template("update.html", firstapp=firstapp)

if __name__ == "__main__":
    with app.app_context(): 
        db.create_all() 
    app.run(debug=True)
