#!/bin/bash

# Define the path to your .env file
ENV_FILE="./.env"

# Check if the .env file exists
if [ -f "$ENV_FILE" ]; then
  # Read the .env file line by line
  while IFS= read -r line; do
    # Skip comments and empty lines
    if [[ "$line" =~ ^\s*#.*$ || -z "$line" ]]; then
      continue
    fi

    # Split the line into key and value
    key=$(echo "$line" | cut -d '=' -f 1)
    value=$(echo "$line" | cut -d '=' -f 2-)

    # Remove quotes and trim whitespace from the value
    value=$(echo "$value" | sed -e "s/^'//" -e "s/'$//" -e 's/^"//' -e 's/"$//' -e 's/^[ \t]*//;s/[ \t]*$//')

    # Export the key and value as environment variables
    export "$key=$value"
  done < "$ENV_FILE"
  echo "Environment variables loaded from $ENV_FILE."
else
  echo "Warning: $ENV_FILE not found. No environment variables loaded."
fi

docker run --net=host -it -e NGROK_AUTHTOKEN=$NGROK_AUTHTOKEN ngrok/ngrok:latest http --url=nonmeteorological-challengingly-bodhi.ngrok-free.dev 8501

