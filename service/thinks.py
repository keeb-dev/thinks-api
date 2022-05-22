import os
from pymongo import MongoClient
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.pymongo import PymongoInstrumentor
import datetime

# set up the otel stuff
provider = TracerProvider(
       resource=Resource.create({SERVICE_NAME: "think-app"})
)
jaeger_exporter = JaegerExporter(
   agent_host_name="edgelord",
   agent_port=6831,
)
provider.add_span_processor(BatchSpanProcessor(jaeger_exporter))

# make sure our pw to our mongo service is set
print("making sure the MONGODB_PW is set")
MONGODB_PW = os.environ.get("MONGODB_PW")
if not MONGODB_PW:
    print("MONGODB_PW not set")
    exit(1)
else:
    print("MONGODB_PW is %s" % MONGODB_PW)

PymongoInstrumentor().instrument(tracer_provider=provider)
client = MongoClient("mongodb+srv://thinks:%s@thinks.kiq2w.mongodb.net/?retryWrites=true&w=majority" % MONGODB_PW)
db = client.thinks
bubbles = db.bubbles


def get_think_list():
    the_actual_list = []
    for thinks in bubbles.find():
        print("the thinks i got was", thinks)
        the_actual_list.append(thinks)
    return the_actual_list


def store_think(think):
    print("got think: %s " % think)
    print("building think record")
    post = {"text": think,
            "date": datetime.datetime.utcnow()}
    print("think record: ", post)
    bubbles.insert_one(post)


