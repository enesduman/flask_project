import locale
from flask import Flask, render_template, flash, redirect, url_for, session, logging, request, Response
from flask_mongoengine import MongoEngine
from flask_wtf import FlaskForm
from wtforms import (
    Form,
    StringField,
    TextAreaField,
    PasswordField,
    validators,
    HiddenField,
    IntegerField
)
import random
from datetime import datetime as dt
from datetime import timedelta as td
from urllib.parse import urlencode

from functools import wraps
from passlib.hash import sha256_crypt
from flask_security import (
    current_user,
    roles_required,
    login_required,
    roles_accepted,
    Security,
    MongoEngineUserDatastore
)
from uuid import uuid1
from flask_login import LoginManager

from flask_mail import Mail, Message


def check_form(form, **kwargs):
    """
        kwargs:
            obj: either class of the base object or an instance
            populate_obj: if object has to be populated from form
            populate_custom: if forms populate_custom function will be called
            form_has_uuid: form object has uuid field (for updating)
    """
    obj = kwargs.get('obj', None)
    populate_obj = kwargs.get('populate_obj', False)
    populate_custom = kwargs.get('populate_custom', False)

    res = {"valid": False, "form": form, "obj": obj}
    if form.validate_on_submit():
        if obj:
            try:
                if form.uuid.data:
                    print(form.uuid.data)
                    obj = obj.__class__.objects(uuid=form.uuid.data).get()
            except Exception as e:
                pass
            if populate_obj:
                form.populate_obj(obj)
            if populate_custom:
                form.populate_custom(obj)
        res['valid'] = True
        res['obj'] = obj
    else:
        flash_errors(form)
    return res


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "logged_in" in session:
            return f(*args, **kwargs)
        else:
            flash("Bu Sayfayı görüntülemek için lütfen giriş yapınız.", "danger")
            return redirect(url_for("login"))
    return decorated_function


locale.setlocale(locale.LC_ALL, "tr_TR.utf8")

login_manager = LoginManager()
app = Flask(__name__)
db = MongoEngine(app)
login_manager.init_app(app)


app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'kullanılcakmail'
app.config['MAIL_PASSWORD'] = 'parola'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)


def load_user(session_token):
    return User.objects(session_token=session_token).first()


login_manager.user_loader(load_user)


class User(db.Document):
    name = db.StringField(max_length=255)
    email = db.StringField(max_length=255, unique=True, index=True, null=True)
    username = db.StringField(
        max_length=255, unique=True, index=True, null=True)
    password = db.StringField(max_length=255)
    uuid = db.StringField(max_length=255)


class Article(db.Document):
    title = db.StringField(max_length=255)
    content = db.StringField(min_length=10)


class Messagee(db.Document):
    title = db.StringField(max_length=255)
    subject = db.StringField(max_length=255)
    description = db.StringField(max_length=255)
    sender = db.StringField(max_length=255)
    uuid = db.StringField(max_length=255)


class Data(db.Document):
    date = db.StringField(max_length=255)
    h00 = db.FloatField()
    h01 = db.FloatField()
    h02 = db.FloatField()
    h03 = db.FloatField()
    h04 = db.FloatField()
    h05 = db.FloatField()
    h06 = db.FloatField()
    h07 = db.FloatField()
    h08 = db.FloatField()
    h09 = db.FloatField()
    h10 = db.FloatField()
    h11 = db.FloatField()
    h12 = db.FloatField()
    h13 = db.FloatField()
    h14 = db.FloatField()
    h15 = db.FloatField()
    h16 = db.FloatField()
    h17 = db.FloatField()
    h18 = db.FloatField()
    h19 = db.FloatField()
    h20 = db.FloatField()
    h21 = db.FloatField()
    h22 = db.FloatField()
    h23 = db.FloatField()


class Role(db.Document):
    name = db.StringField(max_length=80, unique=True)
    description = db.StringField(max_length=255)

    def __str__(self):
        return str(self.name)

    def __unicode__(self):
        return str(self.name)


