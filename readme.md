# CS50 Discogs Collection Viewer

This is a web application that allows you to view and explore a Discogs collection folder.
It can retrieve data from the Discogs API and stores it in a local SQL folder - vinyl_records.db
It also randomly selects an entry in the specified Discogs collection folder and displays artist, title, sleeve artwork and tracklist of that random selected record.

### Features
On launch the app randomly selects a release from the collection folder to provide a varied listening experience, clicking on the displayed table, reloads the table but this time clicking on any track loads the lyrics for that track from genius.com.
It displays the Cover Image, Artist Name, Album Title, Year of Release, Label, Genre and the tracklist for the randomly selected release each page allows you to choose another random selection by clicking the **Random Pick** button on the Navigation Bar.
Clicking on **Full Collection** on the Navigation Bar displays a table of releases containing basic information - Cover Image, Artist Name, Album Title, Year of Release, Label, Genre - about each release in the selected Discogs folder.
Clicking on **Update Database** calls the Discogs API and checks for any new additions to to be inserted into the SQL database, when the update is complete the new collection page will be displayed
Clicking on **Rebuild Database** is the nuclear option and deletes all rows in the table albums and resets the SQL_sequence too, it then accesses the Discogs API and inserts all the albums in the selected folder.
Alongside every cover image are two buttons, the **Delete Album** button removes the entry from the SQL database, whilst the **Wiki Discography** button attempts to access the relevant Wikipedia page.
Clicking on an **album title** will load the album page, where again each tracks lyrics can be loaded and clicking on the **artist name** loads all the uk lp releases logged in the discogs database
Clicking on an albums track will search for and load the tracks lyrics from Genius .com

### Technologies Used
Python,
Flask,
SQL.
html,
CS50

### Getting Started
If you wish to access your own record collection, you can clone this repository: https://github.com/Cundell66/discogs_py.git. You will need to get a Discogs API token by signing up for a free Discogs account at discogs.com and your own genius api token which is again free from genius.com. You will need to identify the folderID for the discogs folder you wish to access.
Then, create a .env file in the root directory and store your token, username and folder ID. Example:
discogsToken = "AAaAaAaAAAaaaaaaaAAAaAaaaAAaaAAaaaaAAaaa"
userName = "jackBauer"
folderID = 1111111
genius_token = "nzGzBS3wLbe_REP0kuKF7RR2wSQacLUgNVpK004qMsjMFf9r009N3oePiUek6VX4"


### Limitations:
Despite storing album info at a local level the cover images are still held on Discogs servers - this can lead to them failing to load or at the least being very slow.
The Genius search can only be conducted by the artist name attached to the album for example compilation albums like the Now series will get a search for Various which will return nothing.