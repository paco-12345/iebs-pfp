import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

#from flaskr.db import get_db

bp = Blueprint('images', __name__, url_prefix='/images')



@bp.route('/submit', methods=('GET', 'POST'))
def submit():
    if request.method == 'POST':
        error = None

        file = request.files['img_submitted']

        print(file.read)

        # check file size

        max_kb = 1000 # limit kilo bytes
        size_bytes = len(file.read())
        if size_bytes > max_kb*1000:
            error = "El archivo subido (" + str(int(size_bytes/1000)) + " kB) supera el límite (" + str(max_kb) + " kB)"
        if error is None:
            ###
            # Feed image to algorithm
            result = "Normal"
            probability = 0.95231546
            ###
            file.close()
            return render_template(
                'images/submit.html',
                show_predictions_modal=True,
                result = result,
                probability = str(round(100.0 * probability, 1))
                )

        else:
            flash(error)
            file.close()
            return render_template(
                'images/submit.html',
                show_predictions_modal=False
                )


    elif request.method == "GET":
        return render_template(
            'images/submit.html',
            show_predictions_modal=False
            )