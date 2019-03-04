import sys
import shutil
import os
from flask import (
    Flask,
    Markup,
    render_template,
    render_template_string,
    request,
    send_file )
from os import listdir
import zipfile
from flask_frozen import Freezer
from werkzeug import secure_filename
from shelljob import proc
#from flask.ext.autoindex import AutoIndex

DEBUG = True

app = Flask(__name__)
freezer = Freezer(app)
app.config.from_object(__name__)


@app.route("/")
def index():
    return render_template('index.html')

@app.route('/links/')
def links():
    return render_template('links.html')

@app.route("/about/")
def about():
    return render_template('about.html')

@app.route("/url/")
def url():
    return render_template('url.html')

@app.route("/urlsfile/")
def urlsfile():
    return render_template('urlsfile.html')

@app.route('/vulnfile/', methods = ['GET', 'POST'])
def enter_url():
   if request.method == 'POST':
      text = request.form['url']
      shutil.rmtree("static/files")
      os.makedirs("static/files")
      f = open("vulnurls.txt", "w")
      f.write(text+"\n")
      f.close()
      import wpvuln
      dir=text[text.find('://www.')+7:text.find('.',text.find('://www.')+7)]
      os.chdir(os.getcwd()+"/static/files")
      path = str(os.getcwd())+"/"+dir
      shutil.make_archive("download", 'zip', path)
      os.chdir("C:/Users/daddela/Pictures/wpvuln")
      return render_template('vulnfile.html')

@app.route('/vulnfiles/', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      f.save(secure_filename(f.filename))
      shutil.rmtree("static/files")
      os.makedirs("static/files")
      import wpvuln
      file = open(f.filename, "r")
      for line in file:
          dir=line[line.find('://www.')+7:line.find('.',line.find('://www.')+7)]
          path = os.getcwd()+"/static/files/"+dir
          shutil.make_archive(path, 'zip', path)
      os.chdir(os.getcwd()+"/static/files")
      zip = zipfile.ZipFile('download.zip', 'w')
      for f in listdir(os.getcwd()):
          if f.endswith('.' + "zip") and 'download.zip' not in f :
              print(f)
              zip.write(f, compress_type=zipfile.ZIP_DEFLATED)
      zip.close()
      file.close()
      os.chdir("C:/Users/daddela/Pictures/wpvuln")
      return render_template('vulnfiles.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route("/404.html")
def static_404():
  return render_template('404.html')


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        freezer.freeze()
    else:
        app.run(debug=True)
