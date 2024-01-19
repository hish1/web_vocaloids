from app import app
from flask import render_template, request, session
from utils import get_db_connection
from models.check_model import get_concerts_email


@app.route('/check', methods=['get', 'post'])
def check():
    conn = get_db_connection()
    address=''
    df_concerts=[]

    if request.values.get('email'):
        address = request.values.get('email')
        df_concerts = get_concerts_email(conn, address)


    html = render_template(
        'check.html',
        address=address,
        concerts_list=df_concerts,
        str=str,
        len=len
    )
    return html
