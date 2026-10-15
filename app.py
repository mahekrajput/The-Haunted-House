import os

from flask import Flask, abort, redirect, render_template, request, session, url_for

app = Flask(__name__)
app.secret_key = os.environ.get(
    "FLASK_SECRET_KEY",
    "local-development-key-change-before-deployment",
)

SCENES = {
    "hallway": {
        "title": "The Hallway",
        "story": (
            "A letter written in your own handwriting warned you not to enter "
            "this abandoned manor. Now the front door has shut behind you, and "
            "a voice whispers, \"You came back.\" A staircase creaks upstairs. "
            "A closed door whispers your name."
        ),
        "choices": [
            {"id": "investigate_staircase", "label": "Investigate the staircase", "next": "portrait"},
            {"id": "open_closed_door", "label": "Open the closed door", "next": "study"},
        ],
        "art_label": "A shadowy manor hallway",
    },
    "portrait": {
        "title": "The Living Portrait",
        "story": (
            "The portrait's painted face changes, slowly taking on your features. "
            "It reveals a brass key hidden behind its frame."
        ),
        "choices": [
            {"id": "continue_to_portrait_secret", "label": "Continue", "next": "portrait_secret"},
        ],
        "art_label": "An old portrait in a dim room",
    },
    "study": {
        "title": "The Whispering Study",
        "story": (
            "An old diary lies open on the desk. Its pages reveal that the house "
            "remembers every visitor's choices."
        ),
        "choices": [
            {"id": "continue_to_diary_warning", "label": "Continue", "next": "diary_warning"},
        ],
        "art_label": "An old diary in a shadowy study",
    },
    "portrait_secret": {
        "title": "The Portrait's Secret",
        "story": (
            "The house offers to reveal why it knows you, but asks you to leave "
            "the key behind."
        ),
        "choices": [
            {"id": "trust_house", "label": "Trust the house", "next": "truth"},
            {"id": "keep_key", "label": "Keep the key", "next": "escape"},
        ],
        "art_label": "A portrait watches from the darkness",
    },
    "diary_warning": {
        "title": "The Diary's Warning",
        "story": (
            "The diary reveals a hidden exit. The house begs you to stay and "
            "become part of its memories."
        ),
        "choices": [
            {"id": "follow_exit", "label": "Follow the exit", "next": "escape"},
            {"id": "answer_house", "label": "Answer the house", "next": "house_wins"},
        ],
        "art_label": "A diary beside a hidden doorway",
    },
    "escape": {
        "title": "The Escape",
        "story": "You escape, but a new letter is waiting outside.",
        "choices": [],
        "ending": True,
        "art_label": "A letter waiting outside the manor",
    },
    "house_wins": {
        "title": "The House Wins",
        "story": "The doors disappear. The manor has decided you belong there.",
        "choices": [],
        "ending": True,
        "art_label": "The manor's doors have disappeared",
    },
    "truth": {
        "title": "The Truth",
        "story": "You discover that the house has been preserving your forgotten past.",
        "choices": [],
        "ending": True,
        "art_label": "A forgotten memory inside the manor",
    },
}

@app.route("/")
def home():
    return render_template("home.html")


@app.post("/start")
def start_game():
    session.clear()
    session["current_scene"] = "hallway"
    session["choices"] = []
    return redirect(url_for("game"))


@app.get("/game")
def game():
    scene_id = session.get("current_scene")
    if scene_id not in SCENES:
        return redirect(url_for("home"))

    scene = SCENES[scene_id]
    return render_template(
        "game.html",
        title=scene["title"],
        story_text=scene["story"],
        choices=scene["choices"],
        ending=scene.get("ending", False),
        art_label=scene["art_label"],
    )


@app.post("/choose")
def choose():
    scene_id = session.get("current_scene")
    if scene_id not in SCENES:
        return redirect(url_for("home"))

    scene = SCENES[scene_id]
    choice_id = request.form.get("choice")
    selected_choice = next(
        (choice for choice in scene["choices"] if choice["id"] == choice_id),
        None,
    )
    if selected_choice is None:
        abort(400, description="That choice is not available in this scene.")

    choice_history = session.get("choices", [])
    session["choices"] = choice_history + [
        {"scene": scene_id, "choice": selected_choice["id"]}
    ]
    session["current_scene"] = selected_choice["next"]
    return redirect(url_for("game"))


@app.post("/play-again")
def play_again():
    session.clear()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)