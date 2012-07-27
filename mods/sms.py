from googlevoice import Voice

class sms:
	def __init__( self, logger, db ):
		self.voice, self.user, self.passwd = Voice(), 'USERNAME_GOES_HERE', 'PASSWORD_GOES_HERE'
		self.log, self.db = logger.write, db
		self.voice.login( self.user, self.passwd )


	def pullTexts( self, purge=False ):
		messages = self.voice.sms().messages
		if not messages:
			self.log( 'MOD_SMS', 'No New Messages Were Received' )
			return

		self.log( 'MOD_SMS', 'New Messages Received, Now Parsing' )
		for msg in messages:
			if not msg.isRead:
				user, cmd = msg[ 'phoneNumber' ], msg[ 'messageText' ].lower() 

				if '!remove' in cmd:
					self.db.remove( user )
				else:
					self.db.insert( user )
			if purge:
				msg.delete()
		self.voice.logout()

	def spam( self, message ):
		for user in self.db.dump():
			self.log( 'MOD_SMS', 'Currently Spamming {}'.format( user ) )
			self.voice.send_sms( user, message )
		self.voice.logout()

	def spamNew( self, message ):
		for user in self.db.dump_new():
			self.log( 'MOD_SMS', 'Currently Spamming {} With Last Update'.format( user ) )
			self.voice.send_sms( user, message )
		self.voice.logout()
