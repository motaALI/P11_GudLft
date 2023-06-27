import json
import os

from flask import Flask, flash, redirect, render_template, request, url_for

from services.booking_service_srv import (
    bookingError,
    check_club_possibility_to_reserve_places,
    check_reservation_not_in_past,
)


def loadClubs():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    clubs_file = os.path.join(current_dir, "clubs.json")
    with open(clubs_file) as c:
        listOfClubs = json.load(c)["clubs"]
        return listOfClubs


def loadCompetitions():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    competitions_file = os.path.join(current_dir, "competitions.json")

    with open(competitions_file) as comps:
        list_of_competitions = json.load(comps)["competitions"]
        return list_of_competitions


app = Flask(__name__)
app.secret_key = "something_special"

competitions = loadCompetitions()
clubs = loadClubs()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/showSummary", methods=["POST"])
def showSummary():
    club = None  # Assign a default value to 'club'
    try:
        club = [club for club in clubs if club["email"] == request.form["email"]][0]
        return render_template("welcome.html", club=club, competitions=competitions)
    except IndexError:
        # Email not found, display custom error message
        error_message = "Email not found"
        flash(error_message)
        return render_template("welcome.html", club=club, competitions=competitions)


@app.route("/book/<competition>/<club>")
def book(competition, club):
    foundClub = [c for c in clubs if c["name"] == club]
    foundCompetition = [c for c in competitions if c["name"] == competition]
    if not foundClub:
        flash("Club not found")
        return (
            render_template("welcome.html", club=club, competitions=competitions),
            404,
        )
    foundClub = foundClub[0]

    if not foundCompetition:
        flash("Competition not found")
        return (
            render_template("welcome.html", club=club, competitions=competitions),
            404,
        )

    foundCompetition = foundCompetition[0]

    if foundClub and foundCompetition:
        return (
            render_template(
                "booking.html", club=foundClub, competition=foundCompetition
            ),
            200,
        )
    else:
        flash("Something went wrong-please try again")
        return render_template("welcome.html", club=club, competitions=competitions)


@app.route("/purchasePlaces", methods=["POST"])
def purchasePlaces():
    competition = [c for c in competitions if c["name"] == request.form["competition"]]
    if competition:
        competition = competition[0]
    club = [c for c in clubs if c["name"] == request.form["club"]]
    if club:
        club = club[0]
    placesRequired = int(request.form["places"])
    try:
        check_club_possibility_to_reserve_places(club, placesRequired)
        check_reservation_not_in_past(competition["date"])
        competition["numberOfPlaces"] = (
            int(competition["numberOfPlaces"]) - placesRequired
        )

        # Deduct the number of points used from the club balance.

        club["points"] = int(club["points"]) - placesRequired
        club_points_report = f"You have {club['points']} points left."
        flash("Great-booking complete!")
        flash(club_points_report)
        return (
            render_template("welcome.html", club=club, competitions=competitions),
            200,
        )
    except bookingError as error:
        flash(error)
        return render_template("welcome.html", club=club, competitions=competitions)


# TODO: Add route for points display
@app.route("/clubsPoints", methods=["GET"])
def clubsPoints():
    return render_template("clubs.html", clubs=clubs)


@app.route("/logout")
def logout():
    return redirect(url_for("index"))
