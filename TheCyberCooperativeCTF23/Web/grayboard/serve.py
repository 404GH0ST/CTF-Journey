from http.server import SimpleHTTPRequestHandler, HTTPServer

class MyHandler(SimpleHTTPRequestHandler):
	def end_headers(self):
		self.send_header('Access-Control-Allow-Origin', '*')
		SimpleHTTPRequestHandler.end_headers(self)

httpd = HTTPServer(('0.0.0.0', 80), MyHandler)
httpd.serve_forever()
