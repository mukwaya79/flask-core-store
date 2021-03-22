from flask import Flask,render_template,url_for,redirect,flash,request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from form import LoginForm, Wellsform, Wellboreform, Wellborecoreform,Categoryform
from flask_login import LoginManager,UserMixin,login_user,login_required,logout_user,current_user
from flask_bcrypt import Bcrypt


app = Flask(__name__)
app.config['SECRET_KEY'] ='kalenzo'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flask.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db =SQLAlchemy(app)
bcrypt =Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key =True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role     = db.Column(db.String(15))

    def __repr__(self):
        return '<User %r>' % self.password

class Wellbore(db.Model):
    wellboreid = db.Column(db.Integer,primary_key =True)
    wellboreofficialname = db.Column(db.String(150), nullable=False)
    wellborelocalname = db.Column(db.String(100), nullable=False)
    wellborealiasname = db.Column(db.String(100), nullable=False)
    spudyear= db.Column(db.String(100), nullable=False)
    wellboretypeid= db.Column(db.Float, nullable=False)
    initialwellborepurposeid= db.Column(db.Float,nullable=False)
    
    wellborespuddate= db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '<Wellbore %r>' % self.wellboreofficialname

class Wells(db.Model):
    id = db.Column(db.Integer,primary_key =True)
    sampletype = db.Column(db.String(150), nullable=False)
    wellname = db.Column(db.String(100), nullable=False)
    layer = db.Column(db.String(150), nullable=False)
    initialdepth = db.Column(db.Float, nullable=False)
    terminationdepth = db.Column(db.Float, nullable=False)
    samplebucket= db.Column(db.String(100), nullable=False)
    uploaddate = db.Column(db.DateTime,default =datetime.now())

    def __repr__(self):
        return '<Wells %r>' % self.sampletype

class Wellborecore(db.Model):
    wellborecoreid = db.Column(db.Integer,primary_key =True)
    corenumber= db.Column(db.Float, nullable=False)
    coringdate= db.Column(db.String(100), nullable=False)
    wellboreid = db.Column(db.Float, nullable=False)
    wbcoringcontractorid = db.Column(db.Float, nullable=False)
    coretopmdrt= db.Column(db.Float, nullable=False)
    corebtmmdrt= db.Column(db.Float, nullable=False)
    coretoptvd= db.Column(db.Float, nullable=False)
    corebtmtvd= db.Column(db.Float, nullable=False)
    cutlength= db.Column(db.Float, nullable=False)
    cutlengthtvd= db.Column(db.Float, nullable=False)
    recoveredlength= db.Column(db.Float, nullable=False)
    corerecovery= db.Column(db.Float, nullable=False)
    recorddate = db.Column(db.DateTime,default =datetime.now())

    def __repr__(self):
        return '<Wellborecore%r>' % self.corenumber

class Category(db.Model):
    corecatalogid = db.Column(db.Integer,primary_key =True)
    wellborecoreid= db.Column(db.Float, nullable=False)
    coretypeid= db.Column(db.Float, nullable=False)
    storeidentifier = db.Column(db.String(100), nullable=False)
    catalogcorefromdepth= db.Column(db.Float, nullable=False)
    catalogcoretodepth= db.Column(db.Float, nullable=False)
    corecatalogsecurityflagid= db.Column(db.Float, nullable=False)
    catalogcorelength= db.Column(db.Float, nullable=False)
    recorddate = db.Column(db.DateTime,default =datetime.now())

    def __repr__(self):
        return '<Category %r>' % self.storeidentifier

@app.route('/dashbord',)
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/',methods =['GET'])
def signin():
    form = LoginForm()
    return redirect(url_for('login'))


@app.route('/login', methods=['GET','POST'])
def login():

    form = LoginForm()
    if request.method == 'POST' :
            user= User.query.filter_by(email=form.email.data).first()
            if user:
                if bcrypt.check_password_hash(user.password,form.password.data) :
                    login_user(user)
                    flash('You are Welcome','success')
                    return redirect(url_for('dashboard'))

                else:
                    flash('login Unsuccessful','danger')
                    return redirect(url_for('signin'))

            else:
                 flash('invalid credentials','danger')
                 return redirect(url_for('signin'))
             
    return render_template('login.html',title='login', form=form)


