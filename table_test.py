import sqlite3

conn = sqlite3.connect('Experiments.db')
tableName = 'stocks'
columnNames = ['date text', 'trans text', 'symbol text', 'qty real', 'price real']
fieldsNum = 5
columnNamesString = ','.join(['{}']*fieldsNum).format(*columnNames)
QUESTIONMARKS = ','.join(['?']*fieldsNum)
data = ['2006-01-05', 'BUY', 'RHAT', 100, 35.14]

c = conn.cursor()
c.execute('CREATE TABLE {} '.format(tableName) + '(' + columnNamesString + ')')
c.execute('INSERT INTO {} VALUES ({})'.format(tableName, QUESTIONMARKS), tuple(data))

#commit the changes to db			
conn.commit()
#close the connection
conn.close()