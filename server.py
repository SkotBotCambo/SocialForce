from flask import Flask, send_from_directory
import os

'''Example taken from http://codepen.io/asommer70/blog/serving-a-static-directory-with-flask'''

app = Flask(__name__, static_url_path='/map')
app.debug = True


@app.route('/')
def send_index():
    return send_from_directory('static/static_html', 'index.html')

@app.route('/map')
def send_static_html():
	return send_from_directory('static/static_html', 'map.html')

@app.route('/map2')
def send_static_html2():
	return send_from_directory('static/static_html', 'map2.html')

@app.route('/js/draw-map.js')
def send_js():
	return send_from_directory('static/js/', 'draw-map.js')
'''
@app.route('/css/example.css')
def send_css(path):
    return send_from_directory('static/css', path)
'''

@app.route('/csv/city-ratio-file.csv')
def send_csv(path):
    return send_from_directory('static/csv', path)

if __name__ == "__main__":
    host_loc = "127.0.0.1"
    print("Running server at %s" % host_loc)
    port = int(os.environ.get('PORT', 5000))
    app.run(host=host_loc, port = port)