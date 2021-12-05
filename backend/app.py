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

@app.route("/upload", methods=['POST'])
def uploader():
 if request.method == 'POST':
  # obtenemos el archivo del input "archivo"
  f = request.files['archivo']
  filename = secure_filename(f.filename)
  # Guardamos el archivo en el directorio "Archivos PDF"
  f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
  # Si se quiere eliminar el archivo usar remove(UPLOADS_PATH + filename)
  # Retornamos una respuesta satisfactoria
  return redirect(url_for('after_upload', file = filename))


if __name__ == '__main__':
    comparator = Comparator(13174)
    app.run(debug=True, port=5050)
