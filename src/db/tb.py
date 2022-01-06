import pandas as pd
import numpy as np
import pymysql
from sqlalchemy import create_engine
import time
# import var
from src.db import var
import os
import datetime
import hashlib


def change_database_sqlmode():
    # 初始化数据库连接，使用pymysql模块
    # MySQL的用户：root, 密码:LxflRwnEawVIr8Q8, 端口：3306,数据库：webdev
    engine = create_engine(var.engine_creation)
    sql = "select @@global.sql_mode;"
    dfData = pd.read_sql_query(sql, engine)
    sql_mode = str(dfData.iloc[0][0])
    sql_mode = sql_mode.replace('ONLY_FULL_GROUP_BY,', '')
    # 连接数据库
    conn = var.pymysql_connect()
    # 使用cursor()方法创建光标
    cur = conn.cursor()
    sql = "set @@global.sql_mode ='" + sql_mode + "';"
    cur.execute(sql)


'''
    建表函数:table_create
    table:int   数据表，取值1-5分别表示 tbUser、tbRequest、tbResponse、tbSuccess、tbProfit;
'''


def table_create(table):
    # 索引为table
    table = table - 1
    # 表名
    tb_Name = var.table_Name[table]
    # 连接数据库
    conn = var.pymysql_connect()
    # 使用cursor()方法创建光标
    cur = conn.cursor()
    # 如果表已经存在，使用execute() 删除表
    cur.execute("drop table if EXISTS " + tb_Name)
    # sql语句
    sql1 = "create table " + tb_Name + var.sql_create[table]
    try:
        # 执行sql语句并commit
        cur.execute(sql1)
        conn.commit()
        print("建表" + tb_Name + "成功")
    except Exception as err:
        # 出错时回滚（Rollback in case there is any error）
        print("建表" + tb_Name + "时出错 {}".format(str(err)))
        conn.rollback()
    # 断开连接
    conn.close()


'''
    建触发器函数: 
        在tbSuccess表上创建触发器，当有数据插入tbSuccess表时，更新tbProfit中的统计信息
'''
def trigger_create():
    # 连接数据库
    conn = var.pymysql_connect()
    # 使用cursor()方法创建光标
    cur = conn.cursor()
    # 如果已存在该触发器则删除
    cur.execute("drop trigger if EXISTS TR_Profit")
    # sql语句
    sql_tr = var.sql_trigger
    # print(sql_tr)
    try:
        # 执行sql语句并commit
        cur.execute(sql_tr)
        conn.commit()
        print("建触发器TR_Profit成功")
    except Exception as err:
        # 出错时回滚（Rollback in case there is any error）
        print("建触发器TR_Profit时出错 {}".format(str(err)))
        conn.rollback()
    # 断开连接
    conn.close()


def table_insert_df(table, df):
    # 索引为table
    table = table - 1
    # 表名
    tb_Name = var.table_Name[table]
    # 将导入的nan转换为None,nan不能在MySQL中使用
    df = df.where(df.notnull(), None)

    # # 特判转换为标准datetime格式
    # if table == 1 or table == 2:
    #     df['起始时间'] = pd.to_datetime(df['起始时间'])

    # 连接数据库
    conn = var.pymysql_connect()
    # 使用cursor()方法创建光标
    cur = conn.cursor()

    # sql语句
    sql_ins = var.sql_insert[table]

    # 导入数据
    # args是一个包含多个元组的列表
    args = df.values.tolist()
    for i in range(len(args)):
        args[i] = tuple(args[i])
    # print(args)
    try:
        cur.executemany(sql_ins, args)
        print("执行MySQL插入语句成功")
    except Exception as err:
        print("执行MySQL: %s 时出错: \n%s" % (sql_ins, err))
    finally:
        cur.close()
        conn.commit()
        conn.close()
        # # 若向tbPRB插入数据，则需要同时生成tbPRBNEW中的数据
        # if table == 2:
        #     print("若向tbPRB插入数据，则需要同时生成tbPRBNEW中的数据")
        #     data_bulkinsert_prbnew()


def table_insert_tuple(table, tp):
    # 索引为table
    table = table - 1
    # 表名
    tb_Name = var.table_Name[table]

    # 连接数据库
    conn = var.pymysql_connect()
    # 使用cursor()方法创建光标
    cur = conn.cursor()

    # sql语句
    sql_ins = var.sql_insert[table]

    # 导入数据
    try:
        cur.execute(sql_ins, tp)
        print("执行MySQL插入语句成功")
    except Exception as err:
        print("执行MySQL: %s 时出错: \n%s" % (sql_ins, err))
    finally:
        cur.close()
        conn.commit()
        conn.close()
        # # 若向tbPRB插入数据，则需要同时生成tbPRBNEW中的数据
        # if table == 2:
        #     print("若向tbPRB插入数据，则需要同时生成tbPRBNEW中的数据")
        #     data_bulkinsert_prbnew()


