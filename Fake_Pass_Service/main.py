#-*- coding=utf-8 -*-
from flask import *
from flask_wtf import FlaskForm
from wtforms import *
from flask_bootstrap import Bootstrap
import csv, datetime

import sys
reload(sys)
sys.setdefaultencoding('utf8')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Anti_ZJNU_Project'
bootstrap = Bootstrap(app)

door_choice = [(1, "校西南门_进校通道_1"), (2, "校西南门_出校通道_1"), (3, "校东南门_进校通道_1"), (4, "校东南门_出校通道_1")]
records = []

class get_information(FlaskForm):
    name = StringField('姓名',  validators=[validators.DataRequired()])
    stu_number = StringField('学号',  validators=[validators.DataRequired()])
    door = SelectField(
        label="入校通道",
        validators=[validators.DataRequired()],
        choices = door_choice,
        default = 1
    )
    submit = SubmitField('Submit')

def csv_init():
    fp = open("./records.csv", "r")
    csv_reader = csv.reader(fp)
    return list(csv_reader)
    
def csv_write(name, stu_number, types):
    fp = open("./records.csv", "a")
    csv_writer = csv.writer(fp)
    tmp = [name, stu_number, types, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')]
    csv_writer.writerow(tmp)
    fp.close()


@app.route("/",methods=['GET', 'POST'])
def index():
    form = get_information()
    if form.validate_on_submit():
        csv_write(form.name.data, form.stu_number.data, door_choice[int(form.door.data)-1][1])
        return render_template('detail.html', grade_number=form.stu_number.data[2:4], stu_number=form.stu_number.data, name=form.name.data, door=door_choice[int(form.door.data)-1][1], bar_code_img=url_for("static", filename="./images/fake.png"))
    return render_template('index.html', form=form)

if __name__ == '__main__':
    records = csv_init()
    app.run(debug=True, host="0.0.0.0",port=5000)
