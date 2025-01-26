from flask import current_app as app

from flask import render_template,request,redirect

from backend.models import db,User,Professional,ServiceCategory,Admin

@app.route("/",methods=["GET","POST"])
def index():
    
    return render_template("Home.html")


@app.route("/register/customer" , methods=["GET","POST"])
def pro_register():
    if request.method =="GET":
        return render_template("/customer/register.html")
    elif request.method =="POST":
        Email = request.form.get("cust_email")
        pwd=request.form.get("cust_password")
        Name=request.form.get("cust_name")
        cust1 = db.session.query(User).filter_by(email=Email).first()
        if not cust1:
            cust = User(name=Name,email = Email,password=pwd)
            db.session.add(cust)
            db.session.commit()
            return redirect("/login")
        else:
            return redirect("/login")
        
@app.route("/register/professional" , methods=["GET","POST"])
def Cust_register():
    if request.method =="GET":
        ser_cat = db.session.query(ServiceCategory).all()

        return render_template("/professional/register.html" ,category = ser_cat)
    elif request.method =="POST":
        Email = request.form.get("pro_email")
        pwd=request.form.get("pro_pwd")
        Name=request.form.get("pro_name")
        pro1 = db.session.query(Professional).filter_by(email=Email).first()
        if not pro1:
            pro = Professional(name=Name,email = Email,password=pwd)
            db.session.add(pro)
            db.session.commit()
            return redirect("/login")
        else:
            return redirect("/login")


@app.route("/login",methods=["GET","POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        Email = request.form.get("user_email")
        pwd=request.form.get("user_password")

        person =  db.session.query(User).filter_by(email=Email).first() or \
              db.session.query(Professional).filter_by(email=Email).first() or  \
                db.session.query(Admin).filter_by(email=Email).first()
        
        if person and person.password == pwd :
            if isinstance(person,User):
                return redirect("/customer/dashboard")
            elif isinstance(person,Admin):
                return redirect("/admin/dashboard")
            elif isinstance(person,Professional):
                return redirect("/professional/dashboard")
        else:
            return redirect("/")
        


@app.route("/customer/dashboard", methods=["GET","POST"])
def cust_dash():
    if request.method=="GET":
        return render_template("/customer/dashboard.html")
    
@app.route("/admin/dashboard", methods=["GET","POST"])
def admin_dash():
    if request.method=="GET":
        return render_template("/admin/dashboard.html")
    

@app.route("/professional/dashboard", methods=["GET","POST"])
def pro_dash():
    if request.method=="GET":
        return render_template("/professional/dashboard.html")