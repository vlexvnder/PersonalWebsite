#defines the backend of the website
from flask import Blueprint, session, redirect, url_for, request, render_template, current_app
import morse.encode as e

morse = Blueprint("morse", __name__, 
    template_folder="templates", 
    static_folder="static", 
    static_url_path="/morse/static" 
)

comments=[] #sets a blank comments field





@morse.route('/login', methods=['GET', 'POST']) #defines the login page
def login():
    if request.method == 'POST': #when the user sumbits their username
        if request.form['username'].strip() == "": #if it is blank space, pass
            pass
        if len(request.form['username'])>25: #if the username is excessively long, pass
            pass
        else:
            session['username'] = request.form['username'] #else set the username (stored locally) to their input
            return redirect(url_for('morse.encodePage')) #and redirect to the main page
    return render_template("login.html") #if the input was impropper (raising a pass), refresh the login

@morse.route('/logout') #defines the logout sequence
def logout():
    session.pop('username', None) #deletes the locally saved session variables
    session.pop('decode',None)
    return redirect(url_for('morse.login')) #redirects to login


@morse.route('/', methods=['GET', 'POST']) #defines the main page
def encodePage():
     if request.method == "POST": #when the user submits something
        if len(comments)>40: #if there are more than 40 messages
            del comments[0] #delete the oldest one
        if request.form['submit']=='Encode': #if the user presses 'encode'
            if request.form["contents"].strip()=="":                                #
                session['decode']="Sorry, you need to type something first!"        #Ensures that the message is not empty or blank
            elif e.encode(request.form["contents"])=="":                            #
                session['decode']="Sorry, we don't support that."                   #
            else:
                comments.append(session['username']+": "+e.encode(request.form["contents"])) #otherwise translates to morse code and displays

        elif request.form['submit']=='Decode': #if the user presses 'decode'
            if request.form['submit'].strip()=="":                                      #
                session['decode']="Sorry, you need to type something first!"            #Ensures that the message is not empty or blank
            elif e.decode(request.form["contents"])=="":                                #
                session['decode']="Sorry, we don't support that."                       #
            else:
                session['decode']=str(request.form["contents"]+" means: "+e.decode(request.form["contents"])) #otherwise, decodes and returns the decoded sequence

        return redirect(url_for('morse.encodePage')) #redirects back to the same page, reloading messages
     if session.get('username') is None: # if there is no username
         return redirect(url_for('morse.login')) #redirect to login
     if session.get('decode') is None: #if there is no decoded material
         session['decode']="" #set decode to blank
     return render_template("MainPage.html", comments=comments, decodeText=session.get('decode')) #renders the main page

@morse.route('/comments', methods=['GET', 'POST']) #returns a list of comments which are displayed every second on the main page using JQuery, giving users the latest messages without refreshing the page
def commentUpdate():
     return render_template("comments.html", comments=comments)
