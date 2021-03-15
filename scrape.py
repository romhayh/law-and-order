from bs4 import BeautifulSoup
import requests
import lxml.html as lh
import pandas as pd
import pyodbc 


def sqlexec(conn, query:str, print_:bool = False):
    cursor = conn.cursor()
    cursor.execute(query)
    if print_:
        for row in cursor:
            print(row)
    conn.commit()


conn = pyodbc.connect('Driver={SQL Server Native Client 11.0};'
                      'Server=DESKTOP-NBQ4LO7;'
                      'Database=law and order;'
                      'Trusted_Connection=yes;')






url1 = r'https://en.wikipedia.org/wiki/List_of_cities_in_Israel'
url2 = r'https://en.wikipedia.org/wiki/List_of_United_States_cities_by_population'
url3 = r'https://www.brown.edu/academics/college/advising/law-school/fields-law/fields-law'

source = requests.get(url2).text
soup = BeautifulSoup(source, 'lxml')
print(soup.body.get_text())
# for i,l in enumerate(soup.find('article').find_all('h2')):
#     print(l)


"""

#* this is the code for url2
tables = pd.read_html(url2, '.+')
print("There are : ", len(tables), " tables")
i = 0
for (i, l) in enumerate(tables[4]['City']):
    print((l.split('['))[0])
    query = f'insert into [cities] values(\'{l}\') '
    try:
        sqlexec(conn, query)
    except:
        print('Failed')
#* this is the code for url1
for l in tables[0]:
    print (l)
    l = ((l.split('['))[0]).replace("'", '')
    #print(l)
    query = f'insert into [cities] values(\'{l}\') '
    print(query)
    #sqlexec(conn, query)

"""

    
conn.close()
    
        