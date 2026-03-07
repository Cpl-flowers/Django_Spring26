# Agile Development Plan – Study Spot Finder

## Initiative
Develop a Django-based web application that helps university students find, reserve, and monitor study spaces across campus in real time. The system will allow students to view available study rooms, check crowd levels, reserve time slots, and locate study areas through an interactive map.

The goal of this initiative is to reduce the time students spend searching for study spaces and improve collaboration among study groups.

---

# Goal 1: User Account and Authentication System

Create a secure user account system that allows students to register, log in, and manage their study reservations.

## User Stories
- As a student, I want to create an account so that I can use the study reservation system.
- As a student, I want to log in and log out so that my reservations are secure.
- As a student, I want to view my reservations so I know when and where I am scheduled to study.

## Tasks
- Set up Django authentication system
- Create signup and login pages
- Create user profile system
- Store user data in the database
- Allow users to view their reservation history

## Sub-Goals (Stretch Goals)
- Profile customization
- Study history tracking
- Favorite study locations

---

# Goal 2: Study Spot Search System

Allow users to search and filter study locations across campus.

## User Stories
- As a student, I want to search study spots by campus or building so that I can find a convenient location.
- As a student, I want to filter study spots by noise level and seating availability so I can choose a comfortable study environment.
- As a student, I want to see available study spaces in real time so I don’t go to a full location.

## Tasks
- Create search bar on homepage
- Implement campus and building filters
- Connect search system to the study location database
- Display results dynamically

## Sub-Goals (Stretch Goals)
- Wi-Fi quality filter
- Power outlet availability filter
- Recommended study spots

---

# Goal 3: Room Reservation System

Allow students to reserve study rooms for specific time periods.

## User Stories
- As a student, I want to reserve a study room so my study group has a place to meet.
- As a student, I want to see existing reservations so I know which rooms are already booked.
- As a student, I want to cancel a reservation if my plans change.

## Tasks
- Create reservation database model
- Implement reservation form
- Display room availability
- Prevent double booking of rooms
- Allow reservation cancellation

## Sub-Goals (Stretch Goals)
- Recurring reservations
- Group reservation invites
- Reservation reminders

---

# Goal 4: Study Spot Map and Crowd Monitoring

Allow users to visually locate study spots and report crowd levels.

## User Stories
- As a student, I want to view study spots on a map so I can easily find them on campus.
- As a student, I want to report crowd levels so other students know if a location is busy.
- As a student, I want crowd reports to expire automatically so outdated information is removed.

## Tasks
- Integrate campus map interface
- Add map markers for study locations
- Implement crowd level reporting system
- Store and display crowd data
- Implement automatic expiration of reports

## Sub-Goals (Stretch Goals)
- Real-time map updates
- Color-coded crowd indicators
- Notifications when crowd levels change

---

# Agile Sprint Plan

## Sprint 1 – Project Setup
- Create Django project
- Setup database structure
- Implement user authentication
- Build basic homepage layout

## Sprint 2 – Search System
- Implement search bar
- Add campus and building filters
- Display available study spots

## Sprint 3 – Reservation System
- Implement room reservation feature
- Add time slot validation
- Display current reservations

## Sprint 4 – Map and Crowd Features
- Implement map interface
- Add crowd level reporting
- Implement report expiration system
