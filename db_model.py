# coding:utf8
from sqlalchemy import create_engine, Column, Integer, String, MetaData, Table
from sqlalchemy.orm import sessionmaker,declarative_base




class DataEngineer:
    def __init__(self, db_name):
        self.db_name = db_name
        self.engine = create_engine(f'sqlite:///{db_name}')
        self.Session = sessionmaker(bind=self.engine)

    def create_database(self, table_name, fields_info, class_name):
        metadata = MetaData()
        columns = [Column(f,t) for f,t in fields_info.items()]  # 'name':String
        table = Table(table_name, metadata, Column('id', Integer, primary_key=True), *columns)
        metadata.create_all(self.engine)

        # 动态创建类
        Base = declarative_base()
        new_class = type(class_name, (Base,), {'__tablename__': table_name, '__table__': table})
        setattr(self, class_name, new_class)

    def close_database(self):
        self.engine.dispose()

    def write_info(self, table_name, class_name, **kwargs):
        session = self.Session()
        obj_class = getattr(self, class_name)
        obj = obj_class(**kwargs)
        session.add(obj)
        session.commit()
        session.close()


# 使用示例
db = DataEngineer('doctors.db')

fields_info = {'name':String,'expertise':String,'education':String,'gender':String,'age':String}
db.create_database('doctors', fields_info, 'Doctor')

doctor_info = {
    'name': '满祎',
    'expertise': '肿瘤外科',
    'education': '安徽医科大学临床医学专业毕业，研究生学历，副主任医师',
    'gender': '男',
    'age': 41
}
db.write_info('doctors', 'Doctor', **doctor_info)

db.close_database()

