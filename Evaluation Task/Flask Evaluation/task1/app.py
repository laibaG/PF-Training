from flask import Flask, render_template, request, url_for

app = Flask(__name__)


@app.route('/')
def rend():
    return render_template('square.html')

@app.route('/square', methods=['GET', 'POST'])
def square_number():
    if request.method == 'POST':
        number = request.form.get('number')

        if not number:
            return render_template('square.html', error='Number not provided')

        try:
            squared_number = float(number) ** 2
            return render_template('square.html', number=squared_number)
        except ValueError:
            return render_template('square.html', error='Invalid number')

    return render_template('square.html')

if __name__ == '__main__':
    app.run(debug=True)
