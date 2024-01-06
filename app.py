import os
import markdown
import codecs
from pymongo_get_database import get_database
from bson.objectid import ObjectId
import random
from flask import Flask, render_template, request, redirect
# from cs50 import SQL
import requests

app = Flask(__name__)

dbname = get_database()
db = dbname["albums"]

# import secrets from .env which is not on github
app.config.from_pyfile("settings.py")
discogsToken = os.environ.get("discogsToken")
discogsName = os.getenv("discogsName")
folderID = os.environ.get("folderID")
geniusToken = os.environ.get("geniusToken")

totalItems = 355

# set urls for required routes
discogsURL = f"https://api.discogs.com/users/{discogsName}/collection/folders/{folderID}/releases?token={discogsToken}"
masterURL = "https://api.discogs.com/masters/"


def fetchAllContents():
    # Get the total number of pages
    response = requests.get(discogsURL).json()
    totalPages = response["pagination"]["pages"]

    allContents = []

    # Fetch all pages
    for page in range(1, totalPages + 1):
        response = requests.get(discogsURL + "&page=" + str(page)).json()
        releases = response["releases"]
        # Fetch and store details for each release
        for release in releases:
            contents = release["basic_information"]
            if contents["year"] == 0:
                idNumber = contents["master_id"]
                master = requests.get(
                    masterURL + str(idNumber) + "?token=" + discogsToken
                ).json()
                contents["year"] = master["year"]
            allContents.append(contents)
    return allContents

@app.route("/", methods=["GET", "POST"])
def home():
        albums = db.find().sort({"artist":1})
        return render_template("collection.html", albums=albums, title = "Full Collection")


@app.route("/update", methods=["GET"])
def update():
    try:
        allcontents = fetchAllContents()
        for i in range(len(allcontents)):
            contents = allcontents[i]
            release_id = contents["id"]
            existing_album = db.count_documents({"release_id": release_id})
            if existing_album == 0:
                print("release id: ", release_id, "added", contents["title"])
                db.insert_one({
                    "artist":contents["artists"][0]["name"], 
                    "artist_id":contents["artists"][0]["id"], 
                    "title":contents["title"], 
                    "year":contents["year"], 
                    "description":",".join(contents["formats"][0]["descriptions"]), 
                    "cover_image":contents["cover_image"], 
                    "genres": contents["genres"][0], 
                    "label":contents["labels"][0]["name"], 
                    "release_id":contents["id"], 
                    "master_id":contents["master_id"]
                    }
                )
        return redirect("/collection")
    except Exception as e:
        return render_template("error.html", title=e)

@app.route("/rebuild", methods=["GET"])
def rebuild():
    try:
        db.drop("albums")
        return redirect("/update")
    except Exception as e:
        return render_template("error.html", title=e)

@app.route("/collection", methods=["GET"])
def collection():
    albums = db.find().sort({"artist":1})
    return render_template("collection.html", albums=albums, title = "Full Collection")

@app.route("/random_pick", methods=["GET"])
def random_pick():
    count = db.estimated_document_count() - 1
    if count < 1:
        return redirect("/update")
    else:
        number = random.randint(0, count)
        album = db.find().skip(number).limit(1)
        return render_template("collection.html", albums=album, title="Random")

@app.route("/about", methods=["GET"])
def about():
    with codecs.open("readme.md", "r", encoding="utf-8") as readme_file:
        readme_content = readme_file.read()
    content = markdown.markdown(readme_content)
    return render_template("about.html", content=content)


@app.route("/delete", methods=["POST"])
def delete():
    album_id = request.form.get("id")
    album_delete = {"_id": ObjectId(album_id)}
    try:
        db.delete_one(album_delete)
        return redirect("/collection")
    except Exception as e:
        return render_template("error.html", title=e)


@app.route("/lyrics", methods=["POST"])
def lyrics():
    bad_chars = [";", ":", "-", "!", "*", ",", "'","&"]
    artist = request.form.get("artist")
    title = request.form.get("title")
    a = ""
    for i in artist:
        if i not in bad_chars:
            a += i
    t = ""
    for i in title:
        if i not in bad_chars:
            t += i
    search_url = f"https://api.genius.com/search?q={a.replace(' ','-')}-{t.replace(' ','-')}"
    headers = {"Authorization": f"Bearer {geniusToken}" }
    response = requests.get(search_url, headers=headers)
    data = response.json()
    if data['response']['hits']!=[]:
        api_path = data['response']['hits'][0]['result']['api_path']
        song_url = f"https://api.genius.com{api_path}"
        song_response = requests.get(song_url, headers=headers)
        song_data = song_response.json()
        content = song_data['response']['song']['embed_content']
        return render_template("lyrics.html", content=content, artist=artist, title=title)
    else:
        content = f"Sorry, {title} by {artist} is not in the database"
        return render_template("lyrics.html", content=content, artist=artist, title=title)


@app.route("/artist", methods=["POST"])
def artist():
    artist = request.form.get("artist")
    discogsURL = f"https://api.discogs.com/database/search?format=lp&artist={artist}&country=uk&token={discogsToken}"
    releases = requests.get(discogsURL).json()
    releases["results"].sort(
        key=lambda x: int(x["year"])
        if "year" in x and x["year"].isdigit()
        else float("inf")
    )
    # Filter the releases to return each title only once
    titles = set()
    unique_releases = []
    for release in releases["results"]:
        if release["title"] not in titles:
            titles.add(release["title"])
            unique_releases.append(release)

    return render_template("artist.html", releases=unique_releases, artist=artist)


@app.route("/tracks", methods=["POST"])
def tracks():
    artist = request.form.get("artist")
    cover = request.form.get("cover")
    title = request.form.get("title")
    idNumber = request.form.get("master_id")
    master = requests.get(masterURL + str(idNumber) + "?token=" + discogsToken).json()
    tracklist = master["tracklist"]
    return render_template("tracks.html", tracks=tracklist, title=title, cover=cover, artist=artist)

@app.route("/search", methods=["POST"])
def search():
    q = request.form.get("q").lower()
    print(q)
    try:
        if q:
            albums = db.find({"artist":{"$regex": q, "$options": "i"}}).sort({"year":1})
        else:
            albums = []
        return render_template("collection.html", albums=albums, title = f"search for {q}")
    except Exception as e:
        return render_template("error.html", title=e)

@app.route("/wiki", methods=["POST"])
def wiki():
    artist = request.form.get("artist")
    url = f"https://www.wikipedia.com/wiki/{artist}_discography"
    return redirect(url)
