import pandas


def get_producers(conn):
    return pandas.read_sql('''
        select producer_id, 
        producer_name as Продюсер, 
        count(program_id) as Количество_продюсеров
        from producer natural join program
        group by producer_id
''', conn)


def get_day(conn):
    return pandas.read_sql('''
        select day_id, 
        day_name as День_Недели, 
        count(concert_id) as Количество_дней
        from day natural join concert
        group by day_id
    ''', conn)


def get_time(conn):
    return pandas.read_sql('''
        select time_id,
            time_name as Время,
            count(concert_id) as Количество_времени
        from concert_time natural join concert
        group by time_id
    ''', conn)


def get_concert(conn):
    return pandas.read_sql('''
        select producer_name as Продюсер,
            day_name as День_недели,
            time_name as Время,
            room_size as Осталось_билетов,
            concert_id as id_Концерта
        from concert
             join day using (day_id)
             join concert_time using (time_id)
             join program using (program_id)
             join producer using (producer_id)
    ''', conn)


def get_concert_songs(conn):
    return pandas.read_sql('''
        select song_name, 
            vocaloid, 
            concert_id as id_Концерта
        from concert 
            natural join program
            natural join songs_list 
            natural join song 
        group by concert_id
    ''', conn)


def get_filter_concert(conn, producer, day, time):
    if producer == []:
        producer = ', '.join([str(i) for i in range(1, 7)])
    else:
        producer = ', '.join(producer)
    if day == []:
        day = ', '.join([str(i) for i in range(1, 8)])
    else:
        day = ', '.join(day)
    if time == []:
        time = ', '.join([str(i) for i in range(1, 4)])
    else:
        time = ', '.join(time)

    sql = f'''
        select producer_name as Продюсер,
            day_name as День_недели,
            time_name as Время,
            room_size as Осталось_билетов,
            concert_id as id_Концерта
        from concert
             join day using (day_id)
             join concert_time using (time_id)
             join program using (program_id)
             join producer using (producer_id) 
        where producer_id in ({producer}) and day_id in ({day}) and time_id in ({time})
    '''
    return pandas.read_sql(sql, conn)


def get_count_email(conn, address):
    return pandas.read_sql(f'''
        select count(email_id)
        from concerts_list 
        natural join email
        where address = '{address}'
    ''', conn)


def get_email(conn, address):
    return pandas.read_sql(f'''
        select email_id
        from email
        where address = "{address}"
    ''', conn)

# для обработки данных о взятой книге
def buy_concert(conn, concert_id, address):
    cur = conn.cursor()
    sql = f'''update concert 
            set room_size=room_size-1 
            where concert_id={concert_id}
    '''
    cur.execute(sql)

    em = get_count_email(conn, address).values[0][0]
    if (em == 0):
        sql1 = f'''insert into email(address)
            values ("{address}")
        '''
        cur.execute(sql1)

    em = get_email(conn, address).values[0][0]
    sql2 = f'''insert into concerts_list(email_id, concert_id)
        values ({em}, {concert_id})
    '''
    cur.execute(sql2)

    conn.commit()

