import functools

from flask import (
   Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

def login_required(view):
   @functools.wraps(view)
   def wrapped_view(**kwargs):
      if g.user is None:
         return redirect(url_for('auth.login'))

      return view(**kwargs)

   return wrapped_view

@bp.route('/add_name', methods= ['POST', 'GET'])
def add_name():
   db = get_db()
   rj = request.json
   try:
      db.execute("INSERT INTO names (name) VALUES (?)",
         (rj.get("name"),
         ))
      db.execute("INSERT INTO sex (name, sex) VALUES (?,?)", (rj.get("name"), rj.get("sex"),))
      if not rj.get("lands") == None:
         for l in rj.get("lands"):
            db.execute("INSERT INTO origins (country, name) VALUES (?,?)", (l, rj.get("name"),))
   except db.IntegrityError:
      error -= f"Could not add {request.name}"
   db.commit()
   return render_template('auth/register.html')


@bp.route('/register', methods=('GET', 'POST'))
def register():
   if request.method == 'POST':
      username = request.form['username']
      password = request.form['password']
      db = get_db()
      error = None
      if not username:
         error = 'Username is required.'
      elif not password:
         error = 'Password is required.'
      if error is None:
         try:
            db.execute(
               "INSERT INTO users (username, password) VALUES (?, ?)",
               (username, generate_password_hash(password)),
            )
            db.commit()
         except db.IntegrityError:
               error = f"User {username} is already registered."
         else:
               return redirect(url_for("auth.login"))
      flash(error)
   return render_template('auth/register.html')

@bp.route('/register_family', methods=('GET', 'POST'))
@login_required
def register_family():
   if request.method == 'POST':
      username = request.form['family_code']
      password = request.form['password']
      db = get_db()
      error = None
      if not username:
         error = 'Family code is required.'
      elif not password:
         error = 'Password is required.'
      if error is None:
         try:
               un = session['user_id']
               db.execute(
                  "INSERT INTO families (familyID, password) VALUES (?, ?)",
                  (username, generate_password_hash(password)),
               )
               db.execute(
                  "INSERT INTO familyMembers(familyID, username) VALUES (?,?)",
                  (username, un)
               )
               db.execute(
                  "INSERT INTO preferences(familyID) VALUES (?)", (username,)
               )
               session['family_code'] = username
               session['family'] = username
               g.family = username
               db.commit()
         except db.IntegrityError:
               error = f"Family {username} is already registered."
         else:
               return redirect(url_for("auth.account"))
      flash(error)
   return render_template('auth/register_family.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
   if request.method == 'POST':
      username = request.form['username']
      password = request.form['password']
      db = get_db()
      error = None
      user = db.execute(
         'SELECT * FROM users WHERE username = ?', (username,)
      ).fetchone()

      if user is None:
         error = 'Incorrect username.'
      elif not check_password_hash(user['password'], password):
         error = 'Incorrect password.'
      print(user)
      if error is None:
         session.clear()
         session['user_id'] = user['username']
         fam = db.execute("SELECT familyID from familyMembers WHERE username = ?", (user['username'],)).fetchone()
         if not fam == None:
            g.family = fam
            session['family_code'] = g.family['familyID']
            partner = db.execute("SELECT username FROM familyMembers WHERE familyID == ? AND NOT username == ?", (g.family['familyID'], user['username']))
            if not partner == None:
               g.partner = partner
         return redirect(url_for('index'))

      flash(error)

   return render_template('auth/login.html')

@bp.route('/join_family', methods=('GET', 'POST'))
@login_required
def join_family():
   if request.method == 'POST':
      username = request.form['family_code']
      password = request.form['password']
      db = get_db()
      error = None
      user = db.execute(
         'SELECT * FROM families WHERE familyId = ?', (username,)
      ).fetchone()

      if user is None:
         error = 'Incorrect family code.'
      elif not check_password_hash(user['password'], password):
         error = 'Incorrect password.'

      if error is None:
         members = db.execute('SELECT COUNT(*) AS c FROM familyMembers WHERE familyID = ?', (username,)).fetchone()
         if members is not None and members['c'] < 2:
            session['family_code'] = username
            un = session['user_id']
            print(username, " ", un)
            fam = db.execute(
               'INSERT INTO familyMembers(familyId, username) VALUES (?, ?)', (username, un)
            )
            db.commit()
            return redirect(url_for('auth.account'))
         else:
            error = 'Family already has 2 users'
            m = db.execute('SELECT username FROM familyMembers WHERE familyID = ?', (username,)).fetchall()
            for memb in m:
               print(memb[0])

            

      flash(error)

   return render_template('auth/join_family.html')


@bp.route('/account', methods=('GET', 'POST'))
@login_required
def account():
   db = get_db()

   if g.family is None:
      session['family_code'] = None
      return render_template('auth/account.html')

   g.family = db.execute('SELECT * FROM preferences WHERE familyID = ?', (g.family['familyID'], )).fetchone()
   g.partner = db.execute('SELECT username FROM familyMembers WHERE familyID == ? AND NOT username == ?', (g.family['familyID'], g.user['username'])).fetchone()
   
   if request.method == 'POST':
      m = "on" if "pref_male" in request.form else "off"
      f = "on" if "pref_female" in request.form else "off"
      x = "on" if "pref_unisex" in request.form else "off"
      fam = db.execute(
         'UPDATE preferences SET male = ?, female = ?, unisex = ? WHERE familyID = ?', (m, f, x, g.family['familyID'])
      )
      db.commit()
      return redirect(url_for('auth.account'))
      
   return render_template('auth/account.html')

@bp.before_app_request
def load_logged_in_user():
   db = get_db()
   user_id = session.get('user_id')


   if user_id is None:
      g.user = None
   else:
      g.user = db.execute(
         'SELECT username FROM users WHERE username = ?', (user_id,)
      ).fetchone()

      if g.user is not None:
         g.family = db.execute(
            'SELECT familyID FROM familyMembers WHERE username = ?', (g.user['username'],)
         ).fetchone()
      else:
         g.family = None

@bp.route('/logout')
def logout():
   session.clear()
   return redirect(url_for('index'))

@bp.route('/leave', methods=['GET', 'POST'])
@login_required
def leave():
   db = get_db()
   db.execute("DELETE FROM familyMembers WHERE username = ?", (g.user['username'],))
   g.family = None
   session['family'] = None
   db.commit()
   return redirect(url_for('auth.account'))

@bp.route('/delete', methods=['GET', 'POST'])
@login_required
def delete():
   return redirect(url_for('auth.account'))