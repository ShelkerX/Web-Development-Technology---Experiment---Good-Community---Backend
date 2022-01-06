import pandas as pd
from sqlalchemy import create_engine
from src.db import var
from src.db import tb
from src.db import user
from scipy.stats import norm
from pandas.core.frame import DataFrame
from collections import defaultdict
import datetime


"""
    返回所有用户的基本信息
    返回值：
        成功返回list[True, list(tup)]
            list(tup): list of [u_name, u_type, r_name, c_type, c_num, p_num, u_level, u_idct, r_city, r_cmty, r_time, m_time]，
        失败返回lsit[false, None]
"""
def admin_all_users():
    # 连接数据库
    conn = var.pymysql_connect()
    # 使用cursor()方法创建光标
    cur = conn.cursor()
    sql = f'SELECT u_name, u_type, r_name, c_type, c_num, p_num, u_level, u_idct, r_city, r_cmty, r_time, m_time ' \
          f'FROM tbUser'
    res = cur.execute(sql)
    if res == 0:
        print("没有用户信息！")
        return [False, None]
    else:
        tup_list = []
        for tup in cur.fetchall():
            tup_list.append(list(tup))
        return [True, tup_list]

"""
    根据请求标识查询发起请求用户的基本信息
    参数顺序：
        req_id
    返回值：
        成功返回list[True, list(tup)]
            list(tup) = [u_name, u_type, r_name, c_type, c_num, p_num, u_level, u_idct, r_city, r_cmty, r_time, m_time]，
        失败返回lsit[false, None]
"""
def admin_reqid_user_info(req_id):
    # 连接数据库
    conn = var.pymysql_connect()
    # 使用cursor()方法创建光标
    cur = conn.cursor()
    # sql语句
    sql1 = f'SELECT req_uid FROM tbRequest WHERE req_id=\'{req_id}\''
    try:
        num = cur.execute(sql1)
        print("执行MySQL查询语句成功")
        if num == 0:
            print(f"req_id({req_id})不存在!")
            res = [False, None]
        else:
            u_id = cur.fetchone()[0]
            res = user.user_info(u_id)
    except Exception as err:
        print("执行MySQL: %s 时出错: \n%s" % (sql1, err))
        res = [False, None]
    finally:
        cur.close()
        conn.commit()
        conn.close()
        return res


"""
    根据响应标识查询帮忙用户的基本信息
    参数顺序：
        rsp_id
    返回值：
        成功返回list[True, list(tup)]
            list(tup) = [u_name, u_type, r_name, c_type, c_num, p_num, u_level, u_idct, r_city, r_cmty, r_time, m_time]，
        失败返回lsit[false, None]
"""
def admin_rspid_user_info(rsp_id):
    # 连接数据库
    conn = var.pymysql_connect()
    # 使用cursor()方法创建光标
    cur = conn.cursor()
    # sql语句
    sql1 = f'SELECT rsp_uid FROM tbResponse WHERE rsp_id=\'{rsp_id}\''
    try:
        num = cur.execute(sql1)
        print("执行MySQL查询语句成功")
        if num == 0:
            print(f"rsp_id({rsp_id})不存在!")
            res = [False, None]
        else:
            u_id = cur.fetchone()[0]
            res = user.user_info(u_id)
    except Exception as err:
        print("执行MySQL: %s 时出错: \n%s" % (sql1, err))
        res = [False, None]
    finally:
        cur.close()
        conn.commit()
        conn.close()
        return res


"""
    管理员查询已完成请求的中介费
    参数顺序：
        
    返回值：
        成功返回agency_fee
        失败返回False
"""
def admin_agency_fee(start, end):
    # 连接数据库
    conn = var.pymysql_connect()
    # 使用cursor()方法创建光标
    cur = conn.cursor()
    sql = f'SELECT COUNT(*) FROM tbSuccess WHERE ' \
          f'agc_time BETWEEN \'{start}\' AND \'{end}\''
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
        return num*4


"""
    管理员查询已完成请求的中介费月份统计数据
    参数顺序：
        start,end
    返回值：
        成功返回list[True, list(tup)]
            list(tup) = [the_month, trx_num, agc_fee]
        失败返回lsit[false, None]
"""
def admin_statistics_info(start, end):
    # 连接数据库
    conn = var.pymysql_connect()
    # 使用cursor()方法创建光标
    cur = conn.cursor()
    # 格式化start和end
    start = datetime.datetime.strptime(start, "%Y-%m-%d %H:%M:%S")
    end = datetime.datetime.strptime(end, "%Y-%m-%d %H:%M:%S")
    # print(type(start), start)
    # print(type(end), end)
    start_month = datetime.datetime.strftime(start, "%Y-%m")
    end_month = datetime.datetime.strftime(end, "%Y-%m")
    print(type(start_month), start_month)
    print(type(end_month), end_month)
    # sql语句
    sql1 = f'SELECT * FROM tbProfit ' \
           f'WHERE the_month BETWEEN \'{start_month}\' AND \'{end_month}\''
    num = cur.execute(sql1)
    print("执行MySQL查询语句成功")
    if num == 0:
        print(f"tbProfit中还没有收益信息")
        res = [False, None]
    else:
        tup_list = []
        for tup in cur.fetchall():
            tup_list.append(list(tup))
        print(tup_list)
        res = [True, tup_list]
    cur.close()
    conn.commit()
    conn.close()
    return res


if __name__ == '__main__':
    print("admin")
    # print(admin_reqid_user_info('RQ101'))
    # print(admin_rspid_user_info('RS101'))
    start_time = "2021-12-30"
    end_time = "2021-12-31"
    start = datetime.datetime.strptime(str(start_time), "%Y-%m-%d")
    print(start)
    end = datetime.datetime.strptime(str(end_time), "%Y-%m-%d")
    print(end)
    print(admin_agency_fee(start, end))
