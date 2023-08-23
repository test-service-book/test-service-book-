import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import orm
import datetime


class ListCharacteristics(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'listcharacteristics'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True)

    id_model = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("car_models.id"), nullable=True)
    id_characteristic = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("characteristics.id"), nullable=True)

    volume = sqlalchemy.Column(sqlalchemy.String)
    units = sqlalchemy.Column(sqlalchemy.String)
    regular_condition = sqlalchemy.Column(sqlalchemy.String)
    diffic_condition = sqlalchemy.Column(sqlalchemy.String)
    recomendation = sqlalchemy.Column(sqlalchemy.String)

    model = orm.relationship('CarModels')
    characteristic = orm.relationship('Characteristics')




# 1	3331	1	7.2	л.	210	210
# 2	3331	2	2,2	л.	60	60	API GL-3* и SAE 75W- 90
# 3	3331	3	1	шт.	7.5	None	None
# 4	3331	5	1,15	л.	30	30	“Toyota Genuine Differential Gear Oil LT” «Оригинальное масло для дифференциалов Toyota LT» • Другое трансмиссионное масло, соответствующее характеристикам API GL-5 и SAE 75W-85
# 5	3331	6	1	None	30	None	SAE J1703 или FMVSS No.116 DOT 3
# 6	3331	7	1	45	45	None	None
# 7	3331	8	1	шт.	90	None	None
# 8	3331	9	4	шт.	90	90	DENSO ZXE27HBR8
# 9	3331	10	1	шт.	15	7.5	C-307
# 10	3331	11	5.4	л.	15	7.5	0w20 (5w30)