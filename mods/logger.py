from time import strftime

class logger:
	def __init__( self, verbose=True, filename='./data/logs.txt' ):
		self.verbose, self.filename = verbose, filename

	def write( self, PREFIX, MESSAGE ):
		fd = open( self.filename, 'a' )
		if fd:
			fd.write( "[{}] - {} : {}\n".format( strftime("%d/%m/%Y %H:%M:%S"), PREFIX, MESSAGE ) )
			fd.close()

		if self.verbose:
			print "[+] [{}] - {} : {}".format( strftime( "%H:%M:%S" ), PREFIX, MESSAGE )
