import logging
import os
from pymongo import MongoClient
from opentelemetry.instrumentation.pymongo import PymongoInstrumentor
from telemetry.tracing import provider, tracer, trace

logger = logging.getLogger(__name__)

# make sure our pw to our mongo service is set
with tracer.start_as_current_span("startup-event"):
    span = trace.get_current_span()
    span.add_event("checking for MONGODB_PW environment variable", {"environment": str(os.environ)})
    MONGODB_PW = os.environ.get("MONGODB_PW")
    if not MONGODB_PW:
        logger.error("MONGODB_PW not set")
        exit(1)
    else:
        logger.debug("MONGODB_PW is %s" % MONGODB_PW)

PymongoInstrumentor().instrument(tracer_provider=provider)

client = MongoClient("mongodb+srv://thinks:%s@thinks.kiq2w.mongodb.net/?retryWrites=true&w=majority" % MONGODB_PW)
db = client.thinks
bubbles = db.bubbles
