import pandas as pd
from sqlalchemy import create_engine
from src.db import var
from src.db import tb
from scipy.stats import norm
from pandas.core.frame import DataFrame
from collections import defaultdict
import datetime


"""
    用户发布响应信息，返回发布结果
    参数顺序：arg_list(list)
    req_id,rsp_uid,rsp_idct
    返回值：
    成功返回rsp_id
    失败返回'RS0'
"""
def user_response_release(arg_list):
    # tbUser表
    table = 2
    # 表名
    table_name = var.table_Name[table]
    # 连接数据库
    conn = var.pymysql_connect()
    # 使用cursor()方法创建光标
    cur = conn.cursor()
    # sql语句
    sql_ins = var.sql_insert[table]
    # 判断请求信息是否存在
    sql_exist = f'SELECT * FROM tbResponse WHERE req_id=\'{arg_list[0]}\' AND rsp_uid=\'{arg_list[1]}\''
    num = cur.execute(sql_exist)
    if num != 0:
        return ['RS0', '对应的请求信息已存在']
    # 生成req_id
    sql1 = f'SELECT nextid FROM tbsequence WHERE tablename=\'{table_name}\''
    sql2 = f'UPDATE tbsequence SET nextid=nextid+1 WHERE tablename=\'{table_name}\''
    cur.execute(sql1)
    rsp_id = f'RS{cur.fetchone()[0]}'
    print(rsp_id)
    arg_list.insert(0, rsp_id)
    cur.execute(sql2)
    # 生成r_time和m_time
    now = datetime.datetime.now()
    now = now.strftime("%Y-%m-%d %H:%M:%S")
    arg_list.append(now)
    arg_list.append(now)
    arg_list.append(0)
    # 生成元组
    tp = tuple(arg_list)
    # 插入数据库
    try:
        cur.execute(sql_ins, tp)
        print("执行MySQL插入语句成功")
        res = rsp_id
        remark = "执行MySQL插入语句成功"
    except Exception as err:
        print("执行MySQL: %s 时出错: \n%s" % (sql_ins, err))
        res = 'RS0'
        remark = str(err)
    finally:
        cur.close()
        conn.commit()
        conn.close()
        return [res, remark]


"""
    用户查询自己发布的所有响应信息，返回查询结果
    参数顺序：
    rsp_uid
    返回值：
    成功返回[True, tup_list]
    tup_list = list[list[rsp_id,req_id,rsp_uid,rsp_idct,rsp_time,m_time,rsp_status]]
    失败返回[False, None]
"""
def user_response_info(rsp_uid):
    # 连接数据库
    conn = var.pymysql_connect()
    # 使用cursor()方法创建光标
    cur = conn.cursor()
    sql = f'SELECT b.rsp_id,b.req_id,b.rsp_uid,b.rsp_idct,b.rsp_time,b.rsp_status,' \
          f'a.req_cmty,a.req_uid,a.req_type,a.req_topic,a.req_idct,a.req_nop,a.end_time,a.req_time,a.req_status ' \
          f'FROM tbRequest a INNER JOIN tbResponse b ' \
          f'ON a.req_id=b.req_id ' \
          f'WHERE rsp_uid=\'{rsp_uid}\''
    res = cur.execute(sql)
    if res == 0:
        print(f"用户{rsp_uid}未发布响应信息！")
        return [False, None]
    else:
        tup_list = []
        for tup in cur.fetchall():
            tup_list.append(list(tup))
        print(tup_list)
        return [True, tup_list]


"""
    用户删除还未被接受的响应信息
    参数顺序：
    rsp_id
    返回值：
    成功返回True
    失败返回False
"""
def user_response_delete(rsp_id):
    # 连接数据库
    conn = var.pymysql_connect()
    # 使用cursor()方法创建光标
    cur = conn.cursor()
    # 判断响应信息是否存在
    sql_exist = f'SELECT * FROM tbResponse ' \
                f'WHERE rsp_id=\'{rsp_id}\''
    num = cur.execute(sql_exist)
    if num == 0:
        return False

    sql = f'UPDATE tbResponse ' \
          f'SET rsp_status=3 ' \
          f'WHERE rsp_id=\'{rsp_id}\''
    try:
        cur.execute(sql)
        print(f"更改响应{rsp_id}状态为取消响应状态！")
        res = True
    except Exception as err:
        print("执行MySQL: %s 时出错: \n%s" % (sql, err))
        res = False
    finally:
        cur.close()
        conn.commit()
        conn.close()
        return res


