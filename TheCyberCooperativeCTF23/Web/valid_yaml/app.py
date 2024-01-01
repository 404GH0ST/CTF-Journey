#!/usr/bin/env python
import functools
import tempfile

from flask import Flask, redirect, render_template, request, session, url_for
from sqlalchemy.exc import IntegrityError

import yamale
from flask_bootstrap import Bootstrap
from models import Schemas, Users, db, hash_password, verify_password

app = Flask(__name__)
app.config.from_object("config.Config")
bootstrap = Bootstrap(app)

db.init_app(app)
with app.app_context():
    db.create_all()


def authed():
    user_id = session.get("id", None)
    return user_id is not None


def authed_only(f):
    @functools.wraps(f)
    def _authed_only(*args, **kwargs):
        if authed():
            return f(*args, **kwargs)
        else:
            return redirect(url_for("login", next=request.full_path))

    return _authed_only


@app.context_processor
def inject_user():
    if session:
        return dict(session)
    return dict()


@app.route("/", methods=["GET", "POST"])
def index():
    schemas = Schemas.query.all()
    if request.method == "GET":
        return render_template("index.html", schemas=schemas)
    elif request.method == "POST":
        schema_id = request.form["schema_id"]
        content = request.form["content"]

        schema = Schemas.query.filter_by(id=schema_id).first_or_404()
        schema = yamale.make_schema(content=schema.content)
        data = yamale.make_data(content=content)

        try:
            yamale.validate(schema, data)
        except ValueError as e:
            result = f"Validation failed: {str(e)}"
            return render_template(
                "index.html",
                schemas=schemas,
                success=False,
                result=result,
                content=content,
            )

        result = "Valid!"
        return render_template(
            "index.html", schemas=schemas, success=True, result=result, content=content
        )


@app.route("/admin/schemas", methods=["GET", "POST"])
@authed_only
def schemas():
    if request.method == "GET":
        schemas = Schemas.query.all()
        return render_template("schemas.html", schemas=schemas)
    elif request.method == "POST":
        name = request.form["name"]
        content = request.form["content"]
        schema = Schemas(name=name, content=content)
        db.session.add(schema)
        db.session.commit()
        return redirect(url_for("schema", schema_id=schema.id))


@app.route("/admin/schemas/<int:schema_id>", methods=["GET", "POST"])
@authed_only
def schema(schema_id):
    schema = Schemas.query.filter_by(id=schema_id).first_or_404()
    if request.method == "GET":
        return render_template("schema.html", schema=schema)
    elif request.method == "POST":
        name = request.form["name"]
        content = request.form["content"]
        schema.name = name
        schema.content = content
        db.session.commit()
        return redirect(url_for("schema", schema_id=schema.id))


@app.route("/logout")
@authed_only
def logout():
    session.clear()
    return redirect("/")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"].strip()
        errors = []

        user = Users.query.filter_by(username=username).first()
        if user:
            pass_test = verify_password(plaintext=password, ciphertext=user.password)
            if pass_test is False:
                errors.append("Incorrect password")
        else:
            errors.append("User does not exist")
            return render_template("login.html", errors=errors)

        if errors:
            return render_template("login.html", errors=errors)

        session["id"] = user.id
        return redirect("/")

    return render_template("login.html")


if __name__ == "__main__":
    app.run(debug=True, threaded=True)
