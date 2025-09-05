from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "chave_secreta_super_segura"  # Troque por algo mais forte

# Pergunta fixa
question = {
    "text": "A Terra é o terceiro planeta a partir do Sol.",
    "answer": True
}

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        name = request.form.get("name")
        if name:
            session["user"] = name
            session["score"] = 0
            session["answered"] = False
            return redirect(url_for("quiz"))
    return render_template("login.html")

@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    if "user" not in session:
        return redirect(url_for("login"))

    feedback = None
    if request.method == "POST" and not session.get("answered", False):
        choice = request.form.get("choice")
        if choice:
            user_answer = True if choice == "true" else False
            if user_answer == question["answer"]:
                session["score"] += 1
                feedback = "✔ Você acertou!"
            else:
                feedback = "✖ Você errou!"
            session["answered"] = True

    return render_template(
        "quiz.html",
        user=session["user"],
        score=session["score"],
        question=question,
        feedback=feedback,
        answered=session.get("answered", False)
    )

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))