"""
    用户修改还未被接受的响应信息
    参数顺序：arg_list(list)
    rsp_id,rsp_idct
    返回值：
    成功返回True
    失败返回False
"""
def user_response_modify(arg_list):
    # 连接数据库
    conn = var.pymysql_connect()
    # 使用cursor()方法创建光标
    cur = conn.cursor()
    # 判断响应信息是否存在
    sql_exist = f'SELECT * FROM tbResponse ' \
                f'WHERE rsp_id=\'{arg_list[0]}\''
    num = cur.execute(sql_exist)
    if num == 0:
        return False

    sql = f'UPDATE tbResponse ' \
          f'SET rsp_idct=\'{arg_list[1]}\' ' \
          f'WHERE rsp_id=\'{arg_list[0]}\''
    try:
        cur.execute(sql)
        print("执行MySQL更新语句成功")
        res = True
    except Exception as err:
        print("执行MySQL: %s 时出错: \n%s" % (sql, err))
        res = False
    finally:
        cur.close()
        conn.commit()
        conn.close()
        return res


"""
    用户查看某一请求信息的所有帮忙信息，返回查询结果
    参数顺序：
    req_id
    返回值：
    成功返回[True, list[list[]]]
    失败返回[false, None]
"""
def user_request_response_info(req_id):
    # 连接数据库
    conn = var.pymysql_connect()
    # 使用cursor()方法创建光标
    cur = conn.cursor()
    sql = f'SELECT rsp_id,req_id,rsp_uid,rsp_idct,rsp_time,rsp_status ' \
          f'FROM tbResponse WHERE req_id=\'{req_id}\''
    res = cur.execute(sql)
    if res == 0:
        print(f"请求信息{req_id}不存在！")
        return [False, None]
    else:
        tup_list = []
        for tup in cur.fetchall():
            tup_list.append(list(tup))
        print(tup_list)
        return [True, tup_list]


"""
    用户查询自己所有已经被接受的请求响应信息，返回查询结果
    参数顺序：
    rsp_uid
    返回值：
    成功返回[True, tup_list]
    tup_list = lsit[list[rsp_id,req_id,rsp_uid,rsp_idct,rsp_time]]
    失败返回[False, None]
"""
def user_response_accepted(rsp_uid):
    # 连接数据库
    conn = var.pymysql_connect()
    # 使用cursor()方法创建光标
    cur = conn.cursor()
    sql = f'SELECT rsp_id,req_id,rsp_uid,rsp_idct,rsp_time ' \
          f'FROM tbResponse WHERE rsp_uid=\'{rsp_uid}\' AND rsp_status=1'
    res = cur.execute(sql)
    if res == 0:
        print(f"用户{rsp_uid}不存在被接受的响应信息！")
        return [False, None]
    else:
        tup_list = []
        for tup in cur.fetchall():
            tup_list.append(list(tup))
        return [True, tup_list]


"""
    判断请求是否已完成
    a > b: 请求未完成，可以继续接收请求
    a = b: 请求完成
    参数：
        req_id
    返回值：
        请求完成返回True
        请求未完成返回False
"""
def if_request_complete(req_id):
    # 连接数据库
    conn = var.pymysql_connect()
    # 使用cursor()方法创建光标
    cur = conn.cursor()
    # 获取帮忙请求人数
    sql1 = f'SELECT req_nop FROM tbRequest ' \
           f'WHERE req_id=\'{req_id}\''
    cur.execute(sql1)
    a = cur.fetchone()[0]
    print(f'{req_id}的请求人数: {a}')
    # 已接受的响应个数
    sql2 = f'SELECT COUNT(*) FROM tbResponse ' \
           f'WHERE req_id=\'{req_id}\' AND rsp_status=1'
    cur.execute(sql2)
    b = cur.fetchone()[0]
    print(f'{req_id}已经接受的的请求人数: {b}')
    if a > b:  # 请求未完成
        return False
    else:  # 请求已完成
        return True


