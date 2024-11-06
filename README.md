# Event Manager Backend
This repository is the backend of and event manager web aplication, this app allow us, create user with authentication implementing OAuth2 and JWT, there are two types of users, admin user and normal user, the admin user can create and manage events and can manage users too. On the other hand the normal users can make a participation request and can add products to show other users.

To run this project follow the next steps:

1. First of all you need to run the sql script in postgres, you can open it with pgAdmin4 or execute from shell

2. Just execute this command (you need to have docker installed and running yet):
    > `docker-compose up -d --build`

To execute testing, execute the next command:
    > `docker-compose exec web pytest`