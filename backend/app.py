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
            static_folder= os.getcwd())

app.config['UPLOAD_FOLDER'] = './Uploads'
os.makedirs(os.path.join(app.instance_path, 'Uploads'), exist_ok=True)


@app.route("/")
def state():
    return render_template('index.html')


@app.route("/ind/<file>/<k>", methods=['GET'])
def KNNSearchInd(file, k):
    # TODO
    k = int(k)
    if(k < 1):
        k = 1
    res = comparator.KNNSearchInd(file, k)
    return render_template('result.html', data = res, name = file)


@app.route("/<file>/<k>", methods=['GET'])
def KNNSearch(file, k):
    # TODO

    res = comparator.KNNSearch(file, int(k))
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
  f.save(os.path.join(app.instance_path, 'Uploads', secure_filename(f.filename)))
  # Si se quiere eliminar el archivo usar remove(UPLOADS_PATH + filename)

  return redirect(url_for('KNNSearchInd', file = filename, k = k))
  



if __name__ == '__main__':
    comparator = Comparator(13174)
    app.run(debug=True, port=5050)
    app.add_url_rule('/favicon.ico',
                redirect_to=url_for('static', filename='frontend/src/logoico.png'))