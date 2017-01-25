from flask import Flask, url_for, flash, redirect, request, render_template
from flask import session as login_session
from database_setup import *
from werkzeug.utils import secure_filename
import locale, os




UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.secret_key = "MY_SUPER_SECRET_KEY"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


engine = create_engine('sqlite:///fizzBuzz.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine, autoflush=False)
session = DBSession()



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
@app.route('/Home', methods = ['GET', 'POST'])
def Home():
    if request.method == 'GET':
        return render_template("Home.html")
    elif request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email is None or password is None:
            flash("Missing Arguments")
            return redirect(url_for('Home'))
        if verify_password(email,password) is None:
            flash("Incorrect username or password combination")
            return redirect(url_for('Home'))
        user = verify_password(email,password)
        login_session['email'] = user.Email
        login_session['id'] = user.ID
        login_session['firstname'] = user.FirstName
        login_session['lastname'] = user.LastName
        return redirect(url_for('Home'))



@app.route('/ClientSignUp', methods = ['GET','POST'])
def ClientSignUp():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        password = request.form['password']
        confirmpassword = request.form['confirmpassword']
        birthday = request.form['birthday']
        cellular = request.form['cellular']
        weight = request.form['weight']
        height = request.form['height']
        country = request.form['country']
        gender = request.form['gender']
        picture = request.files['picture']
        if firstname == "" or lastname == "" or email == "" or password == "" or confirmpassword != password or confirmpassword == "" or not allowed_file(picture.filename):
            flash("Your form is missing arguments")
            return redirect(url_for('ClientSignUp'))
        if session.query(Client).filter_by(Email = email).first() is not None:
            flash("A user with this email address already exists")
            return redirect(url_for('ClientSignUp'))
        client = Client(FirstName = firstname,
        				LastName = lastname,
        				Email=email, 
        				Weight = weight,
        				Height = height,
        				Cellular = cellular,
        				Country = country,
        				Gender = gender)
        session.add(client)
        session.commit()
        filename = str(client.ID) + "_" + secure_filename(picture.filename)
        picture.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        client.set_photo(filename)
        client.hash_password(password)
        session.commit()
        flash("User Created Successfully!")
        return redirect(url_for('Home'))
    else:
        return render_template('ClientSignUp.html')

@app.route('/DietitianSignUp', methods = ['GET','POST'])
def DietitianSignUp():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        password = request.form['password']
        confirmpassword = request.form['confirmpassword']
        birthday = request.form['birthday']
        cellular = request.form['cellular']
        aoelist = request.form.getlist('areasofexpertise')
        yoe = request.form['yearsofexperience']
        country = request.form['country']
        gender = request.form['gender']
        picture = request.files['picture']
        if firstname == "" or lastname == "" or email == "" or password == "" or confirmpassword == "" or confirmpassword != password or not allowed_file(picture):
            flash("Your form is missing arguments")
            return redirect(url_for('ClientSignUp'))
        if session.query(Dietitian).filter_by(Email = email).first() is not None:
            flash("A user with this email address already exists")
            return redirect(url_for('ClientSignUp'))

        for x in aoelist:
            print x    

        aoe = ""
        for i in aoelist:
        	aoe += i + ","
        aoe = aoe[:-1]
        dietitian = Dietitian(FirstName = firstname,
        				LastName = lastname,
        				Email=email, 
        				AOE = aoe,
        				YOE = yoe,
        				Cellular = cellular,
        				Country = country,
        				Gender = gender)	
        filename = str(dietitian.ID) + "_" + secure_filename(picture.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        dietitian.set_photo(filename)
        dietitian.hash_password(password)
        session.add(dietitian)
        session.commit()
        flash("User Created Successfully!")
        return redirect(url_for('Home'))
    else:
        return render_template('DietitianSignUp.html')

@app.route("/product/<int:product_id>")
def product(product_id):
	return "To be implemented"

@app.route("/product/<int:product_id>/addToCart", methods = ['POST'])
def addToCart(product_id):
	return "To be implemented"

@app.route("/shoppingCart")
def shoppingCart():
	return "To be implemented"

@app.route("/removeFromCart/<int:product_id>", methods = ['POST'])
def removeFromCart(product_id):
	return "To be implmented"

@app.route("/updateQuantity/<int:product_id>", methods = ['POST'])
def updateQuantity(product_id):
	return "To be implemented"

@app.route("/checkout", methods = ['GET', 'POST'])
def checkout():
	return "To be implmented"

@app.route("/confirmation/<confirmation>")
def confirmation(confirmation):
	return "To be implemented"

@app.route('/logout', methods = ['POST'])
def logout():
	return "To be implmented"

def verify_password(email,password):
    client = session.query(Client).filter_by(Email = email).first()
    dietitian = session.query(Dietitian).filter_by(Email = email).first()
    if client is not None and client.verify_password(password):
        return client
    elif dietitian is not None and dietitian.verify_password(password):
        return dietitian
    return None


if __name__ == '__main__':
	app.run(debug=True)