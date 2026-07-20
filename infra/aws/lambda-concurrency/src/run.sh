#!/bin/bash
# Web Adapter startup command (Handler = run.sh). Starts the HTTP server that the
# adapter forwards each invocation to. exec so the server receives Lambda's signals.
exec node server.mjs
