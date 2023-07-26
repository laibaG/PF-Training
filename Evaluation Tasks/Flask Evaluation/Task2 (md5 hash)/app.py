import hashlib
from flask import Flask, render_template, request, url_for

app = Flask(__name__)

@app.route('/')
def rend():
    return render_template('md5.html')

@app.route('/image_md5', methods=['GET', 'POST'])
def image_md5():
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('md5.html', error='No file part')

        image_file = request.files['file']
        if image_file.filename == '':
            return render_template('md5.html', error='No selected file')

        try:
            im_bytes = image_file.read()
            im_hash = hashlib.md5(im_bytes).hexdigest()
            return render_template('md5.html', md5_hash=im_hash)
        except Exception as e:
            return render_template('md5.html', error=str(e))

    return render_template('md5.html')
