# hw6-Anna-Mikhaleva
Homework №6.
Unfortunately, I couldn't install docker on my version of Windows. Therefore, this task was performed in Kali Linux.

## What I already have after task #5
1. Flask web application, which can authenticate user with password:
1. Listen on localhost:5000
1. Render authentication form on http://localhost:5000/
1. Return static images and files on http://localhost:5000/static/<image_name>
1. Has secret page for authenticated users on http://localhost:5000/cabinet
1. Valid usernames and passwords are stored in MongoDB database
1. Image upload function in cabinet http://localhost:5000/cabinet/
1. Images are being saved to upload folder

## Basic part:
1. Create docker-compose.yml and Dockerfile to run your application in Docker
1. Move your sources to src directory. Don’t forget to create requirements.txt file
1. In docker-compose.yml there are gonna be two containers named: mongodb, flask-simple
1. Setup port forwarding and run docker-compose up. Check that website works on http://localhost:5000


_You can find it in HW6 folder_
