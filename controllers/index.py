from app import app
from flask import render_template, request, session
from utils import get_db_connection
from models.index_model import get_producers, get_day, get_time, get_concert, get_concert_songs, get_filter_concert, buy_concert


@app.route('/', methods=['get', 'post'])
def search():
    conn = get_db_connection()
    df_producers = get_producers(conn)
    df_day = get_day(conn)
    df_time = get_time(conn)
    checked_list_producers = []
    checked_list_day = []
    checked_list_time = []
    df_filter_concert = get_concert(conn)
    df_songs_list = get_concert_songs(conn)
    pressed = False
    concert_id = -1

    if request.values.get('reset'):
        df_filter_concert = get_concert(conn)
        checked_list_producers = []
        checked_list_day = []
        checked_list_time = []
    else:
        if request.values.get('producers') or request.values.get('day') or request.values.get('time'):
            checked_list_producers = request.form.getlist('producers')
            checked_list_day = request.form.getlist('day')
            checked_list_time = request.form.getlist('time')
            df_filter_concert = get_filter_concert(conn, checked_list_producers, checked_list_day, checked_list_time)

        if request.values.get('concert'):
            concert_id = request.values.get('concert')
            pressed = True

        if request.values.get('cancel'):
            pressed = False
        if request.values.get('bought'):
            pressed = False
            buy_concert(conn, int(request.values.get('bought')), request.values.get('email'))
            df_filter_concert = get_concert(conn)

    html = render_template(
        'index.html',
        producers_box=df_producers,
        day_box=df_day,
        time_box=df_time,
        filter_box=df_filter_concert,
        checked_list_producers=checked_list_producers,
        checked_list_day=checked_list_day,
        checked_list_time=checked_list_time,
        df_songs_list=df_songs_list,
        pressed = pressed,
        concert_id=concert_id,
        str=str,
        len=len
    )
    return html
