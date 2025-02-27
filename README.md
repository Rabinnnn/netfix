# Netfix

## Table of Contents
- [Description](#description)
- [Installation Instructions](#installation-instructions)
- [Usage](#usage)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Contact Information](#contact-information)

## Description
Netfix is a web application designed to manage services, allowing users to request and manage various services efficiently. It is a B2C platform where companies can create account and post the services that they provide. The customer can then view all the availble services from all companies and make a request for the service they require.

## Installation Instructions
1. Clone the repository and navigate to the directory:
   ```bash
   $ git clone https://learn.zone01kisumu.ke/git/somulo/netfix.git
   $ cd netfix
   ```
2. Install the required dependencies:
   ```bash
   $ pip install -r requirements.txt
   ```
3. Apply migrations:
   ```bash
   $ python manage.py makemigrations
   $ python3 manage.py migrate
   ```
4. Run the development server:
   ```bash
   python3 manage.py runserver
   ```

## Usage
Access the application by navigating to `http://127.0.0.1:8000/` in your web browser.

## Features
- Account creation and user authentication.
- Service management(creation and request of services).
- Request status tracking(the company can accept or cancel a pending service request).
- Service request history (customer can view all service requests they've made).
- Most requested services(company can view the most requested services).

## Technologies Used
- Django
- SQLite
- HTML/CSS
- JavaScript

## Contact Information
For questions or feedback, please reach out to:

- **Samuel Omulo**  
  GitHub: [somulo1](https://github.com/somulo1)

- **Rabin Otieno**  
  GitHub: [rabinnnn](https://github.com/rabinnnn)

## License
This is an opensource project licensed under the MIT License. See the LICENSE file for details. If you'd like to contribute, create a branch then create a pull request after making the changes.
