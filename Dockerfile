FROM python:3.8

RUN python3 -m pip install requests

RUN mkdir -p /opt/gandi-dynamic-dns
ADD python/*.py /opt/gandi-dynamic-dns/
ADD python/api_url /opt/gandi-dynamic-dns/api_url
ADD docker-entrypoint.sh /opt/gandi-dynamic-dns/docker-entrypoint.sh

RUN chmod ugo+x /opt/gandi-dynamic-dns/docker-entrypoint.sh 

WORKDIR /opt/gandi-dynamic-dns
CMD ["/opt/gandi-dynamic-dns/docker-entrypoint.sh"]
