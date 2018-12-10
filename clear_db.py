import sqlite3
if input('Delete [y/n]: ') == 'n':
	exit()
connection = sqlite3.connect('Audio.sql')
cursor = connection.cursor()
cursor.execute('DELETE FROM Audio')
connection.commit()
print('Deleted')