from app import create_app
import webbrowser
from threading import Timer

def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000/")

app = create_app()

if __name__ == "__main__":
    Timer(1, open_browser).start()  # Open the browser after 1 second
    app.run(debug=True)