user_datastore = MongoEngineUserDatastore(db, User, Role)

Security(app)
login_manager = app.login_manager

app.secret_key = "dumanke"


class RegisterForm(Form):
    name = StringField("İsim Soyisim", validators=[
                       validators.Length(min=4, max=25)])
    username = StringField("Kullanıcı Adı", validators=[
                           validators.Length(min=5, max=35)])
    email = StringField("Email", validators=[validators.Email(
        message="Lütfen Geçerli Bir Email Adresi Girin")])
    password = PasswordField("Parola:", validators=[
        validators.DataRequired(message="Lütfen Bir Parola Belirleyin"),
        validators.EqualTo(fieldname="confirm", message="Parolanız Uyuşmuyor")
    ])
    confirm = PasswordField("Parola Doğrula")


class LoginForm(Form):
    username = StringField("Kullanıcı Adı : ")
    password = PasswordField("Parolayı Giriniz : ")


class MessageeForm(Form):
    uuid = HiddenField()
    title = StringField("Kullanıcı Adı : ")
    subject = StringField("Konu Giriniz : ")
    description = StringField("Açıklama Giriniz : ")
    sender = StringField("Gönderen Bilgisi : ")


class EditForm(Form):
    name = StringField("İsim Soyisim", validators=[
                       validators.Length(min=4, max=25)])
    username = StringField("Kullanıcı Adı", validators=[
                           validators.Length(min=5, max=35)])
    email = StringField("Email", validators=[validators.Email(
        message="Lütfen Geçerli Bir Email Adresi Girin")])
    password = PasswordField("Parola:", validators=[
        validators.DataRequired(message="Lütfen Bir Parola Belirleyin"),
        validators.EqualTo(fieldname="confirm", message="Parolanız Uyuşmuyor")
    ])
    confirm = PasswordField("Parola Doğrula")


class ArticleForm(Form):
    title = StringField("Makale Başlığı", validators=[
                        validators.length(min=5, max=100)])
    content = TextAreaField("Makale İçeriği", validators=[
                            validators.length(min=10)])


class DataForm(Form):
    date = StringField("Gün Girin", validators=[
                       validators.length(min=1, max=20)])
    input_text = TextAreaField("Veri Giriniz")

    def validate_on_submit(self):
        """Call :meth:`validate` only if the form is submitted.
        This is a shortcut for ``form.is_submitted() and form.validate()``.
        """
        return self.is_submitted() and self.validate()

    def is_submitted(self):
        """Consider the form submitted if there is an active request and
        the method is ``POST``, ``PUT``, ``PATCH``, or ``DELETE``.
        """

        return _is_submitted()


SUBMIT_METHODS = set(('POST', 'PUT', 'PATCH', 'DELETE'))


def _is_submitted():
    """Consider the form submitted if there is an active request and
    the method is ``POST``, ``PUT``, ``PATCH``, or ``DELETE``.
    """
    return bool(request) and request.method in SUBMIT_METHODS


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route('/mail/', methods=["GET", "POST"])
def mail_arayuz():
    if request.method == "POST":
        form = MessageeForm(request.form)
        message = Messagee()
        message.uuid = str(uuid1())
        message.title = form.title.data
        message.subject = form.subject.data
        message.description = form.description.data
        message.sender = form.sender.data
        message.save()

        msg = Message((message.subject, message.title),
                      sender=message.sender,
                      recipients=["yorum13333@gmail.com"])
        msg.body = message.description
        mail.send(msg)

        return redirect(url_for('mail_arayuz'))
    else:
        form = MessageeForm()

    print("formcuk", form.title.data)
    return render_template("mail.html", form=form)


