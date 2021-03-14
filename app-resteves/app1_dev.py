from flask import Flask, render_template, request, redirect, url_for
from fastai.data.all import *
from fastai.callback.core import *
from fastai.vision import *
import pathlib
from werkzeug.utils import secure_filename

# Definición de Función para cargar el modelo
def load_learner(fname, cpu=True, pickle_module=pickle):
    "Load a `Learner` object in `fname`, optionally putting it on the `cpu`"
    distrib_barrier()
    res = torch.load(fname, map_location='cpu' if cpu else None, pickle_module=pickle_module)
    if hasattr(res, 'to_fp32'): res = res.to_fp32()
    if cpu: res.dls.cpu()
    return res


def load_posix_learner():
    temp = pathlib.PosixPath #Solo cuando se corre en Windows
    pathlib.PosixPath = pathlib.WindowsPath #Solo cuando se corre en Windows
    learn = load_learner('model/export.pkl')
    return learn

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
UPLOAD_FOLDER = 'static'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/') #allow both GET and POST requests
def index():
    return render_template('images/submit.html')

#Writing api for inference using the loaded model
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        print("si llego aquí #1") #La mejor herramienta del mundo
        # check if the post request has the file part
        if 'file' not in request.files:
            print('No file part')
            return redirect(request.url)
        file = request.files['file']
        print("si llego aquí #2")
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file_path = os.path.join(app.config['UPLOAD_FOLDER']+"/"+filename)
            print(file_path)
            produccion = load_posix_learner()
            pred,pred_idx,probs = produccion.predict(file_path)
            texto = "Predición: " + str(pred) +"; " + " Probabilidad: " + str(probs[pred_idx])
            print(texto)
            #return redirect(url_for('uploaded_file',filename=filename))
    return render_template('images/submit.html',categoria =pred,
                           probabilidad=probs[pred_idx],
                           show_predictions_modal = True,
                           imagesource='../static/' + filename)

from flask import send_from_directory

@app.route('/static/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],filename)


if __name__ == "__main__":
    app.run(debug=True)



