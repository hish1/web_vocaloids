import pandas


def get_concerts_email(conn, address):
    return pandas.read_sql(f'''
        select producer_name as Продюсер, 
            day_name as День_недели, 
            time_name as Время, 
            room_link as Ссылка,
            concert_id as id_Концерта,
            address
        from concerts_list
             join concert using (concert_id)
             join day using (day_id)
             join concert_time using (time_id)
             join program using (program_id)
             join producer using (producer_id)
             join email using (email_id)
        WHERE address = "{address}"
        ORDER BY 1
        ''', conn)


