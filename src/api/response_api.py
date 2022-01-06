from flask import Blueprint, request
from src.db.response import *

rsp = Blueprint("rsp", __name__)


@rsp.route("/api/user/request/response_info", methods=["GET"])
def requestRspInfo():
    arg = request.args.get("req_id")
    print(arg)
    res = user_request_response_info(arg)
    keys = [
        "rsp_id",
        "req_id",
        "rsp_uid",
        "rsp_idct",
        "rsp_time",
        "rsp_status",
    ]
    return {
        "result": False if not res[0] else True,
        "info_arr": None if not res[0] else dict(zip(range(len(res[1])), [dict(zip(keys, i)) for i in res[1]])),
    }


@rsp.route("/api/user/request/opt_response", methods=["POST"])
def requestOptResponse():
    body = request.json
    arg_list = list(body.values())
    print(arg_list)
    res = user_opt_response(arg_list)
    return {
        "result": res[0],
        "remark": res[1],
    }


@rsp.route("/api/user/response/release", methods=["POST"])
def responseRelease():
    body = request.json
    arg_list = list(body.values())
    res = user_response_release(arg_list)
    return {
        "result": False if res[0] == 'RS0' else True,
        "remark": res[1],
        "rsp_id": res[0],
    }


@rsp.route("/api/user/response/response_info", methods=["GET"])
def responseInfo():
    arg = request.args.get("rsp_uid")
    print(arg)
    res = user_response_info(arg)
    keys = [
        "rsp_id",
        "req_id",
        "rsp_uid",
        "rsp_idct",
        "rsp_time",
        "rsp_status",
        "req_cmty",
        "req_uid",
        "req_type",
        "req_topic",
        "req_idct",
        "req_nop",
        "end_time",
        "req_time",
        "req_status",
    ]
    return {
        "result": False if not res[0] else True,
        "info_arr": None if not res[0] else dict(zip(range(len(res[1])), [dict(zip(keys, i)) for i in res[1]])),
    }


@rsp.route("/api/user/response/modify", methods=["POST"])
def responseModify():
    body = request.json
    arg_list = list(body.values())
    print(arg_list)
    res = user_response_modify(arg_list)
    return {
        "result": res,
    }


@rsp.route("/api/user/response/delete", methods=["POST"])
def responseDelete():
    body = request.json
    arg = body.get("rsp_id")
    print(arg)
    res = user_response_delete(arg)
    return {
        "result": res,
    }



@rsp.route("/api/user/response/accepted", methods=["GET"])
def responseAccepted():
    arg = request.args.get("rsp_uid")
    print(arg)
    res = user_response_accepted(arg)
    keys = [
        "rsp_id",
        "req_id",
        "rsp_uid",
        "rsp_idct",
        "rsp_time"
    ]
    return {
        "result": False if not res[0] else True,
        "info_arr": None if not res[0] else dict(zip(range(len(res[1])), [dict(zip(keys, i)) for i in res[1]])),
    }
