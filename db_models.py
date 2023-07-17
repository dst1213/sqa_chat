# coding:utf8
"""
python sqlalchemy动态修改tablename两种实现方式_python_脚本之家
https://www.jb51.net/article/277897.htm
"""
import logging

from sqlalchemy import create_engine, Column, Integer, String, MetaData, Table
from sqlalchemy.orm import sessionmaker, declarative_base
from log_tools import slogger
from utils import snake_to_camel, craw_to_db_mapping
from test.fake_data import crawl_to_db3


class MedDataBase:
    def __init__(self, db_name):
        self.db_name = db_name
        self.engine = create_engine(f'sqlite:///{db_name}')
        self.Session = sessionmaker(bind=self.engine)

    def create_database(self, table_name, fields_info, class_name, drop_first=False, back_first=False):
        metadata = MetaData()
        columns = [Column(f, t) for f, t in fields_info.items()]  # 'name':String
        table = Table(table_name, metadata, Column('id', Integer, primary_key=True), *columns)

        # 备份旧表
        if back_first:
            old_table_name = f'old_{table_name}'
            # 删除old表
            try:
                old_table = Table(old_table_name, metadata, autoload_with=self.engine)
                old_table.drop(self.engine, checkfirst=True)  # 只有一份old_table
            except Exception as e:
                slogger.error(f"create_database drop old_table:{old_table_name} failed, error:{e}")
            # 新表备份为old表
            old_table = Table(table_name, metadata, autoload_with=self.engine)
            old_table.__tablename__ = old_table_name

        # 删除已存在的新表
        if drop_first:
            table.drop(self.engine, checkfirst=True)

        metadata.create_all(self.engine)

        # 动态创建类
        Base = declarative_base()
        new_class = type(class_name, (Base,), {'__tablename__': table_name, '__table__': table})
        setattr(self, class_name, new_class)

    def close_database(self):
        self.engine.dispose()

    def write_info(self, class_name, **kwargs):
        session = self.Session()
        obj_class = getattr(self, class_name)
        obj = obj_class(**kwargs)
        session.add(obj)
        session.commit()
        session.close()


def write_table(table_info, table_name='doctor', db_name='test_123', class_name='Doctor', fields_info=None,
                drop_first=True, back_first=True):
    # 使用示例
    db = MedDataBase(f'med_db/{db_name}.db')

    slogger.info(f"table_info type:{type(table_info)}, table_info:{table_info}")

    if fields_info is None:
        fields_info = {k: String for k in table_info.keys()}
    slogger.info(f"db_name:{db_name}, table_name:{table_name}, fields_info:{fields_info}")

    db.create_database(table_name, fields_info, class_name, drop_first=drop_first, back_first=back_first)

    db.write_info(class_name, **table_info)

    db.close_database()

def write_all_tables(user,data=None,drop_first=False,back_first=False):
    # res = crawl_to_db3()  # fake data
    res = craw_to_db_mapping(user, data)
    for k,v in res.items():
        for _v in v:
            _new_v = convert_list_to_str_in_dict(_v)  # list转字符串，防止写入Sqlite的值是list而失败
            write_table(table_info=_new_v, table_name=k, db_name=user, class_name=snake_to_camel(k), fields_info=None,
                        drop_first=drop_first, back_first=back_first)

def convert_list_to_str_in_dict(dictionary):
    for key in dictionary.keys():
        if isinstance(dictionary[key], list):
            dictionary[key] = ', '.join([str(elem) for elem in dictionary[key]])
    return dictionary

if __name__ == "__main__":
    # 使用示例
    db_name = 'fake_db'
    table_name = 'fake_table'
    class_name = 'FakeClass'
    db = MedDataBase(f'med_db/{db_name}.db')

    fields_info = {'name': String, 'expertise': String, 'education': String, 'gender': String, 'age': String}
    db.create_database(table_name, fields_info, class_name)

    table_info = {
        'name': '满祎',
        'expertise': '肿瘤外科',
        'education': '安徽医科大学临床医学专业毕业，研究生学历，副主任医师',
        'gender': '男',
        'age': 41
    }
    db.write_info(class_name, **table_info)

    db.close_database()

def map_table_fields(data,table):
    if not isinstance(data,dict):
        return
