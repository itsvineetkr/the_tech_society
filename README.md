# College Clubs Management System

## Overview
This project is a centralized platform designed to manage all the clubs, events, and registrations within a college. Built using Django REST Framework with basic HTML, CSS, and JavaScript, it provides a seamless experience for students, club admins, and site administrators to manage and participate in events from different clubs, all in one place.

## Features

### User Features:
- **User Signup & Authentication**: Students can create an account, log in, and manage their profiles, including details such as name, email, roll number, phone number, branch, and year.
- **Profile Management**: Students can update their personal information and reset their password using the password reset feature.
- **Event Participation**:
  - **Team Participation**: Students can create teams or send join requests to existing teams. Team leaders have control over accepting or rejecting team members.
  - **Individual Participation**: Students can register for events as individuals.
- **Event Filtering**: Users can filter and view events based on different clubs or other criteria, allowing them to find events of interest across the entire college.

### Admin Features:
- **Club Admin Assignment**: Site administrators can assign any student as a club admin. Each club admin can manage events and registrations for their respective club. 
NOTE: Club Assignment can be done via django admin pannel by editing user's data in CustomUser Model.
- **Event Management**: Club admins can create and delete events. (Edit details of any event will also be added in future.)
- **Registration Data Export**: Club admins can download registration data for events in their club for easier tracking and analysis.

### Team Registration:
- **Team Creation & Management**: Students must complete their profile before participating in team events. They can create teams for events, invite others, or accept/join team requests.
- **Team Joining**: Students can send join requests to existing teams, and team leaders can accept or reject these requests.

### Site Admin Features:
- **Manage Clubs & Events**: Site admins oversee the entire platform, including creating and managing clubs, assigning admins, and maintaining the overall system.


## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/itsvineetkr/the_tech_society.git
    cd the_tech_society
    ```

2. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Apply database migrations:
    ```bash
    python manage.py migrate
    ```

4. Create a superuser:
    ```bash
    python manage.py createsuperuser
    ```

5. Run the server:
    ```bash
    python manage.py runserver
    ```

6. Access the site on `http://localhost:8000/`.

## API Endpoints

This project is built using Django REST Framework, and the following are some core API endpoints:

## Technologies Used

- **Backend**: Django REST Framework
- **Frontend**: HTML, CSS, JavaScript
- **Database**: SQLite (default) / Any other relational database can be used