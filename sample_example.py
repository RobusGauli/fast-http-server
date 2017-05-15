from one import Robus

from one.response import json

app = Robus(__name__)

@app.route('/home')
def home(request):
    return json(dict(name='ribus'))

if __name__ == '__main__':
    app.run(hostname='localhost', port=12000)
