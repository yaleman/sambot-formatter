# wsgi.py

from formatter import app
# if you use a method to create the app instance,
# call the method here and set the return value to app variable.
if __name__ == "__main__":
    app.run()