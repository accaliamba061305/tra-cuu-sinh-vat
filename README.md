# tra-cuu-sinh-vat
A biological creature lookup website.

## Overview
This is a website where people can type in the animals they want to know more about to find relevant information (depending on whether the website features that creature) and learn more about biological creatures. I designed it (or hope that it is) to be comprehensible for people of all ages.

## The idea 
Actually, this was not the original idea when I had to do the CS50x final project. About 2 months earlier, I volunteered at Vietnam National Museum of Nature. After that, I became interested in coding and began with HTML. That was when I came up with the idea of this website (I remember thinking, rather naively, ‘Why doesn't a nature museum have a proper website where people can look up the creatures they see?’). With some of my knowledge, I built an html page and left it to gather dust (because I had to study for the high school entrance exam). When doing the final project, I just took it and decided to continue.

## Features
This version of this website:
- can be used by vietnamese and foreigners (the website is bilingual)
- can be used on computers, ipads, and phones. 
- has some iconic creatures for users to experience
- has a simple search bar so people can look up the creature they want to learn more about
- can edit creature data (using authentication via password for safety) by adding creatures, changing the data of the creatures, and deleting a creature.

## Technology stack
- html, css, javascript (super minimal)
- flask
- sqlite3

## project structure
index.html and index-en.html (to differentiate between english and vietnamese)
contact page and about page so people can contact me or understand what on earth is this website for.
on the contact page (only on the vietnamese one), there is a link "them sinh vat" to change the database. However, not everybody can access it. They have to insert the correct password to continue to the CRUD pages.

## How it works
The website uses separate templates for Vietnamese and English pages. Flask and Jinja templates are used to render the appropriate page and database content for each language. I had to look up on some official flask websites to learn how to use sqlite in flask (because, as a matter of fact, I want to take off the cs50 wheel, so without db.execute, life is a bit more complicated)

## authentication
I learned that I could store my local secret in a .env file, use load_dotenv() to load it, and add .env to .gitignore. This prevents the password from being accidentally committed to GitHub. On Render, I can configure the corresponding secret as an environment variable instead.

## Files and Project Structure

### `app.py`

Flask application, routes, database operations,
authentication, search, CRUD...

### `animals.db`

SQLite database contains species' names in both vietnamese and english, their scientific name, scientific taxonomy and a short paragraph. Especially, there is a whole table just for images, including the authors, sources, license, and alt_text for accessibility.

### `static/`
This is the folder which contains css, javascript, and images for the website

#### `styles.css`

styling my website with code 

#### `script.js`

Actually, I did not spend lots of time doing javascipt; hence, there is below 10 lines of javascript

#### `images/`

Where the images of the animals are stored

### `templates/`
This folder contains two sub-folders: en and vi (english and vietnamese) where I stored html templates.

#### `templates/vi/`

All vietnamese templates

#### `templates/en/`

All english templates

#### `templates/vi/change-database/`

Only vietnamese pages (specifically the contact page) has the CRUD pages.

### `requirements.txt`

To note that this website use these tools.

### `ideas.txt`

Where I store my ideas and plans

## CSS design
Admittedly, when I created the html file, I was too curious to see my website when it had css on it, so the first version of css of my website was AI's. However, when doing the final project, I decided to learn CSS from scratch (and also because cs50 said I should be most responsible) by asking AI each selector and its properties inside it and how they work together. Thanks to that method, I was able to learn CSS and wrote 532 lines of CSS in just two days, rather than dying in the freecodecamp css course. Whenever AI helped me directly or I copied AI-generated code, I commented on it in the source code to indicate where it was used.

## Future improvements
- Maybe I will use postgresql instead of sqlite.
- I will improve my search bar by using jsonify() and levenshtein distance
- Improve the security and authentication process of the website.

## Deployment

## Credits
I used mostly ChatGPT, and sometimes Gemini when ChatGPT reached its usage limit.
I also used the museum's logo. As I said, this is only my personal project, which I just wanted to create a creature lookup website so that when this is good enough, I can give it to the museum, but as a matter of fact, it is a long way to go. The museum logo used in this project is based on the logo of the Vietnam National Museum of Nature. The logo and the museum's name are not my property. This is an independent personal project and is not an official website of, nor affiliated with or endorsed by, the Vietnam National Museum of Nature.



## Resources
This might be not necessary, but I still mention it, just in case.
- https://ingiacong.co/bang-code-mau/
- https://flask.palletsprojects.com/en/stable/
- https://www.programiz.com/css?utm_source=programiz.com&utm_medium=referral&utm_audience=ORGANIC-FREEMIUM&- utm_campaign=course_promotion&utm_content=interests_learn_css&utm_term=nav_tutorials_banner

- I used this to learn and make css for the final project:
+ https://www.codechef.com/html-online-compiler

## AI
AI in this final project acted as a teacher, tutor, companion so that I can chat and discuss ideas (because otherwise I would completely mess everything up and it might take me a whole next month just to debug everything properly). However, ultimate decisions were mine and it is true for most of my code in the project.

note: AI hinted the structure of this readme.md as well.

## Author
My name is Dao Hai Long and I am 15 years old. I live in Hanoi, Vietnam