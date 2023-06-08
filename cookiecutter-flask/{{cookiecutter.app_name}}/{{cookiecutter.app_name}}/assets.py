# -*- coding: utf-8 -*-
from flask_assets import Bundle, Environment

css = Bundle(
    "libs/bootstrap/dist/css/bootstrap.css",
    "libs/bootstrap-datetimepicker/bootstrap-datetimepicker.css",
    "libs/font-awesome4/css/font-awesome.css",
    "css/style.css",
    filters="cssmin",
    output="public/css/common.css"
)

js = Bundle(
    "libs/jQuery/dist/jquery.js",
    "libs/bootstrap/dist/js/bootstrap.js",
    "libs/bootstrap/dist/js/transition.js",
    "libs/bootstrap/dist/js/collapse.js",
    "libs/moment/moment.min.js",
    "libs/bootstrap-datetimepicker/bootstrap-datetimepicker.js",    
    "js/plugins.js",
    filters='jsmin',
    output="public/js/common.js"
)

assets = Environment()

assets.register("js_all", js)
assets.register("css_all", css)
