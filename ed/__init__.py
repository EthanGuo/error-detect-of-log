# -*- coding: utf-8 -*-

from app_crash import app_crash
from app_anr import app_anr
from app_wtf import app_wtf
from system_tombstone import system_tombstone
from flask import jsonify, request
import json


TAGS = {
        "system_app_crash": app_crash,
        "SYSTEM_TOMBSTONE": system_tombstone,
        "system_app_wtf":   app_wtf,
        "system_app_anr":   app_anr,
}


def api_detect(tag):
    if not tag in TAGS.keys():
        return jsonify(status=0, msg='tag not supported', features={})
    try:
        data = json.loads(request.data).get('logcat')
        if data:
            md5, features = TAGS[tag](data)
            if features:
                return jsonify(status=1, msg='feature detected', features=features, md5=md5)
            else:
                return jsonify(status=0, msg='failed to detect features', features={})
        else:
            return jsonify(status=0, msg='logcat field required', features={})
    except Exception:
        return jsonify(status=0, msg='failed to detect features', features={})


def setup_ed(app):
    app.add_url_rule('/api/ed/detect/<tag>', 'api_detect', api_detect, methods=['POST'])