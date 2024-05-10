
from flask import Flask,redirect
from flask import render_template
from flask import request
from flask import session
import database as db
import authentication
import logging
import ordermanagement as om

app = Flask(__name__)

def login(oldpassword):
    temp_password = om.get_user(password)
    if (oldpassword==temp_password):
        render_template('finalchangepass.html')


    else:
        render_template('changepass.html')
            
