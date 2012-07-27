#!/usr/bin/python

"""
	LoL_Alerter - Implementation of Text Alerts for NA League Servers

	This program is free software; you can redistribute it and/or modify
	it freely. This program is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
	or FITNESS FOR A PARTICULAR PURPOSE.
"""

from mods.logger import logger
from mods.sql import sql
from mods.sms import sms
from mods.parser import lol_parser as lp
from time import sleep

class LOL_ALERTS:
	def __init__( self ):
		self.logger, self.lp, self.TTL = logger(), lp(), (10 * 60)
		self.db, self.log = sql( self.logger ), self.logger.write

	def daemonize( self ):
		last_update, ServersUp, Alert = None, True, 'LoL Servers Are Back Up Fully Operational, Time To Game ~eCo'
		self.log( 'MAIN', 'Initial Start-Up' )
		try:	
			while (1):
				self.log( 'MAIN', 'Checking For Updates' )
				sms( self.logger, self.db ).pullTexts( True ) 
				if last_update is not None:
					sms( self.logger, self.db ).spamNew( last_update )

				if not self.lp.serversUp():
					ServersUp, self.TTL, ret = False, 60, self.lp.parseThread()
					if ret is not None:
						self.log( 'MAIN', 'New Update, Spamming users' )
						last_update = ret
						sms( self.logger, self.db ).spam( ret )
						self.db.update()
					else:
						self.log( 'MAIN', 'No New Updates, Continuing Execution' )
				else:
					if not ServersUp:
						sms( self.logger, self.db ).spam( Alert )
						self.TTL, ServersUp = (10 * 60), True
					self.log( 'MAIN', 'NA Servers Operational, Going to sleep' )

				sleep( self.TTL )
		except KeyboardInterrupt:
			self.log( 'MAIN', 'Caught SIGINT, Now Exiting' )
		except:
			self.log( 'MAIN', 'Caught Unhandled Exception, Now Exiting' )

if __name__ == '__main__':
	la = LOL_ALERTS()
	la.daemonize()