@app.route("/register", methods=["GET", "POST"])
@app.route("/update/<string:uid>", methods=["GET", "POST"])
def register(uid=None):
    try:
        if request.method == "POST":
            form = RegisterForm(request.form)
            if uid == None:
                u = User()
                u.uuid = str(uuid1())
                flash("Başarıyla Kayıt Oldunuz", "success")

            else:
                u = User.objects(uuid=uid).get()
                flash("Güncelleme başarılı", "success")
            print("form.password:", form.password,
                  "form.password.data:", form.password.data)
            u.password = form.password.data
            u.name = form.name.data
            u.username = form.username.data
            u.email = form.email.data
            u.save()
            return redirect(url_for("login", form=form))
        else:
            form = RegisterForm()
            return render_template("register.html", form=form)
    except Exception as e:
        print(str(e))
        flash('birşeyler ters gitti!', 'danger')
        return redirect(url_for('.database'))


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)

    if request.method == "POST":
        username = form.username.data
        password = form.password.data
        try:
            u = User.objects(
                username=username,
                password=password
            ).get()
            flash("Başarıyla Giriş Yaptınız.", "success")
            session["logged_in"] = True
            session["username"] = username

        except Exception:
            flash("k.adi veya parola yanlis", "danger")
            return render_template("login.html", form=form)
        return redirect(url_for("index"))

    else:

        return render_template("login.html", form=form)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


@app.route("/database")
@login_required
def database():
    if 'logged_in' in session:
        if session["logged_in"] == True:
            cx = {}
            user_list = User.objects()
            cx['user'] = user_list
            return render_template("database.html", cx=cx)
    else:
        return redirect(url_for(".index"))


@app.route('/userdelete/<string:id>', methods=['GET'])
def userdelete(id):
    u = User.objects(uuid=id).get()
    u.delete()
    flash("Kullanıcı Silindi", "success")
    return redirect(url_for(".database"))


@app.route("/Uuidadd", methods=["GET"])
def Uuidadd():
    u = User.objects
    for a in u:
        a.uuid = str(uuid1())
        a.save()
    flash("Uuid Eklendi", "success")
    return redirect(url_for(".database"))


@app.route("/edit/<string:id>", methods=["GET", "POST"])
def edit(id):
    try:
        if request.method == "GET":
            form = RegisterForm()
            user = User.objects(uuid=id).get()
            form.name.data = user["name"]
            form.username.data = user["username"]
            form.email.data = user["email"]
            form.password.data = user["password"]
            return render_template(
                "edit.html",
                form=form,
                user=user)
    except Exception as e:
        print(str(e))
        flash('birşeyler ters gitti!', 'danger')
        return redirect(url_for('.database'))


@app.route("/editt ", methods=["GET", "POST"])
def editt():
    try:
        if request.method == "GET":
            form = ArticleForm()
            article = Article.objects().get()
            form.title.data = article["title"]
            form.content.data = article["content"]

            return render_template(
                "editt.html",
                form=form,
                article=article)
    except Exception as e:
        print(str(e))
        flash('birşeyler ters gitti!', 'danger')
        return redirect(url_for('.article_content'))


@app.route("/downloads")
def downloads():
    u = User.objects()
    csva = 'İsim,Email,Kullanıcı Adı,Parola\n'
    for user in u:
        csva += user.name + ',' + user.email + ',' + \
            user.username + ',' + user.password + '\n'
    filename = 'database.csv'
    return Response(
        csva,
        mimetype="text/csv",
        headers={"Content-disposition":
                 "attachment; filename=database.csv"}
    )


@app.route("/downloadss")
def downloadss():
    a = Article.objects()
    csva = 'Başlık,İçerik\n'
    for articlee in a:
        csva += articlee.title + ',' + articlee.content + '\n'
    filename = 'makale.csv'
    return Response(
        csva,
        mimetype="text/csv",
        headers={"Content-disposition":
                 "attachment; filename=makale.csv"}
    )


@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")


@app.route("/dashboard/addarticle", methods=["GET", "POST"])
@login_required
def addarticle():
    form = ArticleForm(request.form)
    try:
        if request.method == "POST":
            a = Article()
            a.title = form.title.data
            a.content = form.content.data
            a.save()
            flash("Makale Eklendi", "success")
            return redirect(url_for("dashboard"))
        return render_template("addarticle.html", form=form)
    except Exception as f:
        print(str(f))
        flash("Bir Hata Oluştu", "danger")
        t = redirect(url_for(".addarticle"))
        return (t)


