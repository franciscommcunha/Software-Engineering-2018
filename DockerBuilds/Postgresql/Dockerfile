FROM postgres

ENV POSTGRES_USER postgres
ENV POSTGRES_PASSWORD secret
ENV POSTGRES_DB domotics

ADD domotics_tables.sql /docker-entrypoint-initdb.d/

ADD updateConf.sh /docker-entrypoint-initbd.d

ADD postgres.conf /ect/postgresql/postgresql.conf

EXPOSE 5432

#CMD ['-c', 'listen_addresses="*"']

