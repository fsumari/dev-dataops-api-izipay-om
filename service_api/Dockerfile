
# Start from a base image
FROM python:3.11

ENV PYTHONUNBUFFERED True
#ENV PATH="/root/.local/bin:${PATH}"

# Set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt requirements.txt

# Install the required packages
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Expose the app port
# EXPOSE 80
ENV PORT=80
EXPOSE $PORT

COPY . ./
# Run command
# CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", $PORT]
CMD exec uvicorn main:app --host 0.0.0.0 --port ${PORT}