@app.route("/chart")
@login_required
def chart():
    dataset = []
    cx = {}
    items = Data.objects()
    label = ['00.00',
             '01.00',
             '02.00',
             '03.00',
             '04.00',
             '05.00',
             '06.00',
             '07.00',
             '08.00',
             '09.00',
             '10.00',
             '11.00',
             '12.00',
             '13.00',
             '14.00',
             '15.00',
             '16.00',
             '17.00',
             '18.00',
             '19.00',
             '20.00',
             '21.00',
             '22.00',
             '23.00']
    for i in items:
        d = {}
        d['label'] = i.date
        d['data'] = []
        d['backgroundColor'] = 'rgb' + (
            str((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))))

        for a in range(0, 24):
            d['data'].append(int(i["h{:02d}".format(a)]))
        dataset.append(d)

    cx['dataset'] = dataset
    cx['label'] = label

    return render_template("chart.html", cx=cx)


@app.route("/chart/mchart")
@login_required
def mchart():
    dataset = []
    cx = {}
    items = Data.objects()
    label = ['Ocak',
             'Şubat',
             'Mart',
             'Nisan',
             'Mayıs',
             'Haziran',
             'Temmuz',
             'Ağustos',
             'Eylül',
             'Ekim',
             'Kasım',
             'Aralık'
             ]

    tmp_dict = {}
    color_list = []
    for l in label:
        color_list.append('rgb' + (
            str((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))))
        tmp_dict[l] = 0
    for i in items:
        # 01.01.2020
        date_item = dt.strptime(i.date, '%d.%m.%Y')
        month_name = date_item.strftime('%B')
        for a in range(0, 24):
            tmp_dict[month_name] += int(i["h{:02d}".format(a)])

    data = []
    for key, value in tmp_dict.items():
        data.append(value)
    cx['dataset'] = data
    cx['label'] = label
    cx['colorlist'] = color_list

    return render_template("mchart.html", cx=cx)


@app.route("/chart/ychart")
@login_required
def ychart():
    dataset = []
    cx = {}
    items = Data.objects()

    label = ['2016',
             '2017',
             '2018',
             '2019',
             '2020'
             ]

    tmp_dict = {}
    color_list = []
    for l in label:
        color_list.append('rgb' + (
            str((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))))
        tmp_dict[l] = 0
    for i in items:
        # 01.01.2020

        date_item = dt.strptime(i.date, '%d.%m.%Y')
        year_name = date_item.strftime('%Y')
        for a in range(0, 24):
            tmp_dict[year_name] += int(i["h{:02d}".format(a)])

    data = []
    for key, value in tmp_dict.items():
        data.append(value)
    cx['dataset'] = data
    cx['label'] = label
    cx['colorlist'] = color_list

    return render_template("ychart.html", cx=cx)


@app.route("/data", methods=["GET", "POST"])
@login_required
def data():
    form = DataForm(request.form)
    try:
        d = Data()
        if request.method == "POST":
            kw = {'obj': d, 'populate_obj': True}
            res = check_form(form, **kw)
            if res['valid']:
                d = res['obj']
                splitted_rows = res['form'].data['input_text'].split("\r\n")
                for i in range(0, 24):
                    change_format = splitted_rows[i].\
                        replace(',', '').replace('.', '')
                    d["h{:02d}".format(i)] = int(float(change_format))
                d.save()
                flash("Veri Eklendi", "success")
                return redirect(url_for("data"))
        else:
            return render_template("data.html", form=form)
    except Exception as d:
        print(str(d))
        flash("Bir Hata Oluştu", "danger")
        return redirect(url_for(".data"))


@app.route("/article_content")
@login_required
def article_content():
    if 'logged_in' in session:
        if session["logged_in"] == True:
            cx = {}
            article_list = Article.objects()
            cx['article'] = article_list
            return render_template("article_content.html", cx=cx)
    else:
        return redirect(url_for(".index"))


if __name__ == "__main__":
    app.run(debug=True)
