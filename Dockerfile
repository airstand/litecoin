FROM ubuntu:18.04 as packager
ADD shasum.py /tmp/
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
  curl \
  ca-certificates \
  python3 \
  && curl -fsSL https://download.litecoin.org/litecoin-0.17.1/linux/litecoin-0.17.1-x86_64-linux-gnu.tar.gz \
  -o /tmp/litecoin.tar.gz \
  && echo $(\
  curl -fsSL https://download.litecoin.org/litecoin-0.17.1/linux/litecoin-0.17.1-linux-signatures.asc | \
  grep litecoin-0.17.1-x86_64-linux-gnu.tar.gz | awk '{print $1}' \
  ) /tmp/litecoin.tar.gz | \
  sha256sum -c --strict - \
  && python3 /tmp/shasum.py \
  && tar -zxvf /tmp/litecoin.tar.gz -C /tmp/

FROM ubuntu:18.04
RUN useradd -ms /bin/false -u 1001 -U litecoin
COPY --from=packager --chown=litecoin:litecoin /tmp/litecoin-0.17.1/ /home/litecoin/
USER litecoin
CMD /home/litecoin/bin/litecoind