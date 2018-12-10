import sqlite3
#import string

def p(s):
	return s.replace("'","\'")

class DataBase(sqlite3.Connection):
	def __init__(self,db):
		super().__init__(db,check_same_thread = False)
		self.dbcursor = self.cursor()
	def add_file_id(self,client_id,file_id,d,cursor = False):
		if not cursor:
			cursor = self.dbcursor
		cursor.execute( "INSERT INTO Audio (client_id,file_id,description) VALUES (%s,'%s','%s')" % (client_id,p(file_id),p(d).lower()))
		self.commit()
	def search(self,client_id,description):
		query = self.dbcursor.execute("SELECT file_id,description FROM Audio WHERE client_id = {} AND description like '%{}%'".format(client_id, description.lower()) )
		files = query.fetchall()
		if files != None:
			return files
		else:
			return []
	def get_voices(self,client_id):
		query = self.dbcursor.execute('SELECT file_id,description FROM Audio WHERE client_id = {}'.format(client_id))
		fetch = query.fetchall()
		data = []
		for i in fetch:
			data.append({'file_id':i[0],'description':i[1]})
		return data
	def delete(self,file_id):
		query = self.dbcursor.execute("DELETE FROM Audio WHERE file_id = '{}'".format(file_id))
		self.commit()