import functools

from flask import (
   Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('selections', __name__, url_prefix='/selections')


def login_required(view):
   @functools.wraps(view)
   def wrapped_view(**kwargs):
      if g.user is None:
         return redirect(url_for('auth.login'))

      return view(**kwargs)

   return wrapped_view


@login_required
@bp.route('/like/name=<string:name>', methods=['GET', 'POST'])
def like(name):
   db = get_db()
   try:
      db.execute("INSERT INTO likedNames (name, username) VALUES (?, ?)", (name, g.user['username'],))
   except db.IntegrityError:
      error -= f"Could not add {name}"
   db.commit()
   return redirect(url_for('site.index'))

@login_required
@bp.route('/dislike/name=<string:name>', methods=['GET', 'POST'])
def dislike(name):
   db = get_db()
   try:
      db.execute("INSERT INTO dislikedNames (name, username) VALUES (?, ?)", (name, g.user['username'],))
      
   except db.IntegrityError:
      error -= f"Could not add {name}"
   db.commit()
   return redirect(url_for('site.index'))

@login_required
@bp.route('/trash/name=<string:name>', methods=['GET', 'POST'])
def trash(name):
   db = get_db()
   try:
      db.execute("INSERT INTO dislikedNames (name, username) VALUES (?, ?)", (name, g.user['username'],))
      db.execute("DELETE FROM likedNames WHERE name == ? AND username == ?", (name, g.user['username']))

   except db.IntegrityError:
      error -= f"Could not add {name}"
   db.commit()
   return redirect(url_for('selections.liked'))


@login_required
@bp.route('/liked', methods=['GET', 'POST'])
def liked():
   if g.user == None or g.user['username'] == None:
      return redirect(url_for('auth.login'))
   db = get_db()
   names = db.execute("SELECT N.name, S.sex, NT.note FROM Names AS N, likedNames AS L, sex AS S LEFT JOIN notes AS NT ON NT.username == L.username AND NT.name == N.name WHERE L.name == N.name AND L.name == S.name AND L.username == ?", (g.user['username'],)).fetchall()
   return render_template('selections/liked.html', names=names)

@login_required
@bp.route('/note', methods=['POST'])
def note():
    db = get_db()
    name = request.form['name_hidden']
    note = request.form['note_textbox']
    print('new note ', note, ' for ', name)
    db.execute("DELETE FROM notes WHERE name == ? AND username == ?",(name, g.user['username']))
    db.execute("INSERT INTO notes (name, username, note) VALUES (?,?,?)", (name, g.user['username'], note))
    db.commit()
    return redirect(url_for('selections.liked'))

@login_required
@bp.route('/vault_note', methods=['POST'])
def vault_note():
    db = get_db()
    name = request.form['name_hidden']
    note = request.form['note_textbox']
    print('new note ', note, ' for ', name)
    db.execute("DELETE FROM notes WHERE name == ? AND username == ?",(name, g.user['username']))
    db.execute("INSERT INTO notes (name, username, note) VALUES (?,?,?)", (name, g.user['username'], note))
    db.commit()
    return redirect(url_for('selections.vault'))


@login_required
@bp.route('/vault', methods=['GET', 'POST'])
def vault():
   if g.user == None or g.user['username'] == None:
      return redirect(url_for('auth.login'))
   db = get_db()
   partner = db.execute('SELECT username FROM familyMembers WHERE familyID == ? AND NOT username == ?', (g.family['familyID'], g.user['username'])).fetchone()
   
   if partner is None:
      return redirect(url_for('auth.account'))
   
   names = db.execute("SELECT N.name, S.sex, NT.note, NT2.note AS note2 FROM Names AS N, likedNames AS L, sex AS S LEFT JOIN notes AS NT ON NT.username == L.username AND NT.name == N.name  INNER JOIN likedNames AS L2 ON L2.name == N.name AND L2.username = ? LEFT JOIN notes AS NT2 ON NT2.name == N.name AND NT2.username == L2.username WHERE L.name == N.name AND L.name == S.name AND L.username == ?", (partner['username'], g.user['username'],)).fetchall()
   return render_template('selections/vault.html', names=names, partner=partner['username'])

