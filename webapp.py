from flask import Flask, url_for, flash, redirect, request, render_template, send_from_directory
from flask import session as login_session
from database_setup import *
from werkzeug.utils import secure_filename
import locale, os
from datetime import datetime




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

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

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
        login_session['pic'] = user.ImageURL

        dietitian = session.query(Dietitian).filter_by(Email = login_session['email']).first()
        print dietitian
        if dietitian is None:
            login_session['type'] = 'Client'
            return redirect(url_for('MySessions'))
        else:
            login_session['type'] = 'Dietitian'
            return redirect(url_for('DietitianSessions'))
            

        



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

        flag = False
        if picture.filename == '':
            flag = True
            if gender == 'Male':
                picture.filename = 'male.jpg'
            else:
                picture.filename = 'female.jpg'
            
        elif not allowed_file(picture.filename):
            flash("Not allowed uploaded file")
            return redirect(url_for('ClientSignUp'))              

        if firstname == "" or lastname == "" or email == "" or password == "" or confirmpassword != password:
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
                        Birthday = birthday,
        				Cellular = cellular,
        				Country = country,
        				Gender = gender)
        session.add(client)
        session.commit()

        print flag

        if flag == False:
            filename = str(client.ID) + "_" + secure_filename(picture.filename)
            picture.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            client.set_photo(filename)
        else:
            client.set_photo(picture.filename)
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

        flag = False
        if picture.filename == '':
            if gender == 'Male':
                picture.filename = 'male.jpg'
            else:
                picture.filename = 'female.jpg'
            flag = True

        elif not allowed_file(picture.filename):
            flash("Not allowed uploaded file")
            return redirect(url_for('ClientSignUp'))  

        if firstname == "" or lastname == "" or email == "" or password == "" or confirmpassword != password:
            flash("Your form is missing arguments")
            return redirect(url_for('DietitianSignUp'))
        if session.query(Dietitian).filter_by(Email = email).first() is not None:
            flash("A user with this email address already esxists")
            return redirect(url_for('DietitianSignUp'))
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
                        Birthday = birthday,
        				Cellular = cellular,
        				Country = country,
        				Gender = gender)
        session.add(dietitian)
        session.commit()
        if not flag:
            filename = str(dietitian.ID) + "_" + secure_filename(picture.filename)
            picture.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            dietitian.set_photo(filename)
        else:
            dietitian.set_photo(picture.filename)
        dietitian.hash_password(password)
        session.commit()
        flash("User Created Successfully!")
        return redirect(url_for('Home'))
    else:
        return render_template('DietitianSignUp.html')


@app.route("/DietitianSessions", methods = ['GET', 'POST'])
def DietitianSessions():
    diet_list = session.query(Appointment).filter_by(Dietitian_id = login_session['id']).all()

    dates = []
    times= []
    for i in diet_list:
        x = i.Time.strftime("%d %B %Y")
        if x[0] == '0':
            x = x[1:]
        dates.append(x)

        x = i.Time.strftime("%I:%M %p")
        if x[0] == '0':
            x = x[1:]
        times.append(x)

    if request.method == 'GET':
        return render_template('DietitianSessions.html', diet_list=diet_list, length = len(diet_list),dates = dates, times = times)
    else:

        time = request.form['date'] + " " + request.form['time']
        date = datetime.strptime(time, "%Y-%m-%d %H:%M")
        if datetime.now() > date:
            flash("Wront Date and Time")
            return  redirect(url_for('DietitianSessions'))
        dietitian = session.query(Dietitian).filter_by(ID = login_session['id']).one()
        appointment = Appointment(Time = date,
                                  Dietitian = dietitian,
                                  Dietitian_id = login_session['id']) 
        session.add(appointment)
        session.commit()
        return redirect(url_for('DietitianSessions'))

@app.route("/Profile/<string:Email>")
def Profile(Email):
    client = session.query(Client).filter_by(Email = Email).first()
    dietitian = session.query(Dietitian).filter_by(Email = Email).first()
    if client is not None:
        return render_template("Profile.html", user = client)
    return render_template("Profile.html", user = dietitian)

@app.route("/BMICalculator")
def BMI():
    return render_template("BMICalculator.html")

@app.route("/Articles")
def Articles():
    articles = session.query(Article).all()
    length = len(articles)
    images = []
    for i in articles:
        images.append(i.ImageURL)

    return render_template("Articles.html", articles = articles, length = length, images = images)

@app.route("/ArticleRedirect/<int:ID>")
def ArticleRedirect(ID):
    article = session.query(Article).filter_by(ID = ID).one()
    return render_template("ArticleRedirect.html", article = article)

@app.route('/AboutUs')
def AboutUs():
    return render_template('AboutUs.html')

@app.route("/Booking", methods = ['GET', 'POST'])
def Booking():
    availablesessions = session.query(Appointment).filter_by(Client = None).all()
    images = []
    dates = []
    times = []

    for i in availablesessions:
        images.append(i.Dietitian.ImageURL)

        x = i.Time.strftime("%d %B %Y")
        if x[0] == '0':
            x = x[1:]
        dates.append(x)

        x = i.Time.strftime("%I:%M %p")
        if x[0] == '0':
            x = x[1:]
        times.append(x)
    length = len(images)
    if request.method == 'GET':
        return render_template("Booking.html", sessions = availablesessions, images = images, length = length, dates = dates, times = times)

    else:
        return redirect(url_for('Booking'))


@app.route("/LogOut")
def LogOut():
    del login_session['email']
    del login_session['id']
    del login_session['firstname']
    del login_session['lastname']
    del login_session['pic']
    del login_session['type']
    return redirect(url_for('Home'))


@app.route("/MySessions")
def MySessions():
    client = session.query(Client).filter_by(ID = login_session['id']).one()
    mysessions = session.query(Appointment).filter_by(Client = client).all()
    return render_template("ClientSessions.html", mysessions = mysessions, length = len(mysessions))

@app.route("/?/<int:ID>",methods=['GET','POST'])
def DeleteSession(ID):
    appointment = session.query(Appointment).filter_by(ID = ID).first()
    session.delete(appointment)
    session.commit()
    return redirect(url_for('DietitianSessions'))

@app.route("/??/<int:ID>",methods=['GET','POST'])
def BookSession(ID):
    appointment = session.query(Appointment).filter_by(ID = ID).first()
    client = session.query(Client).filter_by(ID = login_session['id']).first()
    appointment.Client = client
    session.commit()

    return redirect(url_for('Booking'))



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