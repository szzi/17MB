#web server on webos (python Flask)
from flask import Flask,render_template

app = Flask(__name___

#default page
@app.route("/")
def index():
    return render_template('../index.html')
