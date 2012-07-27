import sqlite3 as lite

class sql:
	def __init__( self, logger, db='./data/loots.db' ):
		self.db, self.log = lite.connect( db, isolation_level=None ), logger.write
		self.cur = self.db.cursor()
		self.cur.execute( 'CREATE TABLE IF NOT EXISTS LoL_Alerts( ID INTEGER PRIMARY KEY, user TEXT, initial_alert TEXT)' )


	def insert( self, user ):
		self.log( 'MOD_SQL', 'Inserting {} into database'.format( user ) )
		self.cur.execute( 'INSERT INTO LoL_Alerts(user, initial_alert) VALUES ("{}", "False")'.format( user ) )

	def remove( self, user ):
		self.log( 'MOD_SQL', 'Removing {} From Database'.format( user ) )
		self.cur.execute( 'DELETE FROM LoL_Alerts WHERE user="{}"'.format( user ) )

	def dump_new( self ):
		users = [ record[0] for record in self.cur.execute( 'SELECT (user) FROM LoL_Alerts WHERE initial_alert != "True"' ) ]
		self.update()
		return users

	def dump( self ):
		return [ record[0] for record in self.cur.execute( 'SELECT (user) FROM LoL_Alerts' ).fetchall() ]

	def update( self ):
		self.cur.execute( 'UPDATE LoL_Alerts SET initial_alert="True" WHERE initial_alert="False"' )

	def close( self, nuke_db=False ):
		if self.db:
			if nuke_db:
				self.cur.execute( 'DROP TABLE IF EXISTS LoL_Alerts' )
			self.db.close()
