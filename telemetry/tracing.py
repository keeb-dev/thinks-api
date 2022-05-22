from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace.export import BatchSpanProcessor



# set up the otel stuff
provider = TracerProvider(
       resource=Resource.create({SERVICE_NAME: "think-app"})
)
jaeger_exporter = JaegerExporter(
   agent_host_name="edgelord",
   agent_port=6831,
)
provider.add_span_processor(BatchSpanProcessor(jaeger_exporter))


trace.set_tracer_provider(provider)
tracer = trace.get_tracer(__name__)