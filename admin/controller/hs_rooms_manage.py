# coding : utf-8
from flask import render_template,request,json,jsonify
from . import ad
import requests
from flask_paginate import Pagination
from admin.config import Conf
import hashlib


@ad.route("/hs_type_manage")
def hs_type_manage():
    page = request.args.get('page')
    if page == None:
        page = '1'
    try:
        response = requests.get(url=Conf.API_ADDRESS + "/api/v1.0/get_all_hs_type/" + page)
        response_data = json.loads(response.content)
        if response_data['code'] == 1:
            page = response_data['page']
            pages = response_data['pages']
            total = response_data['total']
            entities = response_data['message']

            pagination = Pagination(page=page, total=total, pages=pages)
            return render_template("hs_rooms/hs_type_manage.html", pagination=pagination, entities=entities)

    except Exception as e:
        return render_template("hs_rooms/hs_type_manage.html")

@ad.route("/houses_manage")
def houses_manage():
    page = request.args.get('page')
    if page == None:
        page = '1'
    try:
        response = requests.get(url=Conf.API_ADDRESS + "/api/v1.0/get_all_houses/" + page)
        response_data = json.loads(response.content)
        if response_data['code'] == 1:
            page = response_data['page']
            pages = response_data['pages']
            total = response_data['total']
            entities = response_data['message']

            pagination = Pagination(page=page, total=total, pages=pages)
            return render_template("hs_rooms/houses_manage.html", pagination=pagination, entities=entities)

    except Exception as e:
        return render_template("hs_rooms/houses_manage.html")

@ad.route("/change_status_by_hs_id",methods=["POST"])
def change_status_by_hs_id():
    hs_id = request.json.get("hs_id")
    if not hs_id:
        return jsonify({"code": 0, "message": "参数错误"})
    hs_status = request.json.get("hs_status")
    if not hs_status:
        return jsonify({"code": 0, "message": "参数错误"})
    data = json.dumps({"hs_status": hs_status})
    response = requests.put(Conf.API_ADDRESS + "/api/v1.0/modify_status_by_hs_id/" + str(hs_id),
                        data=data,
                        headers={"content-type": "application/json"})
    response_data = json.loads(response.content)
    # code = 0删除失败
    if response_data["code"] == 0:
        return jsonify(response_data)
    # code = 1 删除成功
    if response_data["code"] == 1:
        return jsonify({"code": 1, "message": "停业操作成功"})


@ad.route("/del_type_by_id",methods=["POST"])
def del_type_by_id():
    ty_id = request.json.get("ty_id")
    if not ty_id:
        return jsonify({"code": 0, "message": "参数错误"})
    response = requests.delete(Conf.API_ADDRESS + "/api/v1.0/ht_delete/" + str(ty_id),headers={"content-type": "application/json"})
    response_data = json.loads(response.content)
    # code = 0删除失败
    if response_data["code"] == 0:
        return jsonify(response_data)
    # code = 1 删除成功
    if response_data["code"] == 1:
        return jsonify({"code": 1, "message": "删除成功"})
    return jsonify({"code": 0, "message": "删除失败"})

@ad.route("/insert_hs_type",methods = ["POST"])
def insert_hs_type():
    ty_name = request.json.get("ty_name")
    if not ty_name:
        return jsonify({"code":0,"message":"参数错误"})
    ty_valume = request.json.get("ty_valume")
    if not ty_valume:
        return jsonify({"code": 0, "message": "参数错误"})

    data=json.dumps({
        "ty_name":ty_name,
        "ty_valume":ty_valume,
    })
    # data = json.dumps({"user_account": user_account, "user_password": user_password_hash})
    response_data = requests.post(url=Conf.API_ADDRESS+"/api/v1.0/ht_insert", data = data, headers={"content-type": "application/json"})
    result_data = json.loads(response_data.content)
    #code =1 注册成功
    if result_data['code'] == 1:
        return jsonify({"code": 1, "message": "删除成功"})
    #code = 0 注册失败
    if response_data['code'] == 0:
        return jsonify(result_data)

@ad.route("/update_type_by_id",methods=['POST'])
def update_type_by_id():
    ty_id = request.json.get("ty_id")
    if not ty_id:
        return jsonify({"code": 0, "message": "参数错误"})
    ty_name = request.json.get("ty_name")
    ty_valume = request.json.get("ty_valume")

    data = json.dumps({
                       "ty_name": ty_name,
                       "ty_valume": ty_valume,
                       })
    response = requests.put(Conf.API_ADDRESS+"/api/v1.0/ht_update/"+str(ty_id),
                            data=data,
                            headers={"content-type": "application/json"})
    response_data = json.loads(response.content)
    # code = 0编辑失败
    if response_data["code"] == 0:
        return jsonify(response_data)

    # code = 1 编辑成功
    if response_data["code"] == 1:
        return jsonify({"code": 1, "message": "success"})