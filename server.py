from flask import Flask, send_from_directory
import pickle
import os

'''Example taken from http://codepen.io/asommer70/blog/serving-a-static-directory-with-flask'''

app = Flask(__name__, static_url_path='/map')
app.debug = True


@app.route('/')
def send_index():
    ''' send_index() returns the html file to display the map.
        This file includes all the javascript necessary to do the 
        Plotly rendering. '''
    return send_from_directory('static/static_html', 'map3.html')

@app.route('/map')
def send_csv():
    '''send_csv() returns the csv file containing the most
    recent data from Google Trends.'''
    return send_from_directory('static/csv/', 'city-ratio-correct-format.csv')

if __name__ == "__main__":
    host_loc = "127.0.0.1"
    print("Running server at %s" % host_loc)
    port = int(os.environ.get('PORT', 5000))
    app.run(host=host_loc, port = port)