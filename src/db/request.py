import pandas as pd
from sqlalchemy import create_engine
from src.db import var
from src.db import tb
from scipy.stats import norm
from pandas.core.frame import DataFrame
from collections import defaultdict
import datetime


"""
    用户发布请求信息，返回发布结果
    参数顺序：arg_list(list)
    req_cmty,req_uid,req_type,req_topic,req_idct,req_nop,end_time,req_photo
    返回值：
    成功返回[req_id, remark]
    失败返回['RQ0', remark]
"""
def user_request_release(arg_list):
    # tbUser表
    table = 1
    # 表名
    table_name = var.table_Name[table]
    # 连接数据库
    conn = var.pymysql_connect()
    # 使用cursor()方法创建光标
    cur = conn.cursor()
    # sql语句
    sql_ins = var.sql_insert[table]
    # 将参数转化为元组
    # 生成req_id
    sql1 = f'SELECT nextid FROM tbsequence WHERE tablename=\'{table_name}\''
    sql2 = f'UPDATE tbsequence SET nextid=nextid+1 WHERE tablename=\'{table_name}\''
    cur.execute(sql1)
    req_id = f'RQ{cur.fetchone()[0]}'
    print(req_id)
    arg_list.insert(1, req_id)
    # 格式化end_time
    end_time = arg_list[7]
    arg_list[7] = datetime.datetime.strptime(str(end_time), "%Y-%m-%d")
    print(arg_list[7])
    # 生成r_time和m_time
    now = datetime.datetime.now()
    now = now.strftime("%Y-%m-%d %H:%M:%S")
    arg_list.append(now)
    arg_list.append(now)
    arg_list.append(1)
    # 生成元组
    tp = tuple(arg_list)
    # 插入数据库
    try:
        cur.execute(sql_ins, tp)
        print("执行MySQL插入语句成功")
        res = req_id
        remark = "发布请求信息成功"
        cur.execute(sql2)
    except Exception as err:
        print("执行MySQL: %s 时出错: \n%s" % (sql_ins, err))
        res = 'RQ0'
        remark = str(err)
    finally:
        cur.close()
        conn.commit()
        conn.close()
        return [res, remark]


"""
    用户查询自己发布的所有请求信息，返回查询结果
    参数顺序：
    req_uid
    返回值：
    成功返回[True, tup_list]
    tup_list = list[list[req_cmty,req_id,req_uid,req_type,req_topic,req_idct,req_nop,end_time,req_photo,req_time,m_time,req_status]]
    失败返回[False, None]
"""
def user_request_info(req_uid):
    # 连接数据库
    conn = var.pymysql_connect()
    # 使用cursor()方法创建光标
    cur = conn.cursor()
    sql = f'SELECT * ' \
          f'FROM tbRequest WHERE req_uid=\'{req_uid}\''
    res = cur.execute(sql)
    if res == 0:
        print("用户未发布请求信息！")
        return [False, None]
    else:
        tup_list = []
        for tup in cur.fetchall():
            tup_list.append(list(tup))
        return [True, tup_list]


"""
    用户删除（已发布还没有响应者）的请求信息 (修改req_status)
    注意删除请求信息时对应的相应信息也要删除
    参数顺序：
    req_id
    返回值：
    成功返回True
    失败返回False
"""
def user_request_delete(req_id):
    # 连接数据库
    conn = var.pymysql_connect()
    # 使用cursor()方法创建光标
    cur = conn.cursor()
    # 先判断req_id是否存在
    sql1 = f'SELECT * FROM tbRequest ' \
           f'WHERE req_id=\'{req_id}\''
    if cur.execute(sql1) == 0:
        return False

    sql2 = f'UPDATE tbRequest ' \
           f'SET req_status=2 ' \
           f'WHERE req_id=\'{req_id}\''

    sql3 = f'UPDATE tbResponse ' \
           f'SET rsp_status=3 ' \
           f'WHERE req_id=\'{req_id}\''
    try:
        cur.execute(sql2)
        print(f"修改请求{req_id}状态为已取消")
        cur.execute(sql3)
        print(f"修改与请求{req_id}相关的响应信息为取消")
        res = True
    except Exception as err:
        print("执行MySQL: %s 时出错: \n%s" % (sql1, err))
        res = False
    finally:
        cur.close()
        conn.commit()
        conn.close()
        return res


