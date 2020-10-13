import boto3

from opentelemetry import trace

# aws propagator
# TODO: Uncomment once ids_generator is released to PyPi
# from opentelemetry.propagator.xray_id_generator import AWSXRayIdsGenerator

from opentelemetry.sdk.resources import (
    Resource,
    OTELResourceDetector,
    get_aggregated_resources,
)
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    ConsoleSpanExporter,
    SimpleExportSpanProcessor,
)

# instrumentor
from opentelemetry.instrumentation.botocore import BotocoreInstrumentor

# TODO: Uncomment once ids_generator is released to PyPi
# trace.set_tracer_provider(TracerProvider()
#     ids_generator=AWSXRayIdsGenerator(), 
# )
trace.set_tracer_provider(TracerProvider())

# === jaeger exporter
# from opentelemetry.exporter import jaeger
# jaeger_exporter = jaeger.JaegerSpanExporter(
#     service_name="my-multi-processors",
#     agent_host_name="localhost",
#     agent_port=6831,
# )
# trace.get_tracer_provider().add_span_processor(
#     SimpleExportSpanProcessor(jaeger_exporter)
# )

trace.get_tracer_provider().add_span_processor(
    SimpleExportSpanProcessor(ConsoleSpanExporter())
)

# === otlp exporter, collector
from opentelemetry.exporter.otlp.trace_exporter import OTLPSpanExporter
otlp_exporter = OTLPSpanExporter(endpoint="localhost:55680")
span_processor = SimpleExportSpanProcessor(otlp_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

# === xray daemon exporter, xray daemon
# from opentelemetry.exporter.xraydaemon import XrayDaemonSpanExporter
# xrayDaemonSpanExporter = XrayDaemonSpanExporter()
# trace.get_tracer_provider().add_span_processor(
#     SimpleExportSpanProcessor(xrayDaemonSpanExporter)
# )

tracer = trace.get_tracer(__name__)

# Customer's lambda function
def main():

    s3 = boto3.resource('s3')
    for bucket in s3.buckets.all():
        print(bucket.name)

    return "200 OK"

# Manual enable otel instrumentation
BotocoreInstrumentor().instrument(tracer_provider=trace.get_tracer_provider())

main()
