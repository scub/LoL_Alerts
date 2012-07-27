from BeautifulSoup import BeautifulSoup
from urllib2 import urlopen

class lol_parser:
	def __init__( self ):
		self.url, self.last_update = 'http://na.leagueoflegends.com/service-status', ''

	def serversUp( self ):
		status = ''.join( BeautifulSoup( urlopen( self.url ).read() ).find( 'span', { 'class' : 'service-status-text' } ).find( 'h2' ).findAll( text=True ) )

		if "Online" in status:
			return True
		else:
			return False

	def parseThread( self ):
		try:
			thread_uri = BeautifulSoup( urlopen( self.url ).read() ).find( 'div', {'class': 'field-content' } ).find( 'a' )[ 'href' ]
			raw_post = BeautifulSoup( urlopen( thread_uri ).read() ).find( 'div', {'class' : 'post_content' } )

			if raw_post.find( 'b' ):
				update = raw_post.find( 'b' ).text
				if self.last_update != update:
					self.last_update = update
					return update
			else:
				if self.last_update != raw_post.text:
					self.last_update = raw_post.text
					return self.last_update
		except:
			return None
		return None
