import os
os.environ["NLS_LANG"] = "UKRAINIAN_UKRAINE.CL8MSWIN1251"
import cx_Oracle

def rows_to_dict_list(in_cursor):
    rows = in_cursor.fetchall()
    #print(cur.description)
    columns = {}
    for i, col in enumerate(in_cursor.description):
        columns[i] = col[0]
    #print(columns)
    result = {}
    for i, row in enumerate(rows):
        result[i] = {}
        for l, data in enumerate(row):
            result[i][columns[l]] = data
    return result

class ora_data:
    connect = None
    def __init__(self):
        try:
            self.connect = cx_Oracle.connect('c##dobrijzmej', '******', 'ZMEJ')
        except cx_Oracle.DatabaseError as exception:
            await
            #client.send_message(message.channel, message.author.mention + 'Failed to connect to ZMEJ')
            print('Failed to connect to %s\n', 'ZMEJ')
            traceback.print_exc()
            # printException(exception)
            return
        print("Connect from class succesfuly")


    def find_system_by_name(self, in_system_name):
        sql = """ /* find_system_by_name */
        select   (select   count(s.id)
                  from     eddb_systems s
                  where    s.name_upper = upper(:name)) this_system,
                  (select   count(s.id)
                  from     eddb_systems s
                  where    CATSEARCH(s.name_upper, upper('*'||:name||'*'), null) > 0) like_system,
                  (select   listagg(s.name, ', ') within group (order by s.name)
                  from     eddb_systems s
                  where    CATSEARCH(s.name_upper, upper('*'||:name||'*'), null)>0
                           and rownum <= 10) like_system_list
        from     dual
        """
        cur = self.connect.cursor()
        cur.execute(sql, name=in_system_name)
        row = cur.fetchone()
        result = {"this_system": row[0], "like_systems":row[1], "like_systems_list":row[2]}
        return result

    def get_system_base_info(self, in_system_name):
        sql = """/* get_system_base_info */
            select   s.id,                   /* field 000 */
                     s.edsm_id,              /* field 001 */
                     s.name as system_name,  /* field 002 */
                     s.x,                    /* field 003 */
                     s.y,                    /* field 004 */
                     s.z,                    /* field 005 */
                     f.name faction_name,    /* field 006 */
                     f.is_player_faction     /* field 007 */
            from     eddb_systems s,
                     eddb_factions f
            where    s.name_upper=upper(:name)
                     and f.id(+)=s.controlling_min_fact_id
                   """
        cur = self.connect.cursor()
        cur.execute(sql, name=in_system_name)
        result = rows_to_dict_list(cur)
        #print(result)
        return result

    def get_system_main_bodies(self, in_system_id):
        """Возвращает все объекты системы, у которых нет parent_id"""
        sql = """/* get_system_base_info */
                    select  s.id
                           ,b.id body_id
                           ,b.name
                           ,b.distance_to_arrival
                           ,g.name_ua
                           ,b.id body_id
                           ,g.name as group_name
                           ,b.spectral_class
                           ,b.solar_radius
                           ,b.is_main_star
                    from   eddb_systems s,
                           eddb_bodies b,
                           eddb_groups g
                    where  s.id=:systemId
                           and b.system_id(+)=s.id
                           and b.parent_id is null
                           and g.id(+)=b.group_id
                    order by b.name
                   """
        cur = self.connect.cursor()
        cur.execute(sql, systemId=in_system_id)
        result = rows_to_dict_list(cur)
        #print(result)
        return result

    def get_system_groups_bodies(self, in_system_id):
        """Возвращает количество объектов системы"""
        sql = """/* get_system_groups_bodies */
                select   g.name_ua,
                         g.name,
                         g.id,
                         count(b.id) count_bodies
                from     eddb_systems s,
                         eddb_bodies b,
                         eddb_groups g
                where    s.id=:systemId
                         and b.system_id=s.id
                         and g.id=b.group_id
                group by g.name_ua, g.name, g.id
                order by g.id
                   """
        cur = self.connect.cursor()
        cur.execute(sql, systemId=in_system_id)
        result = rows_to_dict_list(cur)
        #print(result)
        return result

    def get_system_stations(self, in_system_id):
        """Возвращает количество станций системы"""
        sql = """/* get_system_stations */
                select   st.name,
                         st.type
                from     eddb_systems s,
                         eddb_stations st
                where    s.id=:systemId
                         and st.system_id=s.id
                order by st.name
                   """
        cur = self.connect.cursor()
        cur.execute(sql, systemId=in_system_id)
        result = rows_to_dict_list(cur)
        #print(result)
        return result


    def get_child_bodies(self, in_system_id, in_parent_id):
        """Возвращает количество дочерних объектов тела"""
        sql = """/* get_child_bodies */
                select   g.name group_name,
                         g.name_ua group_name_ua,
                         bt.id type_id,
                         bt.name type_name,
                         bt.name_ua type_name_ua,
                         b.name,
                         b.distance_to_arrival,
                         b.radius,
                         b.gravity,
                         b.is_landable,
                         b.ring_type_id,
                         b.spectral_class,
                         st.type_id station_type_id,
                         st.has_blackmarket,
                         st.has_market,
                         st.has_refuel,
                         st.has_repair,
                         st.has_rearm,
                         st.has_outfitting,
                         st.has_shipyard,
                         st.has_docking,
                         st.has_commodities
                from     eddb_systems s,
                         eddb_bodies b,
                         eddb_groups g,
                         eddb_bodies_types bt,
                         (select * from eddb_stations ss where ss.type_id in (13, 14, 15)) st
                where    s.id=:systemId
                         and b.system_id=s.id
                         and b.parent_id=:parentId
                         and g.id(+)=b.group_id
                         and bt.id(+)=b.type_id
                         and st.body_id(+)=b.id
                         --and nvl(st.type_id, -1) in (14, 15, -1)
                order by nvl(b.distance_to_arrival, 0), b.name
                   """
        cur = self.connect.cursor()
        cur.execute(sql, systemId=in_system_id, parentId=in_parent_id)
        result = rows_to_dict_list(cur)
        #print(result)
        return result

    def get_translate(self, in_word):
        """Возвращает количество дочерних объектов тела"""
        sql = """/* get_child_bodies */
                select   eddb_utils.get_translate(:inWord) translate
                from     dual
                   """
        cur = self.connect.cursor()
        cur.execute(sql, inWord=in_word)
        result = rows_to_dict_list(cur)
        #print(result)
        return result
