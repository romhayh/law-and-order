from enum import unique
from faker import Faker
import pyodbc
import numpy as np
from random import choice


fake = Faker()
conn = pyodbc.connect('Driver={SQL Server Native Client 11.0};'
                      'Server=DESKTOP-NBQ4LO7;'
                      'Database=law and order;'
                      'Trusted_Connection=yes;')


def sqlexec(conn, query:str, print_:bool = False, return_ = False):
    cursor = conn.cursor()
    answer = cursor.execute(query).fetchall()
    if print_:
        for row in cursor:
            print(row)
    conn.commit()
    if return_:
        return answer




def genPeople(amount:int, conn):
    fake = Faker()
    genders = ('male', 'female')
    
    
    for i in range(amount):
        birth = str(fake.date_of_birth(minimum_age=30,maximum_age=80))
        gender = genders[fake.random_int(0,1)]
        
        
        # check if the name is valid:
        while 'trying':
            name = eval(f'fake.unique.name_{gender}()')
            cursor = sqlexec(conn,
                    f'''
                    select * from [people]
                    where [full name] = \'{name}\';
                    ''',
                    return_=True)
            if cursor != []:
                #! found a person that has the same name
                continue
            break
        
        cursor = sqlexec(conn,
                      '''
                        SELECT TOP 1 [city id] FROM [cities]
                        ORDER BY NEWID();''',
                        return_=True)
        cityid = cursor[0][0]

        cursor = conn.cursor()
        cursor.execute(f'''
                       insert into [people]([birthdate], [city id], [full name], [gender])
                       values(\'{birth}\', {cityid}, \'{name}\', \'{gender}\')
                       ''')
        cursor.commit()
        
        
        
def genFirm(amount:int, conn):
    fake = Faker()
    
    for i in range(amount):
        cursor = sqlexec(conn,
                      '''
                        SELECT TOP 1 [city id] FROM [cities]
                        ORDER BY NEWID();''',
                        return_=True)
        cityid = cursor[0][0]
        name = fake.unique.company()
        try:
            cursor = conn.cursor()
            cursor.execute(f'''
                        insert into [firms]([name], [city id])
                        values (\'{name}\', {cityid});
                        ''')
            cursor.commit()
        except:
            print('failed to insert')
        
    
    
def genLawyer(conn):
    AMOUNT_IN_FIRM = 10
    AMOUNT_OF_FIRMS = 100
    
    # create a rank distribution
    rankdist = np.zeros((91), dtype= np.uint8)
    for i in range(len(rankdist)):
        if i < 70:
            rankdist[i] = 1
        elif i < 82:
            rankdist[i] = 2
        elif i < 87:
            rankdist[i] = 3
        elif i < 90:
            rankdist[i] = 4
        elif i < 91:
            rankdist[i] = 5
    print(f'rankdist len = {len(rankdist)}' )
    print(rankdist)
    
    for firmid in range(62, AMOUNT_OF_FIRMS+1):
        #TODO step I
        # get the city of the firm
        cursor = sqlexec(conn,
                        f'''
                            SELECT [city id] from [firms] where [firm id] = {firmid}
                        ''',
                        return_=True)
        if cursor == []:
            continue
        cityid = cursor[0][0]
        
        isManaging = True   # make 1 mg partner for each firm
        if firmid <= 3:
            continue
        
        for i in range(AMOUNT_IN_FIRM):
            
            a = 0
            personid = 0
            while(not personid):
                #TODO step II
                # get a random person from that city
                a+=1
                cursor = sqlexec(conn,
                                f'''
                                    SELECT TOP 1 [person id] FROM [people]
                                    where [city id] = {cityid}
                                    ORDER BY NEWID();''',
                                    return_=True)
                personid = cursor[0][0]
                cursor = sqlexec(conn,
                                f'''
                                    SELECT [person id] from [lawyers]
                                    where [person id] = {personid};''',
                                    return_=True)
                isLawyer = (cursor != [])
                
                cursor = sqlexec(conn,
                                f'''
                                    SELECT [person id] from [judges]
                                    where [person id] = {personid};''',
                                    return_=True)
                isJudge = (cursor != [])
                cursor = sqlexec(conn,
                                f'''
                                    SELECT [person id] from [bar]
                                    where [person id] = {personid};''',
                                    return_=True)
                isListed = (cursor != [])
                if isLawyer or isListed or isJudge:
                    print(f'failed to put person: {a}, firm id = {firmid}')
                    personid = 0
                if a > 10:
                    break
                else:
                    break
            if a > 10:
                continue
                
            # generate bar listing:
            cursor = sqlexec(conn,
                            '''
                                SELECT TOP 1 [specialization id] FROM [specializations]
                                ORDER BY NEWID();''',
                                return_=True)
            spid = cursor[0][0] #specialization id
            cursor = conn.cursor()
            cursor.execute(f'''
                            insert into [bar]([person id], [specialization id])
                            values({personid}, {spid});
                            ''')
            cursor.commit()
            
            # generate lawyer:
            
            cursor = sqlexec(conn,
                            f'''
                            select [bar id] from [bar]
                            where [person id] = {personid};
                            ''',
                            return_=True)
            barid = cursor[0][0]
            
            # generate a rank:
            rankid = 0
            if isManaging:
                rankid = 5
                isManaging = False
            else:
                rankid = rankdist[np.int0(np.random.uniform(0, len(rankdist)))]
                
            
            cursor = conn.cursor()
            cursor.execute(f'''
                            insert into [lawyers]([person id], [firm id], [rank id], [bar id])
                            values({personid}, {firmid}, {rankid}, {barid});
                            ''')
            cursor.commit()
    
    
