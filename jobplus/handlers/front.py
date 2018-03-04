from flask import Blueprint,render_template

front=Blueprint('front',__name__)
@front.Route('/')
def dex():
    return render_template('index.html')

