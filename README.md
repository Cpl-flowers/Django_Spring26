# Django_Spring26
UTRGV Software Engineering Spring 2026 
by Arly Garcia, Angle Rizo, Kevin Flores

## Local setup

From the `testFolder` directory, run:

```powershell
..\..\virt\Scripts\python manage.py migrate
..\..\virt\Scripts\python manage.py loaddata fixtures\initial_data.json
..\..\virt\Scripts\python manage.py runserver
```

The `db.sqlite3` file is intentionally ignored because each teammate has their own local database. Shared starter data, such as buildings and rooms, should be updated in `testFolder/fixtures/initial_data.json` instead.

Do not commit `db.sqlite3`. It is a local database file and does not merge well between teammates.

If you add or edit shared `Building` or `Room` data locally and want the team to get the same base data, update the fixture with:

```powershell
..\..\virt\Scripts\python manage.py dumpdata testApp.Building testApp.Room --indent 2 --output fixtures\initial_data.json
```

Then commit and push the fixture file:

```powershell
git add testFolder/fixtures/initial_data.json
git commit -m "Update shared building and room data"
git push
```


Project Overview
	A Django web application that will help users find an available study spot and log the start/end times of a study session for a group of users. A user can make an account with the web page and request a study room for a given time slot at a specific location so that not only will the user reserve that time and location but so that other users understand as well what reservations have been made. The user will be provided with a timecard associated with a map to available room locations so that the user can interact and see in real time the availability of any given room at the current time of web app use. Users should be able to make reservations and cancel their appropriate reservations at any time within reason as well as be able to observe the current reservations made.
User Stories
-	Carly, I’m a user that is looking to reserve a room in the Engineering building for my study group so that I can finish a project before Friday midnight

-	Barly, I can’t find the room my group agreed on and get easily lost on campus looking for them

-	Charly, sometimes I go to study and the people around me are loud and can’t concentrate on my study material I wish I knew of a quieter location


1. Home Page Features
- Search Bar – Search by campus, building, floor, or room number. Include filters for quiet
level and available seating.
- Campus Selector Dropdown – Allows students to choose between multiple campuses.
- Quick Filter Buttons – Options like Available Now, Quiet, Low Crowd, Has Outlets, Good
Wi-Fi.
- Live Crowd Level Cards – Display popular study spots with crowd level and last updated
time.
- Report Button – Allows students to submit crowd level updates (Low / Medium / High)
with optional comments.
- Login / Sign Up – Students must create an account to use the app. Profile icon shown
after login.
 

2.Additional Features to Consider
- Study Spot Rating System – Students rate locations based on comfort, cleanliness, and
noise level.
- Time-Based Trends – Show typical busy or quiet hours using stored historical data.
- Map View – Display campus map with color-coded pins (Green = Empty, Yellow =
Moderate, Red = Full).
- Notifications – Alert users when a room becomes quiet or less crowded.
- Favorite Spots – Allow users to save preferred study areas.
- Admin Analytics Dashboard – Show peak hours, most used spots, and campus activity
statistics.
- Report Incorrect Info – Users can flag outdated or inaccurate reports.
- Auto-Expire Reports – Crowd updates automatically expire after 30–60 minutes.
