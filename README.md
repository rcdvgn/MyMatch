# MyMatch (Beta)

[Video Demo](https://youtu.be/rnXpGqrKWYI)

## Introduction:

**MyMatch** is a Web Application that I, Ricardo Vigliano, started programming in the early days of my Software Development journey and now decided to give it a second chance. New functionalities were added and a lot was improved from the original version, although it still lacks core aspects I was able to acquire a better understanding of since then and am yet to implement through future updates. 

It was built using HTML/CSS, MySQL and the Python Framework: Flask. The application was created with the intention of rationalizing your day to day interactions. To help better understand, here's a quick run through of how it works.

## Concept:

Let's say you meet a person who sparks your interest. A few days of getting to know each other go by and you're curious about how much, objectively, this person has in common with you. 

Now, the only one capable of making that kind of judgment is yourself, and that's where MyMatch comes in. Its main purpose is to help individuals better understand how characteristics, opinions and behaviors they personally value would match someone else's.

## Getting Started:

**MyMatch** features a basic Login/Sign-Up page where users can register a personal account. Once logged in, their username and a hashed (SHA-256) version of the password will be stored in the "User" table as strings, along with an auto-generated identifier in "INT" format. The user's session will be remembered up to one full year as long as they don't log-out or access the Login/Sign-Up page.

## MyTypes

Are considered Types any tastes, opinions, characteristics and beliefs a user might wish to analyze a relationship by. One can have an unlimited amount of Types, each tied to its own Weight. The Weight is a value from 1 to 10, assigned by the user according to how relevant they personally find that Type to be. Once a new Type is added, the information will be associated with their "User ID", stored in the "Types" table along with its Weight and can be deleted at will.

## New Match

Time to finally create a Match. In this section, you will apply the Types you created earlier as parameters, and rate your Match from 1 to 10 based on each of them. Feel free to choose which Types you will be using (at least 3) by leaving the others blank, but remember: 

1. You are not allowed to create multiple Matches using the same name. 
2. The more Types you base your match on, the more accurate the result is going to be. This result will be a percentage, and is going to inform how compatible you are with said person based on the data you entered.

The algorithm responsible for this process is the following:

```
perfect = 0
score = 0
for i in range(len(types)):
    perfect += weights[i]
    score += weights[i] * (vals[i] * 0.1)
score = round((score * 100) / perfect)
```

## MyMatches

**MyMatches** serves as the Home Page, where you can **view** and **delete** previously created Matches. User's Matches are stored inside the "Matches" table and are made up of their Types and Weights as JSON lists.

## User Settings:

- ```Delete Account```

## Future Updates

- **_Categorized Types_**: the set of attributes you cherish in a person may vary depending on the kind of relationship you are or expect to be in. For example, you might want your best friend to be athletic, funny and political. But at the same time, want your loved one to be sensitive, realistic and protective. Type categorization will allow you to have both.
- Light/Dark mode.
- Profile picture.
- "_Last Added_" Match dates.
- _**Edit Match**_: perception towards relationships and people inevitably change with time. Being able to keep your Matches up to date without having to recreate it every time a change must be made is essential. 
- Change Username and Password.
- Bug fixes.
