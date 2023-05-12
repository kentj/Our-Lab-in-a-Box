#base image
FROM guacamole/guacamole

RUN whoami

#Add the root CA
COPY DC-Lab-CA.pem rootCA.pem

USER root

RUN keytool -import -trustcacerts -alias dc-lab-root -file rootCA.pem -keystore /opt/java/openjdk/jre/lib/security/cacerts -noprompt -keypass changeit -storepass changeit


