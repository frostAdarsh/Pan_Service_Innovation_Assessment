# Use an official, lightweight Node.js runtime as the base image
FROM node:18-alpine

# Set the working directory inside the container
WORKDIR /app

# Copy the package.json and package-lock.json files first
# This helps Docker cache the npm install step so builds are faster
COPY package*.json ./

# Install the frontend dependencies
RUN npm install

# Copy the rest of your React application code into the container
COPY . .

# Expose port 5173 (the default port Vite uses)
EXPOSE 5173

# Command to start the Vite development server
# The "--host 0.0.0.0" flag is strictly required so Docker can expose it to your local browser
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]