def genCourt(conn):
    HIGH_CHANCE = 1/10
    SUPREMES = (114, 185)
    
    cursor = sqlexec(conn,
                    '''
                    select * from [cities];
                    ''',
                    return_=True)
    
    for (cityid, cityname) in cursor:
        name = cityname + '`s court of justice'
        cursor = conn.cursor()
        cursor.execute(f'''
                            insert into [Courts]([name], [city id], [level id])
                            values(\'{name}\', {cityid}, 1);
                            ''')
        cursor.commit()
        if np.random.random() <= HIGH_CHANCE or cityid in SUPREMES:
            name = cityname + '`s high court of justice'
            cursor = conn.cursor()
            cursor.execute(f'''
                            insert into [Courts]([name], [city id], [level id])
                            values(\'{name}\', {cityid}, 2);
                            ''')
            cursor.commit()
        if cityid in SUPREMES:
            name = cityname + '`s supreme court of justice'
            cursor = conn.cursor()
            cursor.execute(f'''
                            insert into [Courts]([name], [city id], [level id])
                            values(\'{name}\', {cityid}, 3);
                            ''')
            cursor.commit()
    
    
def getPerson(conn, cityid: int, amount: int):
    cursor = sqlexec(conn,
                     f'''
                     select top {amount} [person id] from [people]
                     where [city id] = {cityid} and 
                     [person id] not in 
                        (select l.[person id] from [lawyers] l)
                     and
                     [person id] not in 
                        (select j.[person id] from [judges] j)
                     order by newid();
                     ''',
                     return_= True)
    return cursor


def genJudges(conn):
    cursor = sqlexec(conn, 
                     'select [city id] from cities',
                     return_=True)
    for c in cursor:
        ctid = c[0]
        pids = getPerson(conn, ctid, int(np.random.uniform(1, 5)))
        for p in pids:
            pid = p[0]
            crid = sqlexec(conn,
                             f'''
                             select top 1 [court id] from [courts]
                             where [city id] = {ctid}
                             order by newid();
                             ''',
                             return_=True)[0][0]
            cursor = conn.cursor()
            print(f'''
                           insert into [judges]([person id], [court id])
                           values({pid}, {crid});
                           ''')
            cursor.execute(f'''
                           insert into [judges]([person id], [court id])
                           values({pid}, {crid});
                           ''')
            cursor.commit()
        
        
