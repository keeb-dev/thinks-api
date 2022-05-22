The following env variables need to be set
* MONGODB_PW
* OTEL_PYTHON_LOG_CORRELATION = true

Also the JaegerExporter is hardcoded to output to `edgelord` in `service/thinks.py`, this should be changed. And I should probably also make it w

Lastly, also in `service/thinks.py` we create a mongodb client which also is hardcoded to use a database called `thinks`