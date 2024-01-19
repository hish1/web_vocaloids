from app import app
from flask import render_template, request, session
from utils import get_db_connection
from models.index_model import get_producer, get_day, get_time, get_concert, get_count_email, get_concert_songs, get_filter_concert, buy_concert


@app.route('/', methods=['get', 'post'])
def search():
    conn = get_db_connection()
    df_producer = get_producer(conn)
    df_day = get_day(conn)
    df_time = get_time(conn)
    checked_list_producer = []
    checked_list_day = []
    checked_list_time = []
    df_filter_concert = get_concert(conn)
    pressed = False
    concert_id = -1

    if request.values.get('producer') or request.values.get('day') or request.values.get('time'):
        checked_list_producer = request.form.getlist('producer')
        checked_list_day = request.form.getlist('day')
        checked_list_time = request.form.getlist('time')
        df_filter_concert = get_filter_concert(conn, checked_list_day, checked_list_producer, checked_list_time)

    if request.values.get('reset'):
        df_filter_concert = get_concert(conn)
        checked_list_producer = []
        checked_list_day = []
        checked_list_time = []

    if request.values.get('buy'):
        pressed = True

    if request.values.get('bought'):
        concert_id = int(request.values.get('bought'))
        email = get_count_email(conn, request.values.get('email'))
        buy_concert(conn, concert_id, email)

    html = render_template(
        'index.html',
        producer_box=df_producer,
        day_box=df_day,
        time_box=df_time,
        filter_box=df_filter_concert,
        checked_list_producers=checked_list_producer,
        checked_list_day=checked_list_day,
        checked_list_time=checked_list_time,
        pressed = pressed,
        str=str,
        len=len
    )
    return html