def getLawyers(conn, cityid: int, amount: int):
    print(f'''
                     select top {amount} l.[person id], l.[bar id] from [lawyers] l, [people] p
                     where l.[person id] = p.[person id] and 
                     p.[city id] = {cityid}
                     order by newid();
                     ''')
    cursor = sqlexec(conn,
                     f'''
                     select top {amount} l.[person id], l.[bar id] from [lawyers] l, [people] p
                     where l.[person id] = p.[person id] and 
                     p.[city id] = {cityid}
                     order by newid();
                     ''',
                     return_= True)
    return cursor

def getJudges(conn, cityid: int, amount: int):
    print(f'''
                     select top {amount} j.[person id], j.[court id] from [judges] j, [people] p
                     where j.[person id] = p.[person id] and 
                     p.[city id] = {cityid}
                     order by newid();
                     ''')
    cursor = sqlexec(conn,
                     f'''
                     select top {amount} j.[person id], j.[court id] from [judges] j, [people] p
                     where j.[person id] = p.[person id] and 
                     p.[city id] = {cityid}
                     order by newid();
                     ''',
                     return_= True)
    return cursor

def getCity(conn):
    cursor = sqlexec(conn,
                     '''
                     select top 1 [city id]
                     from [cities]
                     order by newid();
                     ''',
                     return_=True)
    return cursor[0][0]

def genTrial(conn: pyodbc.Connection, amount: int):
    
    fake = Faker()
    cursor = conn.cursor()
    conclusions = ['\'innocent\'', '\'sent to 5 years in prison\'', '\'sent to 10 years in prison\'', '\'sent to 15 years in prison\'',  '\'sent to 2 years in prison\'',  '\'sent to 20 years in prison\'',  '\'sent to death\'']
    teams = ['\'Offense\'', '\'Defense\'']
    # generate trial:
    for i in range(amount):
        # subject id
        sid = sqlexec(conn, return_=True,
                    query=f'''
                    select top 1 [specialization id] from [specializations]
                    order by newid();''')[0][0]
        
        
        # date
        date = f'''\'{fake.date_between(start_date='-8y', end_date='today')}\''''
        text = f'''\'{fake.paragraph(nb_sentences=5, variable_nb_sentences=False)}\''''
        
        ctid = getCity(conn)
        crid = sqlexec(conn,
                             f'''
                             select top 1 [court id] from [courts]
                             where [city id] = {ctid}
                             order by newid();
                             ''',
                             return_=True)[0][0]
        try:
            cursor.execute(f'''
                        insert into [trials]([subject id], [date], [description], [court id])
                        values({sid}, {date}, {text}, {crid});
                        ''')
            cursor.commit()
        except pyodbc.IntegrityError:
            continue
            
        
        
        trid = sqlexec(conn, return_=True,
                       query=f'''
                       select top 1 [trial id] from [trials]
                       where [subject id] = {sid} and 
                       [date] = {date} and 
                       [description] = {text} and
                       [court id] = {crid};
                       ''')[0][0]
        print(trid)
        # generate defendants:
        for pid in getPerson(conn, ctid, int(np.random.uniform(1.1, 10))):
            pid = pid[0]
            conclusion = choice(conclusions)
            print(f'''
                           insert into [defendants]([trial id], [person id], [conclusion])
                           values({trid}, {pid}, {conclusion});''')
            cursor.execute(f'''
                           insert into [defendants]([trial id], [person id], [conclusion])
                           values({trid}, {pid}, {conclusion});''')
            cursor.commit()
        
        # generate judges in trial:
        for (jid, cridt) in getJudges(conn, ctid, int(np.random.uniform(1.1, 6))):
            cursor.execute(f'''
                           insert into [judges in trial]([trial id], [person id], [court id])
                           values({trid}, {jid}, {cridt});''')
            cursor.commit()
            
            
        # generate lawyers in trial:
        i = 0
        team = teams[0]
        for (lid, brid) in getLawyers(conn, getCity(conn), int(np.random.uniform(2.1, np.random.uniform(2.2, 10)))):
            if i == 0:
                team = teams[0]
            elif i == 1:
                team = teams[1]
            else:
                team = choice(teams)
            cursor.execute(f'''
                           insert into [lawyers in trial]([trial id], [person id], [bar id], [team])
                           values({trid}, {lid}, {brid}, {team});''')
            cursor.commit()
            i += 1
        

