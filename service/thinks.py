import os
import logging
import datetime
from pymongo import MongoClient
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.pymongo import PymongoInstrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor


# set up the otel stuff
provider = TracerProvider(
       resource=Resource.create({SERVICE_NAME: "think-app"})
)
jaeger_exporter = JaegerExporter(
   agent_host_name="edgelord",
   agent_port=6831,
)
provider.add_span_processor(BatchSpanProcessor(jaeger_exporter))
LoggingInstrumentor().instrument(set_logging_format=True)
PymongoInstrumentor().instrument(tracer_provider=provider)
trace.set_tracer_provider(provider)
tracer = trace.get_tracer(__name__)

# make sure our pw to our mongo service is set
with tracer.start_as_current_span("startup-event"):
    span = trace.get_current_span()
    span.add_event("checking for MONGODB_PW environment variable", {"environment": str(os.environ)})
    MONGODB_PW = os.environ.get("MONGODB_PW")
    if not MONGODB_PW:
        logging.error("MONGODB_PW not set")
        exit(1)
    else:
        logging.debug("MONGODB_PW is %s" % MONGODB_PW)


client = MongoClient("mongodb+srv://thinks:%s@thinks.kiq2w.mongodb.net/?retryWrites=true&w=majority" % MONGODB_PW)
db = client.thinks
bubbles = db.bubbles


def get_think_list():
    the_actual_list = []
    for thinks in bubbles.find():
        logging.debug("the thinks i got was", thinks)
        the_actual_list.append(thinks)
    return the_actual_list


def store_think(think):
    logging.debug("got think: %s " % think)
    logging.debug("building think record")
    post = {"text": think,
            "date": datetime.datetime.utcnow()}
    logging.debug("think record: ", post)
    bubbles.insert_one(post)


