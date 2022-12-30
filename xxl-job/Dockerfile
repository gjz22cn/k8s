FROM openjdk:8-jre-slim

ADD xxl-job-admin-2.3.0.jar /xxl-job-admin.jar
ADD xxl-job-executor-sample-springboot-2.3.0.jar /xxl-job-executor-sample-springboot.jar
COPY docker-entrypoint.sh /

EXPOSE 30405 9999 9081
ENTRYPOINT ["/docker-entrypoint.sh"]
