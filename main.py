from flask import Flask, render_template, redirect, url_for, request, session
from data import db_session
from flask_restful import reqparse, abort, Api, Resource
import secrets


from sqlalchemy import func


from requests import post, get, put, delete
from collections import defaultdict
from pprint import pprint
from datetime import datetime

from forms.register import RegisterForm
from forms.reg_category import RegCompanyForm
from forms.login import LoginForm
from forms.add_work import AddWorkForm
from forms.add_worker import AddWorkerForm
from forms.add_car import AddCarForm
from forms.change_owner import ChangeOwner
from forms.check_mail_code import CheckMailCode
from forms.choose_for_edit_characteristics import ChooseForEdit
from forms.add_selfwork import AddSelfWorkForm
from forms.send_support import SendSupport



from flask_login import LoginManager, login_user, logout_user, login_required, current_user




from data.user import User
from data.worker import Worker
from data.category import Category
from data.car import Car
from data.reg_company import RegCompany
from data.work import Work
from data.code import Code
from data.carcode import CarCode
from data.carmodel import CarModel
from data.characteristics import Characteristics
from data.list_characteristics import ListCharacteristics
from data.role import Role
from data.rolesusers import RolesUsers
from data.mail_code import MailCode
from data.car_marks import CarMarks
from data.car_models import CarModels
from data.company import Company
from data.otherwork import OtherWork

from api import user_resources
from api import category_resources
from api import company_resources
from api import worker_resources
from api import car_resources
from api import work_resources
from api import reg_company_resources
from api import car_models


from functions import generate_code_for_transaction
from configs import CONFIGS

from settings import DB_ADRESS, URL, HOST, PORT
from security import Security
from MailSender import MailSender

import locale
locale.setlocale(locale.LC_ALL, "ru_RU")

app = Flask(__name__)

app.config['SECRET_KEY'] = 'top_secret_key'
# app.config['DEBUG'] = True
app.config.update(CONFIGS)



api = Api(app)

mail_sender = MailSender(app)


login_manager = LoginManager()
login_manager.init_app(app)


db_session.global_init(DB_ADRESS)

security = Security(User, Role, RolesUsers, db_session.create_session())

api.add_resource(user_resources.UserListResource, '/api/user')
api.add_resource(user_resources.UserResource, '/api/user/<int:id>')
api.add_resource(category_resources.CategoryListResource, '/api/category')
api.add_resource(category_resources.CategoryResource, '/api/category/<int:id>')
api.add_resource(company_resources.CompanyListResource, '/api/company')
api.add_resource(company_resources.CompanyResource, '/api/company/<int:id>')
api.add_resource(worker_resources.WorkerListResource, '/api/worker')
api.add_resource(worker_resources.WorkerResource, '/api/worker/<int:id>')
api.add_resource(car_resources.CarListResource, '/api/car')
api.add_resource(car_resources.CarResource, '/api/car/<int:id>')
api.add_resource(work_resources.WorkListResource, '/api/work')
api.add_resource(work_resources.WorkResource, '/api/work/<int:id>')
api.add_resource(reg_company_resources.RegCompanyListResource, '/api/reg_company')
api.add_resource(reg_company_resources.RegCompanyResource, '/api/reg_company/<int:id>')
api.add_resource(car_models.CarModelsResource, '/api/car_models/<int:id>')







@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    session[user_id] = [{'id': car.id, 'name': car.get_name()} for car in db_sess.query(Car).filter(Car.owner_id == user_id).all()]
    return db_sess.query(User).filter(User.id==user_id).first()


def comp_workers(id):
    session = db_session.create_session()
    workers = session.query(Worker).filter(Worker.company_id == id).all()
    return workers


@app.route('/')
@app.route('/index')
def index():
    param = {}
    param['username'] = "Евгений К"
    param['title'] = 'Домашняя страница'
    return render_template('main.html', **param)


@app.route('/reg_company', methods=['GET', 'POST'])
def reg_company():
    form = RegCompanyForm()
    if form.validate_on_submit():
        data = dict()
        data['name'] = form.name.data
        data['about']= form.about.data
        data['phone']= form.phone.data
        data['location'] = form.location.data
        data['INN'] = form.INN.data
        data['email'] = form.email.data
        data['password'] = form.password.data

        res = post(URL + '/api/reg_company', json=data)
        if res:



            return redirect('/index')
        else:
            return render_template('reg_company.html', title='Подача заявки на реистрацию компании',
                                   form=form, message='Ошибка. Данные заполнены неверно')


    return render_template('reg_company.html', title='Подача заявки на реистрацию компании', form=form)