@app.route('/wellbore/new', methods=['GET','POST'])
def new_wellbore():

    form = Wellboreform()
    if request.method == 'POST':
        oilsample=Wellbore(wellboreofficialname=form.wellboreofficialname.data,wellborelocalname=form.wellborelocalname.data,
        wellborealiasname=form.wellborealiasname.data,wellborespuddate=form.wellborespuddate.data,spudyear=form.spudyear.data,
        wellboretypeid=form.wellboretypeid.data,initialwellborepurposeid=form.initialwellborepurposeid.data)
        db.session.add(oilsample)
        db.session.commit()

        flash('Data successfully Added','success')
        return redirect(url_for('wellbore'))

    return render_template('create_wellbore.html',form=form)

@app.route('/wells/new', methods=['GET','POST'])
def new_wells():

    form = Wellsform()
    if request.method == 'POST':
        oilinfo= Wells(wellname=form.wellname.data,sampletype=form.sampletype.data,layer=form.layer.data,
        initialdepth=form.initialdepth.data,terminationdepth=form.terminationdepth.data,samplebucket=form.samplebucket.data)
        db.session.add(oilinfo)
        db.session.commit()

        flash('Data successfully Added','success')
        return redirect(url_for('wells'))

    return render_template('create_wells.html',form=form)


@app.route('/wellborecore/new', methods=['GET','POST'])
def new_wellborecore():

    form = Wellborecoreform()
    if request.method == 'POST':
        corebase=Wellborecore(wellboreid=form.wellboreid.data,corenumber=form.corenumber.data,coringdate=form.coringdate.data
        ,wbcoringcontractorid=form.wbcoringcontractorid.data,coretopmdrt=form.coretopmdrt.data,corebtmmdrt=form.corebtmmdrt.data,coretoptvd=form.coretoptvd.data,
        corebtmtvd=form.corebtmtvd.data,cutlength=form.cutlength.data,cutlengthtvd=form.cutlengthtvd.data,recoveredlength=form.recoveredlength.data,
        corerecovery=form.corerecovery.data)
        db.session.add(corebase)
        db.session.commit()

        flash('Data successfully Added','success')
        return redirect(url_for('wellborecore'))

    return render_template('create_wellborecore.html',form=form)

@app.route('/category/new', methods=['GET','POST'])
def new_category():

    form = Categoryform()
    if request.method == 'POST':
        cat=Category(wellborecoreid=form.wellborecoreid.data,coretypeid=form.coretypeid.data,storeidentifier=form.storeidentifier.data
        ,catalogcorefromdepth=form.catalogcorefromdepth.data,catalogcoretodepth=form.catalogcoretodepth.data,
        corecatalogsecurityflagid=form.corecatalogsecurityflagid.data,catalogcorelength=form.catalogcorelength.data)
        db.session.add(cat)
        db.session.commit()

        flash('Data successfully Added','success')
        return redirect(url_for('category'))

    return render_template('create_category.html',form=form)

@app.route('/wells')
@login_required
def wells():
    infos = Wells.query.all()

    return render_template('wells.html',infos=infos)

@app.route('/wellbore')
@login_required
def wellbore():
    infos = Wellbore.query.all()

    return render_template('wellbore.html',infos=infos)

@app.route('/wellborecore')
@login_required
def wellborecore():
    infos = Wellborecore.query.all()

    return render_template('wellborecore.html',infos=infos)

@app.route('/category')
@login_required
def category():
    infos = Category.query.all()

    return render_template('category.html',infos=infos)

@app.route('/navigation')
@login_required
def navigation():
    return render_template('navigation.html')

@app.route('/logout')
@login_required
def logout():

    logout_user()
    flash('login to continue','danger')
    return redirect(url_for('login'))

@app.route('/wellborecore/<id>/update', methods=['GET','POST'])
def wellborecoreupdate(id):
    corebase1 = Wellborecore.query.get_or_404(id)
    
    if request.method == 'POST':
        
        corebase1.wellboreid = request.form['wellboreid']
        corebase1.corenumber = request.form['corenumber']
        corebase1.coringdate = request.form['coringdate']
        corebase1.wbcoringcontractorid = request.form['wbcoringcontractorid']
        corebase1.coretopmdrt = request.form['coretopmdrt']
        corebase1.corebtmmdrt = request.form['corebtmmdrt']
        corebase1.coretoptvd = request.form['coretoptvd']
        corebase1.corebtmtvd = request.form['cutlength']
        corebase1.cutlength= request.form['cutlength']
        corebase1.cutlengthtvd= request.form['cutlengthtvd']
        corebase1.recoveredlength= request.form['recoveredlength']
        corebase1.corerecovery = request.form['corerecovery']

        try:
            db.session.commit()

            flash('wellbore core data has been successfully updated','success')
            return redirect(url_for('wellborecore'))
        
        except:
            return 'there is an issue updating the info'

    else:
        return render_template('wellborecore_update.html',corebase1=corebase1)

