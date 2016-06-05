from cookbook import app, db

if __name__ == "__main__":
    app.config.from_object('config.DevelopmentConfig')
    # Because we did not initialize Flask-SQLAlchemy with an application
    # it will use `current_app` instead.  Since we are not in an application
    # context right now, we will instead pass in the configured application
    # into our `create_all` call.
    db.create_all(app=app)
    app.run()