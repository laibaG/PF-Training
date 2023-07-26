from flask import Flask, render_template, request, url_for

app = Flask(__name__)

@app.route('/')
def rend():
    return render_template('table.html')

@app.route('/table', methods=['GET', 'POST'])
def generate_table():
    if request.method == 'POST':
        number = int(request.form.get('number'))

        if number is None:
            return render_template('table.html', error='Number not provided')

        table = [number * i for i in range(1, 11)]
        return render_template('table.html', number=number, table=table)

    return render_template('table.html')

if __name__ == '__main__':
    app.run(debug=True)