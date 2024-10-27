# Maze Editor GUI Application
Version: 1.0

# Overview
Trailblazer, a Maze Editor GUI Application is a Tkinter-based tool that allows users to create, edit and solve mazes. It can be used for robotic path planning, R&D, and education. It also includes includes basic authentication with username and password validation, allowing secure access to the GUI.

# Features
**Maze Creation and Editing:** Create mazes using a simple GUI with start and finish points.

**Path Planning Algorithms:** Supports pathfinding algorithms (A*, Dijkstra, RRT currently implemented) to visualise solutions.

**Credential System:** Allows users to set up credentials with a hashed password storage for secure access.

**Password Requirements:** Passwords require numbers, special characters, and a minimum length of 14 characters.

**User Interface:** Easy-to-navigate screens for login, credential setup, and maze editing.


# Getting Started
**Prerequisites**

**Python:** Version 3.6 or higher

**Tkinter:** Standard Python library installation

# Installation
Clone or download this repository to your local machine.

Ensure that Python with Tkinter is installed.  


# Directory Structure

**mazeEditorTkinter.py:** The main GUI code for the maze editor.

**security.py:** Contains functions for authentication and password management.

**README.md:** Instructions for using the application.

**Algorithms Folder:** Holds all the implemented algorithms for the pathing of the mazes. Will dynamically update the GUI as more algorithms are saved.

**savedCourses Folder:** Holds all saved maze configurations, will dynamically update the import drop down menu as mazes are saved. 

**Icons Folder:** Holds all icons and textures used by the GUI.


# Usage

**Start the Application:** Run NewSecurity.py.

**Login or Set Up Credentials:**

New Users: Click "Set Credentials" to create a username and password. Follow the password requirements displayed on-screen.

Existing Users: Use "Login" to access the maze editor.


**Edit and Save Mazes:**
Use the GUI to draw walls, set start/finish points, and solve mazes.

Save your mazes for future use and load saved mazes as needed.

**Run Pathfinding Algorithms:**
Choose from available pathfinding algorithms to see the shortest or most efficient paths within the maze.


# Security
The application uses a basic hashing mechanism to secure passwords:

**Password Hashing:** Passwords are hashed using SHA-256 before storage.

**Password Validation:** The application enforces strong password requirements.
