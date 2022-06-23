import time
from datetime import date
from datetime import datetime
from sqlalchemy import null
from myweb import db
from myweb.models.User import User
from myweb.models.Game import Game
from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash, session, g
from myweb.views.userView import userView
from random import sample

gameView = Blueprint('game',__name__,url_prefix='/game')

@userView.before_app_request
def load_logged_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get_or_404(user_id)

def random():
    return sample(range(1,60),5)



def inicioGame(): 
        global inicio
        inicio = time.time()
        return inicio

def date():
        today = datetime.now()
        return today

def todayTime():
        fechaHora = datetime.now()
        hora = fechaHora.time().strftime("%H:%M:%S")
        return hora


@gameView.route('/guia', methods=['GET','POST'])
def guia():
    if request.method == 'POST':
        
        global rdnum
        rdnum = random()

        global starchron
        starchron= inicioGame()

        global intentos
        intentos = []

        return redirect(url_for('game.play'))
    else:
        return render_template('game/guia.html')


@gameView.route('/play', methods=['GET','POST'])
def play():
    message= ''
    listaNumeros=[]
    if request.method == 'POST':
        valor1= int(request.form['valor1'])
        valor2= int(request.form['valor2'])
        valor3= int(request.form['valor3'])
        valor4= int(request.form['valor4'])
        valor5= int(request.form['valor5'])
        listaNumeros.append(valor1)
        listaNumeros.append(valor2)
        listaNumeros.append(valor3)
        listaNumeros.append(valor4)
        listaNumeros.append(valor5)
        if rdnum != listaNumeros:
            intentos.append(listaNumeros)
            numIntentos = len(intentos)
            
            return render_template('game/play.html', message=message , lista=listaNumeros , rdnum=rdnum  , intentosList=intentos, numIntentos=numIntentos)
            
        else:
            user_id= session['user_id']
            numeroRandom=f"{rdnum[0]}/{rdnum[1]}/{rdnum[2]}/{rdnum[3]}/{rdnum[4]}/"
            numIntentos = len(intentos)
            finaltime = time.time()
            
            if finaltime-inicio >= 60:
                duracion = f"{int((finaltime-inicio)* 0.0166667)}'{int((((finaltime-inicio)* 0.0166667) - int((finaltime-inicio)* 0.0166667))*60)}" 
            elif finaltime-inicio < 60:
                duracion = f"{str(round(finaltime-inicio, 2))}'"

            fecha = date() 
            game= Game(user_id=user_id,intentos=numIntentos,random=numeroRandom,duracion=duracion,estado="finalizado",fecha=fecha)
            db.session.add(game)
            db.session.commit()

            return redirect(url_for('game.win'))
            
    return render_template('game/play.html', message=message , lista=listaNumeros)
    


@gameView.route('/win')
def win():
    return render_template('game/win.html')

@gameView.route("/ranking")
def ranking():
    return render_template('game/ranking.html')