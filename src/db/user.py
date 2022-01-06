import pandas as pd
from sqlalchemy import create_engine
# import var, tb
from src.db import var
from src.db import tb
from scipy.stats import norm
from pandas.core.frame import DataFrame
from collections import defaultdict
import datetime
import hashlib



"""
    用户注册时检查是否合理，返回检查结果
    参数顺序：
    u_name
    返回值：
    True:合理，False:不合理
"""
def user_register_check(u_name):
    # 连接数据库
    conn = var.pymysql_connect()
    # 使用cursor()方法创建光标
    cur = conn.cursor()
    # 如果用户名存在，返回1，否则返回0
    res = cur.execute(f"SELECT u_id,u_name FROM tbUser WHERE u_name=\'{u_name}\'")
    # 返回结果
    return not bool(res)


"""
    用户注册, 返回注册结果
    参数顺序: arg_list(list)
    u_name, u_pwd, u_type, r_name, c_type, c_num, p_num, u_level, u_idct, r_city, r_cmty
    返回值: string
    成功返回[u_id,remark],失败返回['UR0',remark]
"""
def user_register(arg_list):
    # 先做注册检查
    if not user_register_check(arg_list[0]):
        return ['UR0', '用户名已存在']
    # tbUser表
    table = 0
    # 表名
    table_name = var.table_Name[table]
    # 连接数据库
    conn = var.pymysql_connect()
    # 使用cursor()方法创建光标
    cur = conn.cursor()
    # sql语句
    sql_ins = var.sql_insert[table]
    # 密码SHA256加密
    arg_list[1] = hashlib.sha256(arg_list[1].encode('utf-8')).hexdigest()
    # 将参数转化为元组
    # 生成u_id
    sql1 = f'SELECT nextid FROM tbsequence WHERE tablename=\'{table_name}\''
    sql2 = f'UPDATE tbsequence SET nextid=nextid+1 WHERE tablename=\'{table_name}\''
    cur.execute(sql1)
    u_id = f'UR{cur.fetchone()[0]}'
    arg_list.insert(0, u_id)
    cur.execute(sql2)
    # 生成r_time和m_time
    now = datetime.datetime.now()
    now = now.strftime("%Y-%m-%d %H:%M:%S")
    arg_list.append(now)
    arg_list.append(now)
    # 生成元组
    tp = tuple(arg_list)
    # 插入数据库
    try:
        cur.execute(sql_ins, tp)
        print("执行MySQL插入语句成功")
        res = u_id
        remark = '注册成功'
    except Exception as err:
        print("执行MySQL: %s 时出错: \n%s" % (sql_ins, err))
        res = 'UR0'
        remark = str(err)
    finally:
        cur.close()
        conn.commit()
        conn.close()
        return [res, remark]

"""
    用户登录, 返回登录结果
    参数顺序: arg_list(list)
    u_name, u_pwd
    返回值: 
    成功返回list[True, u_id, u_type]
    失败返回list[False, None, None]
"""
def user_login(arg_list):
    # 提取参数
    u_name = arg_list[0]
    u_pwd = hashlib.sha256(arg_list[1].encode('utf-8')).hexdigest()
    # 连接数据库
    conn = var.pymysql_connect()
    # 使用cursor()方法创建光标
    cur = conn.cursor()
    sql = f'SELECT u_id,u_type FROM tbUser WHERE u_name=\'{u_name}\' AND u_pwd=\'{u_pwd}\''
    res = cur.execute(sql)
    if res == 0:
        print("用户名不存在或密码错误！")
        return [False, None, None]
    elif res == 1:
        tup = cur.fetchone()
        return [True] + list(tup)


"""
    用户查询基本信息, 返回查询结果
    参数顺序: u_id
    返回值: 
    成功返回list[True, list(tup)]
    list(tup) = u_name, u_type, r_name, c_type, c_num, p_num, u_level, u_idct, r_city, r_cmty, r_time, m_time]，
    失败返回lsit[false, None]
"""
def user_info(u_id):
    # 连接数据库
    conn = var.pymysql_connect()
    # 使用cursor()方法创建光标
    cur = conn.cursor()
    sql = f'SELECT u_name,u_type,r_name,c_type,c_num,p_num,u_level,u_idct,r_city,r_cmty,r_time,m_time ' \
          f'FROM tbUser WHERE u_id=\'{u_id}\''
    res = cur.execute(sql)
    if res == 0:
        print("用户标识不存在！")
        return [False, None]
    elif res == 1:
        tup = cur.fetchone()
        return [True, list(tup)]


"""
    用户查询基本信息, 返回查询结果
    参数顺序: arg_list(list)
    u_id,u_pwd,p_num,u_idct
    返回值: 
    成功返回True
    失败返回false
"""
def user_info_modify(arg_list):
    # 密码SHA256加密
    arg_list[1] = hashlib.sha256(arg_list[1].encode('utf-8')).hexdigest()
    return tb.table_update(1, arg_list)


if __name__ == '__main__':
    print('user')
    # print(user_register_check('user123'))
    # print(user_register(['user123', 'user123', 1, '李四', 0, '130984200008270016', '', 1, '', '河北', '志愿者']))
    # print(user_register(['user456', 'user456', 1, '王五', 0, '130984200008270048', '', 1, '', '东北', '志愿者']))
    # print(user_register(['user789', 'user789', 1, '孙六', 0, '130984200008270064', '', 1, '', '北京', '志愿者']))
    # login_res = user_login(['admin', 'admin'])
    # print(login_res)
    # print(user_info(login_res[0]))
    # user_info_modify(['u001', 'admin', '18610750900', '测试用，管理员用户'])
