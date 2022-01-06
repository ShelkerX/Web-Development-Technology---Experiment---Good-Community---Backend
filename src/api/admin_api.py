from flask import Blueprint, request
from src.db.admin import *

admin = Blueprint("admin", __name__)



@admin.route("/api/admin/all_users", methods=["GET"])
def adminAllUsersInfo():
    res = admin_all_users()
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
        "info_arr": None if not res[0] else dict(zip(range(len(res[1])), [dict(zip(keys, i)) for i in res[1]])),
    }


@admin.route("/api/admin/request/user_info", methods=["GET"])
def requestUserInfo():
    arg = request.args.get("req_id")
    print(arg)
    res = admin_reqid_user_info(arg)
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


@admin.route("/api/admin/response/user_info", methods=["GET"])
def responseUserInfo():
    arg = request.args.get("rsp_id")
    print(arg)
    res = admin_rspid_user_info(arg)
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


@admin.route("/api/admin/fee", methods=["GET"])
def adminFee():
    start = request.args.get("start_time")
    end = request.args.get("end_time")
    res = admin_agency_fee(start, end)
    return {
        "agency_fee": res
    }


@admin.route("/api/admin/statistics", methods=["GET"])
def adminStatistics():
    start = request.args.get("start_time")
    end = request.args.get("end_time")
    print(type(start), start)
    print(type(end), end)
    res = admin_statistics_info(start, end)
    keys = [
        "the_month",
        "trx_num",
        "agc_fee",
    ]
    return {
        "result": res[0],
        "info_arr": None if not res[0] else dict(zip(range(len(res[1])), [dict(zip(keys, i)) for i in res[1]])),
    }



# @admin.route("/api/admin/requset_info", methods=["GET"])
# @admin.route("/api/admin/response_info", methods=["GET"])