"""
    用户修改（已发布还没响应者）的请求信息
    参数顺序：arg_list(list)
    req_id,req_type,req_topic,req_idct,req_nop,end_time,req_photo
    返回值：
    成功返回True
    失败返回False
"""
def user_request_modify(arg_list):
    # 连接数据库
    conn = var.pymysql_connect()
    # 使用cursor()方法创建光标
    cur = conn.cursor()
    sql = f'UPDATE tbRequest ' \
          f'SET req_type=\'{arg_list[1]}\',req_topic=\'{arg_list[2]}\',req_idct=\'{arg_list[3]}\',req_nop={arg_list[4]},end_time=\'{arg_list[5]}\',req_photo=\'{arg_list[6]}\' ' \
          f'WHERE req_id=\'{arg_list[0]}\''
    try:
        cur.execute(sql)
        print("执行MySQL更新语句成功")
        res = True
        remark = '执行MySQL更新语句成功'
    except Exception as err:
        print("执行MySQL: %s 时出错: \n%s" % (sql, err))
        res = False
        remark = str(err)
    finally:
        cur.close()
        conn.commit()
        conn.close()
        return [res, remark]


"""
    用户查看所属社区所有帮忙请求信息，返回查询结果
    参数顺序：
    cmty
    返回值：
    成功返回[True, tup_list]
    tup_list: list of list[req_cmty,req_id,req_uid,req_type,req_topic,req_idct,req_nop,end_time,req_photo,req_time,m_time,req_status]
    失败返回[False, None]
"""
def user_request_cmty_info(cmty):
    # 连接数据库
    conn = var.pymysql_connect()
    # 使用cursor()方法创建光标
    cur = conn.cursor()
    sql = f'SELECT * ' \
          f'FROM tbRequest WHERE req_cmty=\'{cmty}\''
    res = cur.execute(sql)
    if res == 0:
        print("该社区未发布请求信息！")
        return [False, None]
    else:
        tup_list = []
        for tup in cur.fetchall():
            tup_list.append(list(tup))
        return [True, tup_list]


"""
    用户查看某一帮忙请求具体信息，返回查询结果
    参数顺序：
    req_id
    返回值：
    成功返回[True, list(tup)]
    list[req_cmty,req_id,req_uid,req_type,req_topic,req_idct,req_nop,end_time,req_photo,req_time,m_time,req_status]
    失败返回[False, None]
"""
def user_request_spec_info(req_id):
    # 连接数据库
    conn = var.pymysql_connect()
    # 使用cursor()方法创建光标
    cur = conn.cursor()
    sql = f'SELECT * ' \
          f'FROM tbRequest WHERE req_id=\'{req_id}\''
    res = cur.execute(sql)
    if res == 0:
        print(f"请求信息{req_id}不存在！")
        return [False, None]
    else:
        tup = cur.fetchone()
        return [True, list(tup)]



if __name__ == '__main__':
    print("request")
    # user_request_release(['UR001', 'admin', '18610750900', '管理员用户', 'UR001', 'admin', '2022-1-20', '管理员用户'])
    # user_request_release(['光盘行动', 'UR101', '3', '线上演讲志愿者', '线上演讲志愿者，招募志愿者', 5, '2022-1-20', ''])
    # user_request_release(['关爱拉人', 'UR101', '3', '社区表演志愿者', '社区表演志愿者，招募志愿者', 12, '2022-1-23', ''])
    # print(user_request_info('UR101'))
    # print(user_request_delete('RQ101'))
    print(user_request_delete('一二三'))
    # user_request_modify(['RQ101', 2, '上下班搭车', '上下班搭车,找人', 3, '2021-2-01', ''])
    # print(user_request_cmty_info('垃圾回收'))
    # print(user_request_cmty_info('志愿者'))
    # print(user_request_spec_info('RQ101'))