import os
import logging
from flask import Flask, jsonify, request
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from service.thinks import get_think_list, store_think
from telemetry.tracing import provider, trace

LoggingInstrumentor().instrument(set_logging_format=True, log_level=logging.DEBUG)
logger = logging.getLogger(__name__)

# set up flask and instrumentation
app = Flask(__name__)
FlaskInstrumentor().instrument_app(app, tracer_provider=provider)


@app.route("/api/thinks", methods=["GET"])
def thinks():
    this_is_how_we_do_it = get_think_list()
    return jsonify(this_is_how_we_do_it)


# noop but needs to save to the persistent store
@app.route("/api/think", methods=["POST"])
def new_think():
    rjson = request.json
    if not rjson or rjson.get("think") is None:
        span = trace.get_current_span()
        span.add_event("malformed request submitted", {"request data": request.data})
        logger.error("malformed request submitted")

    logger.debug("storing this think: %s" % rjson)
    store_think(rjson.get("think"))
    return "", 201


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=os.getenv("PORT", default=5000))
