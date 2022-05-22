from flask import Flask, jsonify
import os
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from service.thinks import get_think_list, store_think
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource

# set up the otel stuff
provider = TracerProvider(
       resource=Resource.create({SERVICE_NAME: "think-app"})
)
jaeger_exporter = JaegerExporter(
   agent_host_name="edgelord",
   agent_port=6831,
)

provider.add_span_processor(BatchSpanProcessor(jaeger_exporter))

# set up flask and instrumentation
app = Flask(__name__)
FlaskInstrumentor().instrument_app(app, tracer_provider=provider)


@app.route("/api/thinks", methods=["GET"])
def thinks():
    this_is_how_we_do_it = get_think_list()
    thx = [x["text"] for x in this_is_how_we_do_it]
    return jsonify(thx)


# noop but needs to save to the persistent store
@app.route("/api/think", methods=["POST"])
def new_think():
    return 201


@app.route("/api/think", methods=["GET"])
def get_think():
    # need to remember how to take arguments here
    # i think you do /api/thot/:1 ?
    return jsonify(["poop"])


@app.route("/secret")
def secret():
    # we are adding some data in secret!!
    store_think("i am thinking about something and it is really great")
    return "", 201


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=os.getenv("PORT", default=5000))
