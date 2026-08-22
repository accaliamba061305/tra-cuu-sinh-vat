# tra-cuu-sinh-vat
A bilingual biological creature lookup website.

## Overview
This is a website for looking up information about biological creatures. Users can search for supported species and view information such as common names, scientific names, taxonomy, descriptions, and images.
The website supports both Vietnamese and English and is designed to work across desktop and mobile devices.

## Features
This version of this website:
- supports both Vietnamese and English
- has responsive design for computers, iPads, and phones. 
- has some iconic creatures for users to explore
- has a simple search bar so people can look up the creature they want to learn more about
- can edit creature data (using authentication via password for safety) by adding creatures, changing the data of the creatures, and deleting a creature.

## Technology stack
- HTML
- CSS
- JavaScript
- Flask
- SQLite

## Files and Project Structure

### `app.py`
The main Flask application containing routes, database operations, authentication, search functionality, and CRUD functionality.

### `animals.db`

The SQLite database containing creature information in Vietnamese and English, scientific names, taxonomy, descriptions, and image metadata.

### `static/`
Contains CSS, JavaScript, and images for the website

### `templates/`
Contains separate folders for Vietnamese version and English version of Jinja templates

#### `templates/vi/change-database/`
Only the vietnamese version (specifically the contact page) has the CRUD pages.

### `requirements.txt`
Lists the Python dependencies required by the application.

### `ideas.txt`
Contains initial notes and ideas

## How it works
The website uses separate templates for Vietnamese and English pages. Flask and Jinja templates are used to render the appropriate page and database content for each language.

When a user visits the website, Flask handles the request and determines which page should be displayed. The corresponding Jinja template is then rendered and inserted with information retrieved from the SQLite database.

The creature data is stored in animals.db. Each creature can have information such as its Vietnamese name, English name, scientific name, taxonomy, description, and related image information. The application uses this database to search for creatures and display their information on the appropriate page.

The search bar allows users to enter the name (or the scientific one) of a creature and look for matching records in the database. If a supported creature is found, the website displays its available information. If there is no matching creature, the website informs the user that the creature could not be found.one

The website also contains a separate database-management area. This area is protected by password authentication and allows authorized users to add new creatures, edit existing information, or delete records from the database.

For the bilingual interface, the same underlying database is used for both languages. The Vietnamese and English templates determine how the available information is presented to the user.

The frontend is built with HTML and CSS, with a small amount of JavaScript for client-side functionality. Flask connects the frontend to the database and handles the application's server-side logic.

## Authentication
The database-management functionality is protected by password authentication.

The local secret is stored in a .env file and excluded from version control using .gitignore. In deployment, the corresponding secret is configured as an environment variable.

## CSS design
The website uses custom CSS for layout, responsive design, navigation, forms, cards, and other interface elements.
During development, I used AI as a learning and debugging aid to understand CSS selectors, properties, and their interactions. Where AI-generated code was directly incorporated into the project, I documented its use in the source code.

## Future improvements
- Change to PostgreSQL instead of SQLite.
- Improve my search functionality by using jsonify() and Levenshtein distance
- Improve the security and authentication process of the website.

## Deployment
The application is deployed online for testing.

## Credits
This is an independent personal project and is not affiliated with or endorsed by the Vietnam National Museum of Nature.

The project uses the museum's logo for illustrative purposes. The logo and museum name remain the property of the Vietnam National Museum of Nature.

## Resources
- Hexidecimal color code table: https://ingiacong.co/bang-code-mau/
- Flask documentation: https://flask.palletsprojects.com/en/stable/
- Programiz CSS tutorial: https://www.programiz.com/css?utm_source=programiz.com&utm_medium=referral&utm_audience=ORGANIC-FREEMIUM&- utm_campaign=course_promotion&utm_content=interests_learn_css&utm_term=nav_tutorials_banner
- Codechef HTML online compiler: https://www.codechef.com/html-online-compiler
- w3schools: https://www.w3schools.com/

## AI
AI tools were used during development as a learning, debugging, and development aid.

For this Final Project, AI was used to discuss implementation ideas, explain technical concepts, identify bugs, and assist with parts of the development process. Where AI-generated code was directly incorporated, its use is documented in the relevant source code.

note: AI was also used to help structure this README.

## Author
My name is Dao Hai Long.