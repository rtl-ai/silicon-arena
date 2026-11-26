FROM ubuntu:24.04
RUN apt-get update && apt-get install -y --no-install-recommends python3 yosys=0.33-5build2 && rm -rf /var/lib/apt/lists/*
ENV PYTHONDONTWRITEBYTECODE=1
USER 65534:65534
WORKDIR /tmp
ENTRYPOINT ["python3","/arena/tools/fast_judge.py","--engine","native"]
