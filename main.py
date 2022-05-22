from flask import Flask, jsonify
import os

app = Flask(__name__)

# of course eventually we need to actually maintain a list of these and persist them
thot_list = ["thot 1", "thot 2", "thot 3"]


# probably should also move the API to a separate endpoint or app so we can decouple viewing
# from the other stuff

@app.route('/')
def index():
    return "imagine making a website."


@app.route("/api/thots", methods=["GET"])
def thots():
    return jsonify(thot_list)


# noop but needs to save to the persistent store
@app.route("/api/thot", methods=["POST"])
def new_thot():
    return 201


@app.route("/api/thot", methods=["GET"])
def get_thot():
    # need to remember how to take arguments here
    # i think you do /api/thot/:1 ?
    return jsonify(thot_list[1])


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=os.getenv("PORT", default=5000))
