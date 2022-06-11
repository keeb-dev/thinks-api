from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
import os

AGENT_HOSTNAME = os.getenv("AGENT_HOSTNAME", "localhost")
AGENT_PORT = int(os.getenv("AGENT_PORT", "4317"))

# set up the otel stuff
provider = TracerProvider(
       resource=Resource.create({SERVICE_NAME: "think-app"})
)

trace.set_tracer_provider(provider)
tracer = trace.get_tracer(__name__)


otlp_exporter = OTLPSpanExporter(endpoint=f"{AGENT_HOSTNAME}:{AGENT_PORT}", insecure=True)
provider.add_span_processor(BatchSpanProcessor(otlp_exporter))


