

This project consists in connecting back end to front end. The application uses React(front end) to accept data from two other applications(back end). In the back end, one application has credintials to get songs information from spotify with lyrics link from genius and the second application has songs, artists from the database.


#  Making the back end , APIS and testing
the backend was made in python from files of project milestone1(main.py) and project milestone2(app.py). The two apps are also deposited on github and they contain the API calls for the front end. The back end can be tested indepently in thee terminal to check which data that wiill be transferred to the front end. For instance, for milestone2 back end: run 'python3 appy' and browse http://127.0.0.1:5000/users. This will show {"email": "jkumutima3@gmail.com", "id": 1, "password": "123456"}. That is an example of JSON data retrieved from the database and they are to be transmitted to the front end.



# Getting Started with Create React App

This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app).

# USed Scripts

In the project directory, you can run:

### `npm start`
It runs the app that I developped 
Click on  [http://localhost:3000](http://localhost:3000) to view it in the browser.
The app from Milestone1 run on 3000 while the app from milestone2 run on port 5000. The two apps have to be also running for the front end to be woring. The front end will decide which part of the apps to display. FOr instance, fetch('http://127.0.0.1:5000/spotify') in React will display the Justin Bieber random song from top five songs that i got from spotify ini project milestone1. The components run specific pages in the fron end. For instance, the component song displays songs of choise eaither from the first app or the second app.

The page will reload if you make edits while it is still loading. ctrl+c stops the app
You will also see any lint errors in the console.

### `npm test`
It launches the test runner in the interactive watch mode. I runned it while the other two apps in the backend are simultaneously running.
 

### Deployment
My React app uses the back end built on two apps that have already been deployed on Heroku in the previous project milestones. 



### README Questions:
What are at least 3 technical issues you encountered with your project? How did you fix them?  
    I encountered my laptop not being able to run my code. I fixed it by installinig missing packages on my laptop
    I encountered that JSON  API for my database is not serializable and i had to change the syntax to make it serializable
    I encountered that some modules such "connexion" does not download on my laptop for the reasons I could not find. To resolve this obstacle, I decided to use other libraries.
What part of the stack do you feel most comfortable with? What part are you least comfortable with?
    I feel confortable with react codes in front end or python in the backend
    I dont feel confortable in generating JSON  API data especially from Milestone two because it contained multiple functions which needed their specific API calls and hence involve multiple components in React to be created.


Techniques that I used:
how to change python backend into json data for java scripts:https://www.w3schools.com/python/gloss_python_convert_into_JSON.asp, 
I had to install extra modules.