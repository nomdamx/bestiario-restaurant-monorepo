from app import create_app,socketio
import os
from app.sockets import *

app = create_app()

@app.route('/favicon.ico')
def favicon():
    from flask import send_from_directory
    return send_from_directory(
        os.path.join(app.root_path, 'static'),
        'favicon.ico',
        mimetype='image/vnd.microsoft.icon'
    )

@app.route('/')
def index():
    return "Index de la api"

if __name__ == "__main__":
    socketio.start_background_task(ticket_watcher,app)
    socketio.run(app,host="0.0.0.0", port=5000,debug=False,use_reloader=False) # type: ignore