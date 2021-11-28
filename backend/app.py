from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    jsonify
)
app = Flask(__name__, template_folder='../frontend/',
            static_folder='../frontend/')


@app.route("/", methods=['GET'])
def KNNSearchInd():
    # TODO
    res = comparator.KNNSearchInd(file, K)
    return res


@app.route("/", methods=['GET'])
def KNNSearch():
    # TODO
    res = comparator.KNNSearch(file, K)
    return res


@app.route("/", methods=['GET'])
def rangeSearchInd():
    # TODO
    res = comparator.rangeSearchInd(file, radius)
    return res


@app.route("/", methods=['GET'])
def rangeSearch():
    # TODO
    res = comparator.rangeSearch(file, radius)
    return res


if __name__ == '__main__':
    comparator = Comparator(13174)
    app.run(debug=True, port=5050)
