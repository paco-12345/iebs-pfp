import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

#from flaskr.db import get_db

bp = Blueprint('images', __name__, url_prefix='/images')



@bp.route('/submit', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        # username = request.form['username']
        # password = request.form['password']
        # db = get_db()
        # error = None

        # if not username:
        #     error = 'Username is required.'
        # elif not password:
        #     error = 'Password is required.'
        # elif db.execute(
        #     'SELECT id FROM user WHERE username = ?', (username,)
        # ).fetchone() is not None:
        #     error = 'User {} is already registered.'.format(username)

        # if error is None:
        #     db.execute(
        #         'INSERT INTO user (username, password) VALUES (?, ?)',
        #         (username, generate_password_hash(password))
        #     )
        #     db.commit()
        #     return redirect(url_for('auth.login'))

        # flash(error)
        pass

    return render_template('images/submit.html')