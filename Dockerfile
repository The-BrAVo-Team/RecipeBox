# Use a Debian-based image with Node.js and Python
FROM node:14-alpine

# Set the working directory
WORKDIR /RecipeBox

# Copy Python requirements file
COPY requirements.txt .

# Install Python and pip
RUN apk add --no-cache python3 py3-pip \
    && ln -sf python3 /usr/bin/python \
    && ln -sf pip3 /usr/bin/pip 


# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY ./client/package-lock.json /RecipeBox/client/package-lock.json

# Install Node.js dependencies
RUN (cd client; npm install)

COPY . .

# Set the entry point or provide any other necessary instructions
CMD ["python", "app.py"]