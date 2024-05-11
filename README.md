# Recipe-Microservice

## Overview

This project is a microservice that provides endpoints for retrieving recipes.

## Features

- Retrieve Recipes

## Usage

1. Clone the repository:

   ```bash
   git clone <https://github.com/avd1729/Recipe-Microservice>
   ```

2. Navigate to the project directory:

   ```bash
   cd Recipe-Microservice
   ```

3. Build the Docker image:

   ```bash
   docker build -t recipes .
   ```

4. Run the Docker container:

   ```bash
   docker run -p 5001:5001 recipes
   ```

### Endpoints

GET /recipes: Retrieve all recipes.
