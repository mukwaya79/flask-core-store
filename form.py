from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,DecimalField,DateField
from wtforms.validators import DataRequired,Email


class LoginForm(FlaskForm):
       
       password = PasswordField('password',validators=[DataRequired()])
       email    =StringField('email',validators=[DataRequired(),Email()])
       submit =SubmitField('login')

class Wellboreform(FlaskForm):
       wellboreofficialname= StringField('wellboreofficialname',validators=[DataRequired()])
       wellborelocalname = StringField('wellborelocalname',validators=[DataRequired()])
       wellborespuddate = StringField('wellborespuddate',validators=[DataRequired()])
       wellborealiasname = StringField('wellborealiasname',validators=[DataRequired()])
       spudyear = StringField('spudyear',validators=[DataRequired()])
       wellboretypeid= DecimalField('wellboretypeid',validators=[DataRequired()])
       initialwellborepurposeid= DecimalField('initialwellborepurposeid',validators=[DataRequired()])
    

       submit =SubmitField('submit')


class Wellsform(FlaskForm):
       sampletype= StringField('sampletype',validators=[DataRequired()])
       layer= StringField('layer',validators=[DataRequired()])
       wellname = StringField('wellname',validators=[DataRequired()])
       initialdepth = DecimalField('initialdepth',validators=[DataRequired()])
       terminationdepth  = DecimalField('terminationdepth',validators=[DataRequired()])
       samplebucket = StringField('samplebucket',validators=[DataRequired()])
       
       submit =SubmitField('submit')

class Wellborecoreform(FlaskForm):
       wellboreid =DecimalField('wellboreid',validators=[DataRequired()])
       corenumber= DecimalField('corenumber',validators=[DataRequired()])
       coringdate= StringField('coringdate',validators=[DataRequired()])
       wbcoringcontractorid = DecimalField('wbcoringcontractorid',validators=[DataRequired()])
       
       coretopmdrt= DecimalField('coretopmdrt',validators=[DataRequired()])
       corebtmmdrt = DecimalField('corebtmmdrt',validators=[DataRequired()])
       coretoptvd= DecimalField('corettoptvd',validators=[DataRequired()])
       corebtmtvd= DecimalField('corebtmtvd',validators=[DataRequired()])
       cutlength= DecimalField('cutlength',validators=[DataRequired()])
       cutlengthtvd= DecimalField('cutlengthtvd',validators=[DataRequired()])
       recoveredlength= DecimalField('recoveredlength',validators=[DataRequired()])
       corerecovery= DecimalField('corerecovery',validators=[DataRequired()])
       
       submit =SubmitField('submit')

class Categoryform(FlaskForm):
       wellborecoreid =DecimalField('wellborecoreid',validators=[DataRequired()])
       coretypeid= DecimalField('coretypeid',validators=[DataRequired()])
       storeidentifier= StringField('storeidentifier',validators=[DataRequired()])
       catalogcorefromdepth= DecimalField('catalogcorefromdepth',validators=[DataRequired()])
       
       catalogcoretodepth= DecimalField('catalogcoretodepth',validators=[DataRequired()])
       corecatalogsecurityflagid = DecimalField('corecatalogsecurityflagid',validators=[DataRequired()])
       catalogcorelength= DecimalField('catalogcorelength',validators=[DataRequired()])
       
       submit =SubmitField('submit')
