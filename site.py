import functools

from flask import (
   Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db
from flaskr.auth import login_required

bp = Blueprint('site', __name__)

@login_required
@bp.route('/')
def index():
   if(g.user is None):
      return redirect(url_for('auth.login'))
   else:
      if(g.user['fam_id'] is None):
         return redirect(url_for('auth.account'))
      db = get_db()
      pref = db.execute(
         'SELECT male, female, unisex FROM family WHERE fam_id = ?', (g.user['fam_id'],)
      ).fetchone()
      print(pref)
      print(pref['male'], pref['female'], pref['unisex'])

      preferences = []
      
      p = tuple(preferences)
      command = "SELECT * FROM name WHERE sex IN ("
      if pref['male'] == 'on':
         command = command + str("\'M\'")
      if pref['female'] == 'on':
         if not command.endswith('('):
            command = command + str(", ")
         command = str(command) + "\'F\'"
      if pref['unisex'] == 'on':
         if not command.endswith('('):
            command = command + str(", ")
         command = str(command) + "\'X\'"
      
      command = command + ")"
      print(command)
      name = db.execute(
         command
      ).fetchone()

   return render_template('site/index.html', name=name)