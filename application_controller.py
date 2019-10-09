import os

from flask import Flask, request, render_template
from flask_paginate import Pagination, get_page_parameter

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
    
    if request.method == "POST":
        # pageキーで表示上を切り替えてpaginationを表現する
        result = post_query()
        page = request.args.get(get_page_parameter(), type=int, default=1)
        res = result[(page - 1)*2: page*2]
        pagination = Pagination(page=page, total=len(result),  per_page=2, css_framework='bootstrap4')
        print("""-----------------------------
               ---max---\n{}
               ---res---\n{}
               ---arg---\n{}
               ---pag---\n{}
              """
              .format(len(result),
                      res,
                      request.args,
                      page))
        return render_template("index.html", result=result, pagination=pagination)

    # paginationでGETされたときに渡されたパラメータを再利用する
    import json
    result = []
    for i in request.args:
        for j in request.args.getlist("result"):
            print("{}->{}".format(type(j), j))
            j = j.replace("\'", "\"")
            result.append(json.loads(j)) # 文字列からjsonへ変換して操作する
    page = request.args.get(get_page_parameter(), type=int, default=1)
    res = result[(page - 1)*2: page*2]
    pagination = Pagination(page=page, total=len(result),  per_page=2, css_framework='bootstrap4')
    print("""-----------------------------
           ---max---\n{}
           ---res---\n{}
           ---arg---\n{}
           ---pag---\n{}
          """
          .format(len(result),
                  res,
                  request.args,
                  page))
    return render_template("index.html", result=result, pagination=pagination)

def post_query():
    result = [{"page":1, "param":"出力用パラメータ1"},
              {"page":1, "param":"出力用パラメータ2"},
              {"page":2, "param":"出力用パラメータ3"},
              {"page":2, "param":"出力用パラメータ4"}]
    return result
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=1025)