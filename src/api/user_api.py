from flask import Blueprint, request
from src.db.user import *

user = Blueprint("user", __name__)


@user.route("/api/user/register", methods=["POST"])
def register():
    print(request.json)  # dict
    body = request.json
    arg_list = list(body.values())
    res = user_register(arg_list)
    return {
        "result": False if res[0] == 'UR0' else True,
        "u_id": res[0],
        "remark": res[1],
    }


@user.route("/api/user/login", methods=["POST"])
def login():
    body = request.json
    arg_list = list(body.values())
    print(arg_list)
    res = user_login(arg_list)
    return {
        "result": res[0],
        "u_id": res[1],
        "u_type": res[2],
    }


@user.route("/api/user/info", methods=["GET"])
def userPerInfo():
    arg = request.args.get("u_id")
    # print(request.args)
    print(arg)
    res = user_info(arg)
    keys = [
        "u_name",
        "u_type",
        "r_name",
        "c_type",
        "c_num",
        "p_num",
        "u_level",
        "u_idct",
        "r_city",
        "r_cmty",
        "r_time",
        "m_time",
    ]
    return {
        "result": False if not res[0] else True,
        "info_obj": None if not res[0] else dict(zip(keys, res[1])),
    }


@user.route("/api/user/modify", methods=["POST"])
def userPerInfoModify():
    body = request.json
    print(body)
    arg_list = list(body.values())
    print(arg_list)
    return {
        'result': True if user_info_modify(arg_list) else False
    }