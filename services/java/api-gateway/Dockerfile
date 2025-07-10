# services/java/api-gateway/Dockerfile
# Stage 1: Build the application
FROM gradle:jdk17-focal AS build
LABEL authors="surivarapuashwin"
WORKDIR /app
COPY gradlew .
COPY gradle gradle
COPY build.gradle .
COPY settings.gradle .
COPY src src
RUN gradle bootJar

# Stage 2: Create the final image
FROM openjdk:17-jdk-slim
WORKDIR /app
COPY --from=build /app/build/libs/*.jar app.jar
EXPOSE 8080
ENTRYPOINT ["java", "-jar","app.jar"]