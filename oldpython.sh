#!/usr/bin/bash
#docker image build -t oldpython:1.0 .
docker run -ti --mount type=bind,src="$(pwd)",dst=/queue oldpython:1.0 /bin/bash
