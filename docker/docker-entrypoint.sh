#!/bin/sh

# startup message
/bin/echo "YFPY is ready!"

# execute CMD from Dockerfile
exec "$@"
