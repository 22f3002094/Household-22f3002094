from flask import current_app as app
from flask_login import login_user,current_user,login_required,logout_user
from flask import render_template,request,redirect,flash

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
        
        if person :
            if person.password == pwd:
                if isinstance(person,User):
                    login_user(person)
                    return redirect("/customer/dashboard")
                elif isinstance(person,Admin):
                    login_user(person)
                    return redirect("/admin/dashboard")
                elif isinstance(person,Professional):
                    login_user(person)
                    return redirect("/professional/dashboard")
                else:
                    return redirect("/login")
            
            else:
                flash("Wrong password,try again!!")
                flash("xyz")
                return redirect("/login")
        else:
            return redirect("/")
        


@app.route("/customer/dashboard", methods=["GET","POST"])
@login_required
def cust_dash():
    if request.method=="GET":
        
        return render_template("/customer/dashboard.html",u=current_user)
    
@app.route("/admin/dashboard", methods=["GET","POST"])
@login_required
def admin_dash():
    if request.method=="GET":
        categories = db.session.query(ServiceCategory).all()
        A_p = db.session.query(Professional).filter_by(status = "Active").all()
        R_p = db.session.query(Professional).filter_by(status = "Requested").all()
        F_p = db.session.query(Professional).filter_by(status = "Flagged").all()
        A_c = db.session.query(User).filter_by(status = "Active").all()
        F_c = db.session.query(User).filter_by(status = "Flagged").all()
        return render_template("/admin/dashboard.html",categories=categories,A_p = A_p,R_p=R_p,F_p=F_p,A_c=A_c,F_c=F_c,page="home")
    elif request.method=="POST":
        if request.args.get("action")=="create":
            cat_name= request.form.get("cat_name")
            cat_price=request.form.get("cat_price")
            # cat_desc=request.form.get("cat_desc")
            check_cat =db.session.query(ServiceCategory).filter_by(name =cat_name).first()
            if not check_cat:
                cat = ServiceCategory(name=cat_name,base_price=cat_price)
                db.session.add(cat)
                db.session.commit()
                return redirect("/admin/dashboard")
            else:
                flash("a catefory with the same name is present") 
                return redirect("/admin/dashboard")
        
        elif request.args.get("action")=="edit": 

            id= request.args.get("id")
            cat_change_name =request.form.get("cat_change_name")
            cat_change_price=request.form.get("cat_change_price")
            cat= db.session.query(ServiceCategory).filter_by(id = id).first()
            if cat_change_name:
                cat.name = cat_change_name
            elif cat_change_price:
                cat.base_price = cat_change_price
            db.session.commit()

            return redirect("/admin/dashboard") 
        elif request.args.get("action") == "reject":
            id = request.args.get("id")
            sp = db.session.query(Professional).filter_by(id = id).first()
            sp.status = "Rejected"
            db.session.commit()
            flash(f"{sp.name}'s request is rejected")
            return redirect("/admin/dashboard")
        elif request.args.get("action") == "accept":
            id = request.args.get("id")
            sp = db.session.query(Professional).filter_by(id = id).first()
            sp.status = "Active"
            db.session.commit()
            flash(f"{sp.name}'s request is Accepted")
            return redirect("/admin/dashboard")
        elif request.args.get("action") == "flag":
            id = request.args.get("id")
            if request.args.get("utype") =="professional":
                sp = db.session.query(Professional).filter_by(id = id).first()
                sp.status = "Flagged"
                db.session.commit()
                flash(f"{sp.name}'s is Flagged")
                return redirect("/admin/dashboard")
            elif request.args.get("utype")=="customer":
                cust = db.session.query(User).filter_by(id = id).first()
                cust.status = "Flagged"
                db.session.commit()
                flash(f"{cust.name}'s is Flagged")
                return redirect("/admin/dashboard")

        elif request.args.get("action") == "unflag":

            id = request.args.get("id")
            if request.args.get("utype")=="professional":
                sp = db.session.query(Professional).filter_by(id = id).first()
                sp.status = "Active"
                db.session.commit()
                flash(f"{sp.name}'s is Unflagged")
                return redirect("/admin/dashboard")
            elif request.args.get("utype")=="customer":
                cust = db.session.query(User).filter_by(id = id).first()
                cust.status = "Active"
                db.session.commit()
                flash(f"{cust.name}'s is Unflagged")
                return redirect("/admin/dashboard")


@app.route("/admin/search", methods=["GET","POST"])
@login_required
def admin_search():
    if request.method=="GET":
        return render_template("admin/search.html",page="search" )

@app.route("/professional/dashboard", methods=["GET","POST"])
def pro_dash():
    if request.method=="GET":
        return render_template("/professional/dashboard.html")
    

@app.route("/logout",methods=["GET"])
@login_required
def logout():
    logout_user()
    return redirect("/login")