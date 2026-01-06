from flask import Flask, render_template, request
import functions

tracks_dict = functions.read_json("Data/tracks.json")
tmx_recs = functions.read_json("Data/tmx_replays.json")
dedi_recs = functions.read_json("Data/dedi_replays.json")

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html', tracks=tracks_dict)

@app.route('/track/<track_id>')
def track(track_id):
    tmx = tmx_recs[track_id]
    dedi = dedi_recs[track_id]
    return render_template('records.html', track_id=track_id, tmx_records=tmx, dedi_records=dedi)

if __name__ == '__main__':
    app.run(debug=True)