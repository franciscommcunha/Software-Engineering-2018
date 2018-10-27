FROM tomcat:latest

EXPOSE 8080
EXPOSE 5432
EXPOSE 5555

USER root

##PERMITS ACCESSING TOMCAT MANAGER FROM OUTSIDE
ADD context.xml /usr/local/tomcat/webapps/manager/META-INF/context.xml

##JDBC CONTEX
ADD contextApp.xml /usr/local/tomcat/conf/context.xml

ADD postgresql-8.2-506.jdbc4.jar /usr/local/tomcat/lib/

##FILE RESULTED FROM DASHBOARD BUILD (OUTSIDE SOCKER)
ADD admin-starter.war /usr/local/tomcat/webapps/admin-starter.war

##FILE WITH TOMCAT MANAGER
ADD tomcat-users.xml /usr/local/tomcat/conf/tomcat-users.xml

CMD ["catalina.sh","run"]


