#** Nunez,Priscilla  
#** Fall 2018 • SI364 midterm


#** Marvel Comic Collection App **
App allows a user to register and be able to search for Marvels Comics Collection for a particular year.
The proposed features for the app are as follows:

- **User will be able to register / login to the app. No password required.**
- **User will be able to search for a particular year.**
- **User will be able to bookmark a comic out of the ones returned from a searched year.**
- **User will be able to view all comics he has bookmarked.**
- **User should be able to like a comic. [One:many relationship]**
- **User will be able to view all comics he has liked.** 
- **User will be able to view a list of all registered users in the application.**
- **User will be able to list all years he has previously searched. [One:many relationship w/in year and collections.]**

#** Available Routes are as follows:

- http://locahost:50000 -> index.html
- http://locahost:50000/search -> search.html
- http://locahost:50000/like -> none
- http://locahost:50000/bookmark -> none
- http://locahost:50000/likes -> liked_comics.html
- http://locahost:50000/bookmarks -> bookmarked_comics.html
- http://locahost:50000/names -> name_example.html
- http://locahost:50000/searches -> searches.html
- http://locahost:50000/logout -> none


#** All requirements have been met. NunezP 

 - **Ensure that the SI364midterm.py file has all the setup (app.config values, import statements, code to run the app if that file is run, etc) necessary to run the Flask application, and the application runs correctly on http://localhost:5000 (and the other routes you set up)
 Add navigation in base.html with links (using a href tags) that lead to every other viewable page in the application. (e.g. in the lecture examples from the Feb 9 lecture, like this )**

 - **Ensure that all templates in the application inherit (using template inheritance, with extends) from base.html and include at least one additional block.
 Include at least 2 additional template .html files we did not provide.**

 - **At least one additional template with a Jinja template for loop and at least one additional template with a Jinja template conditional.
These could be in the same template, and could be 1 of the 2 additional template files.**
 
 - **At least one errorhandler for a 404 error and a corresponding template.**
 
 - **At least one request to a REST API that is based on data submitted in a WTForm.**

 - **At least one additional (not provided) WTForm that sends data with a GET request to a new page.**
 
 - **At least one additional (not provided) WTForm that sends data with a POST request to the same page.**
 
 - **At least one custom validator for a field in a WTForm.**

 - **At least 2 additional model classes.
 Have a one:many relationship that works properly built between 2 of your models.**
 
 - **Successfully save data to each table.**
 
 - **Successfully query data from each of your models (so query at least one column, or all data, from every database table you have a model for).**
 
 - **Query data using an .all() method in at least one view function and send the results of that query to a template.**
 
 - **Include at least one use of redirect. (HINT: This should probably happen in the view function where data is posted...)**
 
 - **Include at least one use of url_for. (HINT: This could happen where you render a form...)**
 
 - **Have at least 3 view functions that are not included with the code we have provided. (But you may have more! Make sure you include ALL view functions in the app in the documentation and ALL pages in the app in the navigation links of base.html.)**

#** NunezP original code - Additional requirements met for an additional 200 points (to reach 100%) -- an app with extra functionality.

- **(100 points) Include an additional model class (to make at least 4 total in the application) with at least 3 columns. Save data to it AND query data from it; use the data you query in a view-function, and as a result of querying that data, something should show up in a view. (The data itself should show up, OR the result of a request made with the data should show up.)**

- **(100 points) Write code in your Python file that will allow a user to submit duplicate data to a form, but will not save duplicate data (like the same user should not be able to submit the exact same tweet text for HW3).**
# si364F18midterm
