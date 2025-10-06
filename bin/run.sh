#!/bin/bash

pip install --no-cache-dir -r requirements.txt
streamlit run --server.headless true ./scripts/main.py
