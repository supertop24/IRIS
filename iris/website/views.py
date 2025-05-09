from flask import Blueprint, render_template

views = Blueprint('views', '__name__')

@views.route('/')
def portalSelect():

   return render_template("portalSelect.html")

#For now, just comment out ^ if you want to see the navBase
@views.route('/navBase')
def navBase():
    return render_template("navBase.html")