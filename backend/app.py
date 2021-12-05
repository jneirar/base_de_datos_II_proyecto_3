from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    jsonify
)
from werkzeug.utils import secure_filename
import os
from Comparator import Comparator

app = Flask(__name__, template_folder='../frontend/html/',
            static_folder='../frontend/')

UPLOAD_FOLDER = './backend/UploadFotos'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route("/")
def state():
    return render_template('index.html')


@app.route("/ind/<file>/<k>", methods=['GET'])
def KNNSearchInd(file, k):
    # TODO
    res = comparator.KNNSearchInd(file, k)
    return res


@app.route("/<file>/<k>", methods=['GET'])
def KNNSearch(file, k):
    # TODO
    res = comparator.KNNSearch(file, k)
    return render_template('result.html', data = res)


@app.route("/ind/<file>/<radius>", methods=['GET'])
def rangeSearchInd(file, radius):
    # TODO
    res = comparator.rangeSearchInd(file, radius)
    return res


@app.route("/<file>/<radius>", methods=['GET'])
def rangeSearch(file, radius):
    # TODO
    res = comparator.rangeSearch(file, radius)
    return res

@app.route("/upload", methods=['POST'])
def uploader():
 if request.method == 'POST':
  # obtenemos el archivo del input "archivo"
  f = request.files['archivo']
  k = request.form['Kfotos']
  print(k)
  filename = secure_filename(f.filename)
  f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
  # Si se quiere eliminar el archivo usar remove(UPLOADS_PATH + filename)
  # Retornamos una respuesta satisfactoria
  return redirect(url_for('KNNSearch', file = filename, k = k))
  



if __name__ == '__main__':
    comparator = Comparator(13174)
    app.run(debug=True, port=5050)