@app.route('/check_code', methods=['GET', 'POST'])
def check_code():

    form = CheckMailCode()
    hash = request.args.get('hash')
    if not hash:
        return redirect('/')

    if form.validate_on_submit():
        code = form.code.data

    if request.method == 'GET':
        code = request.args.get('code')


    if code:
        db_sess = db_session.create_session()
        mc = db_sess.query(MailCode).filter(MailCode.hash == hash, MailCode.code == code).first()
        if not mc:
            return render_template('check_code.html', form=form, message='Неверный код')

        user = db_sess.query(User).filter(User.id == mc.user_id).first()

        if db_sess.query(Company).filter(Company.user_id == user.id).first():
            security.set_role(user, 'company')
        else:
            security.set_role(user, 'user')

        user.activate_user()
        db_sess.delete(mc)

        db_sess.commit()
        return redirect('/login')


    return render_template('check_code.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def reqister():

    if current_user.is_authenticated:
        return redirect('/account')

    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data,
            phone=form.phone.data,
            role = 1
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()

        code = MailCode(
            hash=secrets.token_urlsafe(16),
            code=generate_code_for_transaction(5),
            user_id=db_sess.query(User).filter(User.email == form.email.data).first().id
        )
        db_sess.add(code)
        db_sess.commit()

        mail_sender.send_registration_code(form.email.data, code.hash, code.code)



        return redirect(f'/check_code?hash={code.hash}')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect('/account')

    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()

        if not user:
            return render_template('login.html', title='Авторизация', form=form,
                                   message='Пользователь в системе не зарегистрирован.')

        if not user.is_activated:
            return render_template('login.html', title='Авторизация', form=form, message='Завершите регистрацию. Перейдите по ссылке, отправленной на почту.')

        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            if user.role == 1:
                return redirect('/user_account')
            elif user.role == 2:
                return redirect('/company_account')
            elif user.role == 3:
                return redirect('/moderator_account')
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/user_account')
@login_required
@security.role_required('user')
def user_account():
    sess = db_session.create_session()
    cars = sess.query(Car).filter(Car.owner_id==current_user.id).all()
    return render_template('user_account.html', title='Личный кабинет', cars=cars)


@app.route('/company_account')
@login_required
@security.role_required('company')
def company_account():

    return render_template('company_account.html', title='Личный кабинет', workers=comp_workers(current_user.id))


@app.route('/moderator_account')
@login_required
@security.role_required('moderator')
def moderator_account():
    # message = request.args['messages']
    session = db_session.create_session()
    regs = session.query(RegCompany).filter(RegCompany.accepted == False).all()

    return render_template('moderator_account.html', title='Личный кабинет', regs=regs)


@app.route('/accept_company/<int:id>')
@login_required
@security.role_required('moderator')
def accept_company(id):

    session = db_session.create_session()

    reg_com = session.query(RegCompany).filter(RegCompany.id == id).first()

    if not reg_com:
        return redirect('/moderator_account')

    user = User(
        name=reg_com.name,
        about=reg_com.about,
        email=reg_com.email,
        hashed_password=reg_com.hashed_password,
        phone=reg_com.phone
    )


    comp = Company(
        name=reg_com.name,
        about=reg_com.about,
        phone=reg_com.phone,
        location=reg_com.location,
        INN=reg_com.INN,
        user=user
    )
    session.add(comp)

    user = session.query(User).filter(User.email == user.email).first()

    code = MailCode(
        hash=secrets.token_urlsafe(16),
        code=generate_code_for_transaction(5),
        user_id=user.id
    )
    session.add(code)


    mail_sender.send_registration_code(user.email, code.hash, code.code)

    reg_com.accepted = 1
    session.commit()

    return redirect('/moderator_account')


@app.route('/reject_company/<int:id>')
@login_required
@security.role_required('moderator')
def reject_company(id):
    delete(URL + f'/api/reg_company/{id}')
    return redirect('/moderator_account')


@app.route('/add_work', methods=['GET', 'POST'])
@login_required
@security.role_required('company')
def add_work():
    form = AddWorkForm()
    session = db_session.create_session()

    workers = session.query(Worker).filter(Worker.company_id==current_user.id).all()
    characteristic = session.query(Characteristics).all()
    cars = session.query(Car).all()

    form.worker.choices = [(worker.id, worker.name) for worker in workers]
    form.characteristic.choices = [(ch.id, ch.name) for ch in characteristic]

    data = {'brand': form.brand.data, 'amount': form.amount.data}

    if form.validate_on_submit():

        code = session.query(CarCode).filter(CarCode.code == form.code.data).first()
        if not code:
            return render_template('add_work.html', title='Обслужить автомобиль', form=form,
                                   workers=workers, message='Нет такого кода пользователя')

        car = session.query(Car).filter(Car.id == code.car_id).first()
        # car = session.query(Car).filter(Car.id == int(form.car.data.split()[-1][1:-1])).first()
        # data['worker_id'] = form.worker.data.split()[-1][1:-1]
        # data['category_id'] = form.category.data.split()[-1][1:-1]
        # data['car_id'] = form.car.data.split()[-1][1:-1]
        data['worker_id'] = form.worker.data
        data['characteristic_id'] = form.characteristic.data
        data['car_id'] = car.id

        data['company_id'] = current_user.id
        data['millage'] = form.millage.data

        send_work = post(URL + '/api/work', json=data)
        send_millage = put(f'{URL}/api/car/{data["car_id"]}', json={'millage': form.millage.data})

        if send_work:
            return render_template('add_work.html', title='Обслужить автомобиль', form=form,
                                   workers=workers, message='Добавлено')
        else:
            return render_template('add_work.html', title='Обслужить автомобиль', form=form,
                                   workers=workers, message=send_work.content)

    return render_template('add_work.html', title='Обслужить автомобиль', form=form,  workers=workers)


@app.route('/add_other_work', methods=['GET', 'POST'])
@login_required
@security.role_required('company')
def add_other_work():
    form = AddWorkForm()
    sess = db_session.create_session()
    company = sess.query(Company).filter(Company.user_id==current_user.id).first()

    # использую форму из добавления работы, brand=description
    # for validation
    form.amount.data = '0'
    form.characteristic.choices = [(0, '1')]
    form.characteristic.data = '0'

    workers = sess.query(Worker).filter(Worker.company_id==company.id).all()


    form.worker.choices = [(worker.id, worker.name) for worker in workers]

    if form.validate_on_submit():
        code = sess.query(CarCode).filter(CarCode.code == form.code.data).first()
        if not code:
            return render_template('add_other_work.html', title='Обслужить автомобиль', form=form,
                                   workers=workers, message='Нет такого кода пользователя')

        car = sess.query(Car).filter(Car.id == code.car_id).first()

        work = OtherWork()
        work.description = form.brand.data
        work.millage = form.millage.data
        work.company_id = company.id
        work.worker_id = form.worker.data
        work.car_id = car.id
        sess.add(work)
        sess.commit()
        send_millage = put(f'{URL}/api/car/{car.id}', json={'millage': form.millage.data})

        if send_millage:
            return render_template('add_other_work.html', title='Обслужить автомобиль', form=form,
                                   workers=workers, message='Добавлено')
        else:
            return render_template('add_other_work.html', title='Обслужить автомобиль', form=form,
                                   workers=workers, message=send_work.content)

    return render_template('add_other_work.html', title='Обслужить автомобиль', form=form,  workers=workers)




@app.route('/add_selfwork', methods=['GET', 'POST'])
@login_required
@security.role_required('user')
def add_selfwork():
    form = AddSelfWorkForm()
    session = db_session.create_session()

    characteristic = session.query(Characteristics).all()
    cars = session.query(Car).filter(Car.owner_id==current_user.id).all()

    form.characteristic.choices = [(ch.id, ch.name) for ch in characteristic]
    form.car.choices = [(car.id, car.car_models.name) for car in cars]

    if form.validate_on_submit():

        print(form.car.data)
        car = session.query(Car).filter(Car.id == form.car.data).first()

        work = Work(
            brand=form.brand.data,
            amount=form.amount.data,
            millage=form.millage.data,
            company_id=2,
            car_id=form.car.data,
            worker_id=2,
            characteristic_id=form.characteristic.data
        )
        car.millage=form.millage.data

        session.add(work)
        session.commit()
        return redirect('/user_account')

        # # car = session.query(Car).filter(Car.id == int(form.car.data.split()[-1][1:-1])).first()
        # # data['worker_id'] = form.worker.data.split()[-1][1:-1]
        # # data['category_id'] = form.category.data.split()[-1][1:-1]
        # # data['car_id'] = form.car.data.split()[-1][1:-1]
        # data['worker_id'] = form.worker.data
        # data['characteristic_id'] = form.characteristic.data
        # data['car_id'] = car.id
        #
        # data['company_id'] = current_user.id
        # data['millage'] = form.millage.data
        #
        # send_work = post(URL + '/api/work', json=data)
        # send_millage = put(f'{URL}/api/car/{data["car_id"]}', json={'millage': form.millage.data})
        #
        # if send_work:
        #     return render_template('add_work.html', title='Обслужить автомобиль', form=form,
        #                            workers=workers, message='Добавлено')
        # else:
        #     return render_template('add_work.html', title='Обслужить автомобиль', form=form,
        #                            workers=workers, message=send_work.content)

    return render_template('add_selfwork.html', title='Обслужить автомобиль', form=form, cars=cars)


@app.route('/add_other_selfwork', methods=['GET', 'POST'])
@login_required
@security.role_required('user')
def add_other_selfwork():
    form = AddSelfWorkForm()
    session = db_session.create_session()

    cars = session.query(Car).filter(Car.owner_id==current_user.id).all()

    # brand будет использоваться для описания работы
    # for validation
    form.characteristic.choices = [(0, '0')]
    form.characteristic.data = '0'
    form.amount.data='0'

    form.car.choices = [(car.id, car.car_models.name) for car in cars]

    pprint([(f.name, f.data)for f in form])
    if form.validate_on_submit():

        print(form.car.data, type(form.car.data))
        car = session.query(Car).filter(Car.id == form.car.data).first()

        work = OtherWork(
            description=form.brand.data,
            millage=form.millage.data,
            car_id=form.car.data,
            company_id=2,
            worker_id=2
        )
        car.millage=form.millage.data

        session.add(work)
        session.commit()
        return redirect('/user_account')

        # # car = session.query(Car).filter(Car.id == int(form.car.data.split()[-1][1:-1])).first()
        # # data['worker_id'] = form.worker.data.split()[-1][1:-1]
        # # data['category_id'] = form.category.data.split()[-1][1:-1]
        # # data['car_id'] = form.car.data.split()[-1][1:-1]
        # data['worker_id'] = form.worker.data
        # data['characteristic_id'] = form.characteristic.data
        # data['car_id'] = car.id
        #
        # data['company_id'] = current_user.id
        # data['millage'] = form.millage.data
        #
        # send_work = post(URL + '/api/work', json=data)
        # send_millage = put(f'{URL}/api/car/{data["car_id"]}', json={'millage': form.millage.data})
        #
        # if send_work:
        #     return render_template('add_work.html', title='Обслужить автомобиль', form=form,
        #                            workers=workers, message='Добавлено')
        # else:
        #     return render_template('add_work.html', title='Обслужить автомобиль', form=form,
        #                            workers=workers, message=send_work.content)

    return render_template('add_other_selfwork.html', title='Обслужить автомобиль', form=form, cars=cars)



@app.route('/add_worker', methods=['GET', 'POST'])
@login_required
@security.role_required('company')
def add_worker():
    form = AddWorkerForm()
    if form.validate_on_submit():
        data = {
            'name' : form.name.data,
            'phone' : form.phone.data,
            'about' : form.about.data,
            'company_id' : current_user.id
        }
        res = post(f'{URL}/api/worker', json=data)
        if res:
            return redirect('/company_account')

    return render_template('add_worker.html', title='Добавить сотрудника', form=form, workers=comp_workers(current_user.id))


@app.route('/add_car', methods=['GET', 'POST'])
@login_required
@security.role_required('user')
def add_car():
    session = db_session.create_session()
    form = AddCarForm()
    form.mark.choices = [(mark.id, mark.name) for mark in session.query(CarMarks).all()]
    form.model.choices = [(model.id, model.name) for model in session.query(CarModels).filter(CarModel.id == form.mark.choices[0][0]).all()]

    form.engine.choices = [(0, 'Бензин'), (1, 'Дизель'), (2, 'Гибрид'), (3, 'Электро')]
    form.drive_unit.choices = [(0, 'Передний привод'), (1, 'Задний привод')]
    form.transmission.choices = [(0, 'АКПП'), (1, 'МКПП'), (2, 'Вариатор'), (3, 'Робот')]


    if form.validate_on_submit():
        data = {
            'model' : form.model.data,
            'millage' : form.millage.data,
            'year' : form.year.data,
            'body_number' : form.body_number.data,
            'engine_number': form.engine_number.data,
            'owner_id': current_user.id,
            'state_number': form.state_number.data,
            'engine': form.engine.data,
            'transmission': form.transmission.data,
            'drive_unit': form.drive_unit.data,
            'car_model_id': form.model.data
        }
        res = post(f'{URL}/api/car', json=data)



        if res:
            return redirect('/user_account')

    return render_template('add_car.html', title='Добавить автомобиль', form=form, cars=ucars(current_user.id))


@app.route('/car/<id>', methods=['GET'])
@login_required
@security.role_required('user')
def about_car(id):
    session = db_session.create_session()
    car = session.query(Car).filter(Car.id==id).first()
    works = session.query(Work).filter(Work.car_id==id, Work.company_id != 1).all()
    other_works = session.query(OtherWork).filter(OtherWork.car_id==id).all()
    cars = [{'id': car.id, 'car': f'{car.car_models.mark.name} {car.car_models.name}'} for car in current_user.cars]
    list_features = session.query(ListCharacteristics).filter(ListCharacteristics.id_model == car.car_model_id).all()

    has_initial = bool(session.query(Work.id).filter(Work.company_id==1, Work.car_id==id).all())

    last_works = session.query(Work.id, Work.characteristic_id, Work.millage, Work.characteristics,  func.max(Work.date)).filter(Work.car_id==id).group_by(Work.characteristic_id).all()
    last_works = { work[1]: work  for work in last_works}

    res = []
    for feature in list_features:
        f = last_works.get(feature.id_characteristic)
        if f:
            millage = int(f[2])
        else:
            millage = 0

        rec_millage = 0
        if feature.regular_condition and feature.regular_condition != 'None':
            rec_millage = millage + float(feature.regular_condition) * 1000

        res.append([feature.characteristic.name, int(rec_millage), int(rec_millage-car.millage), int(rec_millage - millage) ])

    res.sort(key=lambda x: x[2])

    return render_template('car.html', title='Информация о ТО', car=car, works=works, other_works=other_works, cars=cars, list_features=res, has_initial=has_initial)


@app.route('/company/<id>', methods=['GET'])
@login_required
@security.role_required('user')
def about_company(id):
    sess = db_session.create_session()
    company = sess.query(Company).filter(Company.id==id).first()

    return render_template('about_company.html', title='Информация о компании', company=company)



@app.route('/change_owner', methods=['GET', 'POST'])
@login_required
@security.role_required('user')
def change_owner():
    session = db_session.create_session()
    cars = session.query(Car).filter(Car.owner_id == current_user.id).all()


    form = ChangeOwner()
    form.message = (None, None)
    form.car.choices = [(car.id, car.model) for car in cars]
    if form.validate_on_submit():
        new_owner = session.query(Code).filter(Code.code == form.user.data).first()
        car = session.query(Car).filter(Car.id == form.car.data).first()
        if car:
            car.owner_id = new_owner.user_id
            session.commit()
            form.message = (1, 'Владелец изменен')
            return render_template('change_owner.html', title='Изменение владельца', form=form,
                                   cars=ucars(current_user.id))

    return render_template('change_owner.html', title='Изменение владельца', form=form, cars=ucars(current_user.id))


@app.route('/generate_code', methods=['GET', 'POST'])
@login_required
@security.role_required('user')
def generate_code():
    sess = db_session.create_session()

    user_cars = sess.query(Car).filter(Car.owner_id==current_user.id).all()

    usercode = sess.query(Code).filter(Code.user_id == current_user.id).first()
    if not usercode:

        while True:
            generated_code = generate_code_for_transaction()
            if not session.query(Code).filter(Code.code == generated_code).first():
                break


        usercode = Code(code=generated_code, user_id=current_user.id)
        session.add(usercode)

    codes = []
    for car in user_cars:
        carcode = sess.query(CarCode).filter(CarCode.car_id == car.id).first()
        if not carcode:
            while True:
                generated_code = generate_code_for_transaction()
                if not sess.query(CarCode).filter(CarCode.code == generated_code).first():
                    break

            carcode = CarCode(code=generated_code, car_id=car.id)
            session.add(carcode)
        codes.append(carcode)
    print(codes)






    sess.commit()



    return render_template('generate_code.html', title='Генерация кода', cars=user_cars, code=usercode, codes=codes)





@app.route('/init_characteristics/<id_car>', methods=['GET', 'POST'])
@login_required
@security.role_required('user')
def init_characteristics(id_car:int):
    '''для расчета следующей замены нужны данные последней замены. Тут пользователь будет вводить,
    возможно и примерные, даты последних замен при первоначальном добавлении машины.
    записи добавляются в таблицу work, компания с id = 1, эта компания только для начальной инициализации'''
    session = db_session.create_session()
    car = session.query(Car).filter(Car.id==id_car).first()
    car_model = session.query(CarModels).filter(CarModels.id==car.car_model_id).first()
    list_characteristics = session.query(ListCharacteristics).filter(ListCharacteristics.id_model == car_model.id).all()
    works = session.query(Work).filter(Work.company_id==1, Work.car_id==id_car).all()
    works = {work.characteristic_id:work.millage for work in works}

    data = dict()
    for l in list_characteristics:
        data[l.characteristic.name] = (works.get(l.id_characteristic, ''), l.id_characteristic)

    if request.method == 'POST':
        # pprint(data)
        # pprint(list(request.form.to_dict().items()))
        # for k, v in request.form.to_dict().items():
        #     # print(k, v)
        #     if not v:
        #         return render_template('init_characteristics.html',
        #                                title='Настройка системы рекомендаций',
        #                                car=car, data=data, message='Заполнены не все поля',
        #                                cars=ucars(current_user.id))
        #
        # works = session.query(Work).filter(Work.company_id == 1, Work.car_id == id_car).delete()

        from datetime import timedelta

        for k, v in request.form.to_dict().items():
            if v:
                tmp = Work()
                tmp.characteristic_id = int(k)
                tmp.company_id = 1
                tmp.millage = int(v)
                tmp.date = datetime.now() - timedelta(days=300) # минус дата для теста
                tmp.car_id = id_car
                tmp.worker_id = 1
                session.add(tmp)
        session.commit()
        return redirect(f'/car/{car.id}')
        return render_template('init_characteristics.html',
                               title='Настройка системы рекомендаций',
                               car=car, data=data, message='Done', cars=ucars(current_user.id))







    return render_template('init_characteristics.html', title='Настройка системы рекомендаций',
                           car=car, data=data, cars=ucars(current_user.id))
    # return '1'




@app.route('/test', methods=['GET'])
def test():

    session = db_session.create_session()

    # запись информации об авто в базу
    # from requests import get
    # session.query(CarMarks).delete()
    # session.query(CarModels).delete()
    #
    # for mark in get('https://cars-base.ru/api/cars').json():
    #     name = mark['name']
    #     print(name)
    #     car_mark = CarMarks(name=name)
    #     for model in get(f'https://cars-base.ru/api/cars/{mark["id"]}').json():
    #         car = CarModels(name=model['name'], mark=car_mark)
    #         session.add(car)
    # # pprint(get('https://cars-base.ru/api/cars').json())
    # session.commit()




    # from datetime import datetime
    # print(int(datetime.fromisoformat('2015-01-20').timestamp()))
    # print(int(datetime.fromisoformat('2015-04-21').timestamp()))
    # print(int(datetime.fromisoformat('2015-12-19').timestamp()))
    # print(int(datetime.fromisoformat('2016-03-24').timestamp()))
    # print(int(datetime.fromisoformat('2016-05-04').timestamp()))
    # print(int(datetime.fromisoformat('2016-07-23').timestamp()))
    # print(int(datetime.fromisoformat('2016-07-04').timestamp()))
    # print(datetime.fromtimestamp(1484013552))

# 21.04.2015
# 19.12.2015
# 24.03.2016
# 04.05.2016
# 23.07.2016
# 04.07.2016'))



    return '123'


# ________________MODERATOR PAGES_____________________

@app.route('/edit_characteristics/<int:id_model>', methods=['GET', 'POST'])
@login_required
@security.role_required('moderator')
def edit_caracteristics(id_model):

    # Охлаждающая жидкость инвертора

    session = db_session.create_session()
    car = session.query(CarModels).filter(CarModels.id==id_model).first()
    titles = {'regular_condition' : 'Обычные условия' , 'diffic_condition': 'Пробег при сложных условиях', 'recomendation':'Рекомендации','volume': 'Объем/Количество', 'units': 'Единицы измерения'}



    features = [f.to_dict() for f in session.query(Characteristics).order_by(Characteristics.name).all()]
    list_features = {f.id_characteristic : f.to_dict(only=('volume', 'diffic_condition', 'regular_condition', 'recomendation', 'units', 'id_characteristic', 'id_model')) for f in session.query(ListCharacteristics).filter(ListCharacteristics.id_model == id_model).all()}

    if request.method == 'POST':
        d = defaultdict(dict)

        for k, v in request.form.to_dict().items():
            # print(k, v)
            name, ind = k.split('-')
            d[ind][name] = v


        res_d = {}
        for k, v in d.items():
            # if v['volume'] and (v['regular_condition'] or v['diffic_condition']):
            if v['regular_condition']:
                res_d[k] = v

        # print(res_d.items())

        # session.query(ListCharacteristics).filter(ListCharacteristics.id_model == id_model).delete()

        for k, v in res_d.items():

            character = ListCharacteristics(id_model=id_model, id_characteristic=int(k))
            if v['diffic_condition']: character.diffic_condition = v['diffic_condition']
            if v['regular_condition']: character.regular_condition = v['regular_condition']
            if v['units']: character.units = v['units']
            if v['recomendation']: character.recomendation = v['recomendation']
            if v['volume']: character.volume = v['volume']
            session.add(character)

        session.commit()
        return redirect(f'/edit_characteristics/{id_model}')



    return render_template('edit_characteristics.html', title='Редактирование характеристик', car=car, features=features, list_features=list_features, titles=titles)



@app.route('/choose_for_edit_characteristics', methods=['GET', 'POST'])
@login_required
@security.role_required('moderator')
def chooese_for_edit_caracteristics():
    form = ChooseForEdit()

    session = db_session.create_session()
    form.mark.choices = [(mark.id, mark.name) for mark in session.query(CarMarks).all()]
    form.model.choices = [(model.id, model.name) for model in session.query(CarModels).filter(
        CarModel.id == form.mark.choices[0][0]).all()]

    if form.validate_on_submit():
        return redirect(f'/edit_characteristics/{form.model.data}')

    return render_template('choose_for_edit.html', title='Редактирование характеристик', form=form)


@app.route('/send_support', methods=['GET', 'POST'])
def send_support():
    form = SendSupport()

    if form.validate_on_submit():
        mail_sender.send_support_message(form.email.data, form.subject.data, form.text.data, form.fio.data, form.link.data)
        return redirect('/account')




    return render_template('send_support.html', title='Написать в поддержку', form=form)




@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(403)
def page_access_denied(e):
    return render_template('403.html'), 403


@app.route('/account')
@login_required
def account():
    role = current_user.roles[0].name
    if 'user' == role:
        return redirect('/user_account')
    if 'company' == role:
        return redirect('/company_account')
    if 'admin' == role:
        return redirect('/admin_account')
    if 'moderator' == role:
        return redirect('/moderator_account')

    redirect('/')

if __name__ == '__main__':
    app.run(port=PORT, host=HOST)


#TODO В таблице с машинами поле для идентификатора к таблице с общими характеристиками машины
#TODO Поле в компании дата регистрации

#TODO удаление машины?
# удаление сотрудника
# инициализация бд тестовыми данными
# инициализация бд данными (компания для рекомендаций и самообслуживанию)
# вывод основных характеристик авто
# продумать вывод сообщений


