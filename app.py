from search import search
from flask import Flask, request, send_from_directory, escape, Markup
app = Flask(__name__)

TEMPLATE = Markup('''<html><head><title>PDF Searcher</title></head><body>%s</body><html>''')

@app.route('/png/<path:path>')
def send_page(path):
    return send_from_directory('build/png', path)


@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
      count, results = search(request.form.get('authority'), request.form.get('q'))
      html = Markup('<h1>Search Planning Documents</h1><p>Search results for <tt>%s</tt> <tt>%s</tt>.</p>') % (
        request.form.get('authority', None),
        request.form.get('q', None),
      )
      if (results):
          html += Markup('<ul>')
          for result in results:
              html += Markup('<li>')+Markup('<a href="/png/')+result['name']+Markup('/')+result['page_number']+Markup('.png">')+escape(result['name']+' page '+result['page_number'])+Markup('</a>')+Markup('</li>')
          html += Markup('</ul>')
      else:
          html += Markup('<p>No results</p>')
      return TEMPLATE % html
    else:
      return TEMPLATE % Markup('''
<h1>Search Planning Documents</h1>

<form method="POST">
<span style="display: inline-block; width: 100px">Authority: </span><input type="text" name="authority"><br>
<span style="display: inline-block; width: 100px">Keywords: </span><input type="text" name="q"><br>
<span style="display: inline-block; width: 100px"></span><input type="submit" value="Search">
</form>''')
