# OCI Functions / Fn Project - Python FDK base image
FROM fnproject/python:3.11 as build-stage

# Set working directory used by Fn
WORKDIR /function

# Install Python deps into the special /python path
ADD requirements.txt /function/
RUN pip3 install --target /python/ -r requirements.txt

# Add the function code
ADD . /function/

# Use the FDK entrypoint and point to our handler
ENTRYPOINT ["/python/bin/fdk", "/function/src/func.py", "handler"]
