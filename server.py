from application import setup

app = setup()

if __name__ == '__main__':
	# handler = RotatingFileHandler("log/error.log", maxBytes=10000000, backupCount=10)
	# handler.setLevel(logging.WARNING)
	# app.logger.addHandler(handler)

	app.run(debug=True, port=45535)