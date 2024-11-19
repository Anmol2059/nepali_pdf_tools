#!/bin/bash

# Environment name
ENV_NAME="pdf_extraction"
YML_FILE="environment.yml"

# Check if the environment already exists
if conda info --envs | grep -q "^$ENV_NAME"; then
    echo "Environment '$ENV_NAME' already exists. Activating it..."
    conda activate "$ENV_NAME"
else
    echo "Environment '$ENV_NAME' not found. Creating it from $YML_FILE..."
    if [ -f "$YML_FILE" ]; then
        conda env create -f "$YML_FILE"
        echo "Environment '$ENV_NAME' created successfully. Activating it..."
        conda activate "$ENV_NAME"
    else
        echo "Error: $YML_FILE not found. Please ensure the file exists in the current directory."
        exit 1
    fi
fi

# Run your application or script here
echo "Environment is active. Running the application..."
streamlit run app.py  # Replace 'app.py' with your Python script if different
