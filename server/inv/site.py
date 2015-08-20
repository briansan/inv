from flask import Blueprint, redirect, url_for, render_template

site = Blueprint('site',__name__)

@site.route('/', methods=['GET'])
def home():
  return redirect(url_for('about'))

@site.route('/about', methods=['GET'])
def about():
  return render_template('about.html')

@site.route('/doc', methods=['GET'])
def doc():
  return render_template('doc.html')

@site.route('/support', methods=['GET'])
def support():
  return render_template('support.html')