@app.route('/wells/<id>/update', methods=['GET','POST'])
def wellsupdate(id):
    oilinfo1 = Wells.query.get_or_404(id)
    
    if request.method == 'POST':
        
        oilinfo1.sampletype = request.form['sampletype']
        oilinfo1.wellname = request.form['wellname']
        oilinfo1.layer = request.form['layer']
        oilinfo1.initialdepth = request.form['initialdepth']
        oilinfo1.terminationdepth = request.form['terminationdepth']
        oilinfo1.samplebucket = request.form['samplebucket']
        

        try:
            db.session.commit()

            flash('Wells data has been successfully updated','success')
            return redirect(url_for('wells'))
        
        except:
            return 'there is an issue updating the info'

    else:
        return render_template('wells_update.html',oilinfo1 = oilinfo1)

@app.route('/wellbore/<id>/update', methods=['GET','POST'])
def wellboreupdate(id):
    oilsample1 = Wellbore.query.get_or_404(id)
    
    if request.method == 'POST':
        
        oilsample1.wellboreofficialname= request.form['wellboreofficialname']
        oilsample1.wellborelocalname = request.form['wellborelocalname']
        oilsample1.wellborealiasname= request.form['wellborealiasname']
        oilsample1.wellborespuddate = request.form['wellborespuddate']
        oilsample1.spudyear = request.form['spudyear']
        oilsample1.wellboretypeid = request.form['wellboretypeid']
        oilsample1.initialwellborepurposeid = request.form['initialwellborepurposeid']
      

        try:
            db.session.commit()

            flash('Wellbore data has been successfully updated','success')
            return redirect(url_for('wellbore'))
        
        except:
            return 'there is an issue updating the info'

    else:
        return render_template('wellbore_update.html',oilsample1 = oilsample1)

@app.route('/category/<id>/update', methods=['GET','POST'])
def categoryupdate(id):
    category1 = Category.query.get_or_404(id)
    
    if request.method == 'POST':
        
        category1.wellborecoreid = request.form['wellborecoreid']
        category1.coretypeid = request.form['coretypeid']
        category1.storeidentifier= request.form['storeidentifier']
        category1.catalogcorefromdepth = request.form['catalogcorefromdepth']
        category1.catalogcoretodepth= request.form['catalogcoretodepth']
        category1.corecatalogsecurityflagid = request.form['corecatalogsecurityflagid']
        category1.catalogcorelength = request.form['catalogcorelength']
        
        try:
            db.session.commit()

            flash('Category data has been successfully updated','success')
            return redirect(url_for('category'))
        
        except:
            return 'there is an issue updating the info'

    else:
        return render_template('category_update.html',category1 = category1)



@app.route('/wellborecore/delete/<int:id>')
def deletewellborecore(id):

    item_to_delete = Wellborecore.query.get_or_404(id)
    try:
        flash('item Successfully deleted','success')
        db.session.delete(item_to_delete)
        db.session.commit()
        return redirect(url_for('wellborecore'))
    
    except:
        flash('Unable to delete ','danger')
        return redirect(url_for('wellborecore'))

@app.route('/wells/delete/<int:id>')
def deletewells(id):

    item_to_delete = Wells.query.get_or_404(id)
    try:
        flash('item Successfully deleted','success')
        db.session.delete(item_to_delete)
        db.session.commit()
        return redirect(url_for('Wells'))
    
    except:
        flash('Unable to delete ','danger')
        return redirect(url_for('wells'))

@app.route('/wellbore/delete/<int:id>')
def deletewellbore(id):

    item_to_delete = Wellbore.query.get_or_404(id)
    try:
        flash('item Successfully deleted','success')
        db.session.delete(item_to_delete)
        db.session.commit()
        return redirect(url_for('wellbore'))
    
    except:
        flash('Unable to delete ','danger')
        return redirect(url_for('navigation'))

@app.route('/category/delete/<int:id>')
def deletecategory(id):

    item_to_delete = Category.query.get_or_404(id)
    try:
        flash('item Successfully deleted','success')
        db.session.delete(item_to_delete)
        db.session.commit()
        return redirect(url_for('category'))
    
    except:
        flash('Unable to delete ','danger')
        return redirect(url_for('category'))



















if __name__ == '__main__':
    app.run(debug=True)