"""
    获取 帮忙请求的请求人数 a 和 已接受的响应个数 b
    a > b: 可以继续接收请求
    a = b: 请求完成，更新请求的状态为已完成（0），更新剩余待接受（0）的响应为拒绝（2）
    参数：
        req_id
    返回值：
        请求完成返回True
        请求未完成返回False
"""
def user_status_update(req_id):
    # 连接数据库
    conn = var.pymysql_connect()
    # 使用cursor()方法创建光标
    cur = conn.cursor()
    # 获取帮忙请求人数
    sql1 = f'SELECT req_nop FROM tbRequest ' \
           f'WHERE req_id=\'{req_id}\''
    cur.execute(sql1)
    a = cur.fetchone()[0]
    print(f'{req_id}的请求人数: {a}')
    # 已接受的响应个数
    sql2 = f'SELECT COUNT(*) FROM tbResponse ' \
           f'WHERE req_id=\'{req_id}\' AND rsp_status=1'
    cur.execute(sql2)
    b = cur.fetchone()[0]
    print(f'{req_id}已经接受的的请求人数: {b}')
    if a > b:  # 请求未完成
        return False
    else:  # 请求已完成
        # 更新请求的状态为已完成（0）
        sql3 = f'UPDATE tbRequest SET req_status=0 WHERE req_id=\'{req_id}\''
        sql4 = f'UPDATE tbResponse SET rsp_status=2 WHERE req_id=\'{req_id}\' AND rsp_status=0'
        try:
            cur.execute(sql3)
            print(f"请求信息{req_id}状态修改为已完成")
            cur.execute(sql4)
            print(f"与请求信息{req_id}相关的未接受响应状态修改为拒绝")
        except Exception as err:
            print("执行MySQL: %s 时出错: \n%s" % err)
        finally:
            cur.close()
            conn.commit()
            conn.close()
            return True


"""
    用户处理响应信息，返回处理结果
    注意，处理响应信息的情况：
        1.拒绝，被拒绝的响应信息状态修改
        2.同意，帮忙请求信息和相应信息对应状态修改，修改帮忙成功明细表
    参数顺序：arg_list(list)
    req_id,req_uid,rsp_id,rsp_uid,option
    返回值：
    成功返回[True, remark]
    失败返回[False, remark]
"""
def user_opt_response(arg_list):
    # 提取参数
    req_id, req_uid, rsp_id, rsp_uid, option = arg_list
    # 连接数据库
    conn = var.pymysql_connect()
    # 使用cursor()方法创建光标
    cur = conn.cursor()
    # 获取当前时间
    now = datetime.datetime.now()
    now = now.strftime("%Y-%m-%d %H:%M:%S")
    # 判断请求id和响应id是否对应
    sql = f'SELECT * FROM tbResponse ' \
          f'WHERE req_id=\'{req_id}\' AND rsp_id=\'{rsp_id}\''
    num = cur.execute(sql)
    print("num: ", num)
    if num == 0:
        return [False, '请求ID和响应ID不对应！']
    # 判断人数是否达上限
    if if_request_complete(req_id):  # 已完成，人数达上限
        return [False, '响应人数已达上限！']

    # 判断option
    if option:  # 接收响应
        sql1 = f'UPDATE tbResponse SET rsp_status=1 WHERE rsp_id=\'{rsp_id}\''
        sql2 = f'INSERT INTO tbSuccess(req_id,req_uid,rsp_id,rsp_uid,agc_time) ' \
               f'VALUES (%s,%s,%s,%s,%s)'
        try:
            cur.execute(sql1)
            print(f"被接受的响应信息{rsp_id}状态修改")
            cur.execute(sql2, (req_id, req_uid, rsp_id, rsp_uid, now))
            print(f"帮忙成功表中添加记录")
            res = [True, "已接受该响应"]
        except Exception as err:
            print("执行MySQL语句时出错: \n%s" % err)
            res = [False, "已完成对该响应的处理"]
        finally:
            cur.close()
            conn.commit()
            conn.close()
        # 被接受的相应信息增加，更新状态信息
        print(f"请求信息{req_id}已完成:", user_status_update(req_id))
    else:  # 拒绝响应
        sql = f'UPDATE tbResponse SET rsp_status=2 WHERE rsp_id=\'{rsp_id}\''
        try:
            cur.execute(sql)
            print(f"被拒绝的响应信息{rsp_id}状态修改")
            res = [True, "已拒绝该响应"]
        except Exception as err:
            print("执行MySQL: %s 时出错: \n%s" % (sql, err))
            res = [False, "已完成对该响应的处理"]
        finally:
            cur.close()
            conn.commit()
            conn.close()
    return res


if __name__ == '__main__':
    print("response")
    # user_response_release(['RQ103', 'UR100', '会舞蹈才艺'])
    # user_response_release(['RQ101', 'UR100', '上班路线相同'])
    # user_response_release(['RQ101', 'UR102', '上班路线相同'])
    # print(user_response_info('UR100'))
    # user_response_delete('RS100')
    # user_response_modify(['RS101', '上班路线相同,有搭车意向'])
    # print(user_request_response_info('RQ101'))
    # print(user_response_accepted('UR100'))
    # user_opt_response(['RQ101', 'UR101', 'RS102', 'UR102', False])
    # user_opt_response(['RQ101', 'UR101', 'RS102', 'UR102', True])
    # user_opt_response(['RQ101', 'UR101', 'RS101', 'UR100', True])
    # print(user_response_accepted('UR100'))
