# Dockerfile for Flask application
FROM  python:3.12-slim

#Install rquired packages and add user
RUN apt-get update && \
    apt-get install git -y && \
    useradd --create-home --no-log-init -u 1000 akm

# Switch to the non-root user and set the working directory
WORKDIR /app

# Copy the application files and install dependencies
COPY requirements.txt .

RUN --mount=type=secret,id=gitcredentials,dst=/root/.git-credentials \
    git config --global credential.helper store && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the application port and set the default command
EXPOSE 9000
ENV FLASK_APP=app
CMD ["python3", "app.py"]