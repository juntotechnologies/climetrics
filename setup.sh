mkdir -p ~/.streamlit/
echo "[general]  
email = \"mikaelmoise00@gmail.com""  > ~/.streamlit/credentials.toml
echo "[server]
headless = true
port = $PORT
enableCORS = true"  >> ~/.streamlit/config.toml