'''
    建表函数:table_update
    table:int   数据表，取值1-5分别表示 tbUser、tbRequest、tbResponse、tbSuccess、tbProfit;
    arg_list:list 参数列表，arg_list[0]为对应表格的唯一标识，之后为允许修改的全部参数
'''


def table_update(table, arg_list):
    # 索引为table
    table = table - 1
    # 表名
    tb_Name = var.table_Name[table]

    # 连接数据库
    conn = var.pymysql_connect()
    # 使用cursor()方法创建光标
    cur = conn.cursor()

    # sql语句
    sql_upt = f'UPDATE {tb_Name} '
    if tb_Name == 'tbUser':
        arg = f'SET u_pwd=\'{arg_list[1]}\',p_num=\'{arg_list[2]}\',u_idct=\'{arg_list[3]}\' ' \
              f'WHERE u_id=\'{arg_list[0]}\''
    elif tb_Name == 'tbRequest':
        arg = f'SET req_type={arg_list[1]},req_topic=\'{arg_list[2]}\',req_idct=\'{arg_list[3]}\',req_nop={arg_list[4]},end_time=\'{arg_list[5]}\' ' \
              f'WHERE req_id=\'{arg_list[0]}\''
    elif tb_Name == 'tbResponse':
        arg = f'SET rsp_idct=\'{arg_list[1]}\',m_time=NULL ' \
              f'WHERE rsp_id=\'{arg_list[0]}\''
    elif tb_Name == 'tbSuccess':
        return False
    elif tb_Name == 'tbProfit':
        return False

    sql_upt += arg
    try:
        cur.execute(sql_upt)
        print("执行MySQL更新语句成功")
        res = True
    except Exception as err:
        print("执行MySQL: %s 时出错: \n%s" % (sql_upt, err))
        res = False
    finally:
        cur.close()
        conn.commit()
        conn.close()
        return res


"""
    统计表格中行数
"""
def table_count(table):
    # 索引为table
    table = table - 1
    # 表名
    tb_Name = var.table_Name[table]
    # 连接数据库
    conn = var.pymysql_connect()
    # 使用cursor()方法创建光标
    cur = conn.cursor()
    sql = f'SELECT COUNT(*) FROM {tb_Name}'
    try:
        cur.execute(sql)
        tup = cur.fetchone()
        num = tup[0]
        print("执行MySQL计数语句成功")
    except Exception as err:
        print("执行MySQL: %s 时出错: \n%s" % (sql, err))
    finally:
        cur.close()
        conn.commit()
        conn.close()
        return num


"""
    创建一个Sequence表
"""
def sequence_create():
    # 连接数据库
    conn = var.pymysql_connect()
    # 使用cursor()方法创建光标
    cur = conn.cursor()
    sql = """
        CREATE TABLE tbsequence (
            tablename VARCHAR(30) NOT NULL,
            nextid bigint(20) NOT NULL,
            PRIMARY KEY(tablename)
        )
    """
    try:
        cur.execute(sql)
        print("创建tbsequence表成功")
    except Exception as err:
        print("执行MySQL: %s 时出错: \n%s" % (sql, err))
    finally:
        cur.close()
        conn.commit()
        conn.close()


if __name__ == '__main__':
    # sequence_create()
    #
    # for i in range(1, 6):
        # table_create(i)
    # table_create(4)
    # table_create(6)
    # table_create(5)
    # trigger_create()
    # now = datetime.datetime.now()
    # now = now.strftime("%Y-%m-%d %H:%M:%S")
    # pwd = 'admin'
    # admin_info = ('UR001','admin', hashlib.sha256(pwd.encode('utf-8')).hexdigest(), 0, '管理员', 0, '11000000000000000', '17100010001', 0, '系统管理员', '北京市', '001', now, now)
    # table_insert_tuple(1, admin_info)
    # table_insert_tuple(1, ('UR001', 'admin', 'admin', 0, '张三', 0, '110693184506080045', '18610750900', 0, '管理员用户，测试用', '北京', '测试社区', now, now))
    # table_update(1, ('u001', 'admin123', '16630731691'))
    # table_update(1, ('u001', 'admin', '18610750900'))
    print(table_count(1))
