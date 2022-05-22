import os
from opentelemetry import trace
from pymongo import MongoClient
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
   BatchSpanProcessor,
   ConsoleSpanExporter,
)
from opentelemetry.instrumentation.pymongo import PymongoInstrumentor
import datetime

provider = TracerProvider()
processor = BatchSpanProcessor(ConsoleSpanExporter())
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)
tracer = trace.get_tracer(__name__)

with tracer.start_as_current_span("service_thinks_setup"):
    with tracer.start_as_current_span("mongopw"):
        # make sure our pw to our mongo service is set
        print("making sure the MONGODB_PW is set")
        MONGODB_PW = os.environ.get("MONGODB_PW")
        if not MONGODB_PW:
            print("MONGODB_PW not set")
            exit(1)
        else:
            print("MONGODB_PW is %s" % MONGODB_PW)

PymongoInstrumentor().instrument()
client = MongoClient("mongodb+srv://thinks:%s@thinks.kiq2w.mongodb.net/?retryWrites=true&w=majority" % MONGODB_PW)
db = client.thinks
bubbles = db.bubbles


def get_think_list():
    the_actual_list = []
    with tracer.start_as_current_span("service_thinks_method"):
        with tracer.start_as_current_span("get_think_list"):
            for thinks in bubbles.find():
                print("the thinks i got was", thinks)
                the_actual_list.append(thinks)
            return the_actual_list


def store_think(think):
    with tracer.start_as_current_span("service_thinks_method"):
        with tracer.start_as_current_span("store_think"):
            print("got think: %s " % think)
            print("building think record")
            post = {"text": think,
                    "date": datetime.datetime.utcnow()}
            print("think record: ", post)
            bubbles.insert_one(post)


