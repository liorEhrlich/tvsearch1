import os
from bottle import (get, post, redirect, request, route, run, static_file,
                    template,error,response)
import utils
import json
from os import listdir
from os.path import isfile, join
import ast

# template routes

# Static Routes

@route('/browse/ratingSorted')
def index():
    shows_list = utils.getListDictionary()
    shows_list = sorted(shows_list, key=lambda k: k['rating']["average"])
    sectionTemplate = "./templates/browse.tpl"
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate, sectionData=shows_list)

@route('/browse/nameSorted')
def index():
    shows_list = utils.getListDictionary()
    shows_list = sorted(shows_list, key=lambda k: k['name'])
    sectionTemplate = "./templates/browse.tpl"
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate, sectionData=shows_list)


@route('/browse')
def index():
    shows_dict = utils.getListDictionary()
    sectionTemplate = "./templates/browse.tpl"
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate, sectionData =shows_dict)

@route("/search")
def search():
    sectionTemplate = "./templates/search.tpl"
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate,
                    sectionData={})

@post("/search")
def search():
    form_query = request.forms.get("q")
    shows_dict = utils.getListDictionary()
    result_episode_list = []
    for s in shows_dict:
        for ep in s['_embedded']['episodes']:
            if form_query in ep["name"]:
                result_episode_list.append({'showid': s['id'], 'episodeid': ep["id"], 'text': s["name"]+":"+ep["name"]})
            if ep["summary"] is not None:
                if form_query in ep["summary"]:
                    result_episode_list.append({'showid': s['id'], 'episodeid': ep["id"], 'text': s["name"]+":"+ep["name"]})
    sectionTemplate = "./templates/search_result.tpl"
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate,
                    sectionData={}, query=form_query, results=result_episode_list)


@get("/ajax/show/<number>")
def test(number):
    show_dict = json.loads(utils.getJsonFromFile(number))
    return template("./templates/show.tpl", version=utils.getVersion(), result=show_dict)


@get("/show/<number>")
def test(number):
    if utils.getJsonFromFile(number) == "{}":
        response.status = 404
        sectionTemplate = "./templates/404.tpl"
        return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate,
                        sectionData={})
    else:
        sectionTemplate = "./templates/show.tpl"
        show_dict = json.loads(utils.getJsonFromFile(number))
        return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate,
                    sectionData=show_dict)

@get("/ajax/show/<number>/episode/<epnumber>")
def test(number, epnumber):
    show_dict = json.loads(utils.getJsonFromFile(number))
    for ep in show_dict['_embedded']['episodes']:
        if ep["id"] == int(epnumber):
            episode = ep
    return template("./templates/episode.tpl", version=utils.getVersion(), result=episode)

@get("/show/<number>/episode/<epnumber>")
def test(number,epnumber):
    if utils.getJsonFromFile(number) == "{}":
        response.status = 404
        sectionTemplate = "./templates/404.tpl"
        return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate,
                        sectionData={})
    show_dict = json.loads(utils.getJsonFromFile(number))
    episode = ""
    for ep in show_dict['_embedded']['episodes']:
        if ep["id"] == int(epnumber):
            episode = ep
    if episode == "":
        response.status = 404
        sectionTemplate = "./templates/404.tpl"
        return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate,
                        sectionData={})
    sectionTemplate = "./templates/episode.tpl"
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate, sectionData=episode)


@get("/js/<filepath:re:.*\.js>")
def js(filepath):
    return static_file(filepath, root="./js")

@get("/css/<filepath:re:.*\.css>")
def css(filepath):
    return static_file(filepath, root="./css")

@get("/images/<filepath:re:.*\.(jpg|png|gif|ico|svg)>")
def img(filepath):
    return static_file(filepath, root="./images")

@error(404)
def error_404(error):
    return template("./templates/404.tpl", version=utils.getVersion(),sectionData={})


@route('/')
def index():
    sectionTemplate = "./templates/home.tpl"
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate, sectionData = {})

run(host='localhost', port=os.environ.get('PORT', 7000))
