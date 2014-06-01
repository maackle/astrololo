module.exports = (grunt) ->

	livereloadPort = 17364

	# Project configuration.
	grunt.initConfig
		pkg: grunt.file.readJSON('package.json')

		config:
			app: 'assets'
			dist: 'static'

		# connect:
		# 	server:
		# 		options:
		# 			port: 1337
		# 			open: true
		# 			livereload: livereloadPort
		# 			base: '<%= config.dist %>'

		watch:
			livereload:
				files: [
					"<%= config.dist %>/**/*.{css,js,html}"
				]
				options:
					livereload: livereloadPort
			coffee:
				files: ["<%= config.app %>/scripts/*.coffee"]
				tasks: ['coffee']
			compass:
				files: ["<%= config.app %>/styles/*.{sass,scss}"]
				tasks: ['compass']


		coffee:
			options:
				join: true
			compile:
				files:
					"<%= config.dist %>/build/main.js": [
						"<%= config.app %>/scripts/*.coffee",
					] # // compile and concat into single file

		compass:
			dist:
				options:
					sassDir: "<%= config.app %>/styles/",
					cssDir: "<%= config.dist %>/build/",
					environment: 'production'


	grunt.loadNpmTasks('grunt-contrib-coffee')
	grunt.loadNpmTasks('grunt-contrib-watch')
	grunt.loadNpmTasks('grunt-contrib-compass')
	grunt.loadNpmTasks('grunt-contrib-connect')
	grunt.loadNpmTasks('grunt-notify')

	#// Default task(s).
	grunt.registerTask 'default', [
		'build'
		'watch'
	]

	grunt.registerTask 'build', [
		'coffee:compile'
		'compass:dist'
	]