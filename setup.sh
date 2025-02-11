PORT=${PORT:-8501} 
mkdir -p ~/.streamlit/

echo "[general]
email = \"mikaelmoise00@gmail.com\"" > ~/.streamlit/credentials.toml

echo "[server]
headless = true
port = $PORT
enableCORS = false" >> ~/.streamlit/config.toml
