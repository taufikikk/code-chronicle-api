from app import create_app, db
import models

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {"db": db, "models": models}


if __name__ == "__main__":
    app.run(debug=True, port=5001)
