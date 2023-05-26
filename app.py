from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/play', methods=['GET', 'POST'])
def get_word():
    # This is where you would get a word from your word source.
    # For the time being, let's just return a static word.
    return jsonify({"word": "HELLO"})

# Only run code when imported as script, not a module
if __name__ == '__main__':
    app.run(debug=True)