from flask import Blueprint, request
from src.db.request import *

req = Blueprint("req", __name__)


@req.route("/api/user/request/release", methods=["POST"])
def requestRelease():
    print(request.json)  # dict
    body = request.json
    arg_list = list(body.values())
    print(arg_list)
    res = user_request_release(arg_list)
    return {
        "result": False if res[0] == "RQ0" else True,
        "req_id": res[0],
        "remark": res[1],
    }


@req.route("/api/user/request/info", methods=["GET"])
def requestInfo():
    arg = request.args.get("req_uid")
    print(arg)
    res = user_request_info(arg)
    keys = [
        "req_cmty",
        "req_id",
        "req_uid",
        "req_type",
        "req_topic",
        "req_idct",
        "req_nop",
        "end_time",
        "req_photo",
        "req_time",
        "m_time",
        "req_status",
    ]
    return {
        "result": False if not res[0] else True,
        "info_arr": None if not res[0] else dict(zip(range(len(res[1])), [dict(zip(keys, i)) for i in res[1]])),
    }


@req.route("/api/user/request/delete", methods=["POST"])
def requestDelete():
    arg = request.json.get("req_id")
    print(arg)
    res = user_request_delete(arg)
    return {
        "result": res
    }


@req.route("/api/user/request/modify", methods=["POST"])
def requestModify():
    body = request.json
    arg_list = list(body.values())
    print(arg_list)
    res = user_request_modify(arg_list)
    return {
        "result": res[0],
        "remark": res[1],
    }


@req.route("/api/user/response/request_info", methods=["GET"])
def requestCmtyInfo():
    arg = request.args.get("community")
    res = user_request_cmty_info(arg)
    keys = [
        "req_cmty",
        "req_id",
        "req_uid",
        "req_type",
        "req_topic",
        "req_idct",
        "req_nop",
        "end_time",
        "req_photo",
        "req_time",
        "m_time",
        "req_status"
    ]
    return {
        "result": False if not res[0] else True,
        "info_arr": None if not res[0] else dict(zip(range(len(res[1])), [dict(zip(keys, i)) for i in res[1]])),
    }


@req.route("/api/user/request/spec_info", methods=["GET"])
def requestSpecInfo():
    arg = request.args.get("req_id")
    res = user_request_spec_info(arg)
    keys = [
    "req_cmty",
     "req_id",
     "req_uid",
     "req_type",
     "req_topic",
     "req_idct",
     "req_nop",
     "end_time",
     "req_photo",
     "req_time",
     "m_time",
     "req_status"
    ]
    return {
        "result": False if not res[0] else True,
        "info_obj": None if not res[0] else dict(zip(keys, res[1])),
    }