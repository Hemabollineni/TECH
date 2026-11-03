from flask import Flask, jsonify

# Create Flask application
app = Flask(__name__)


# Create GET API
@app.route('/welcome', methods=['GET'])
def welcome():

    return jsonify({
        "message": "Welcome to Flask API"
    })


# Run Flask server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)