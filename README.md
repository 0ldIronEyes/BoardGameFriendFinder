Board Game Friend Finder

This app allows users to sign up and search for nearby fans of board games to facilitate board game nights.Users can create an account and add games that they have in their collection, and see what games other users have in their collecions. Users can then contact nearby players via email and plan game sessions.

The app is created using Flask, postGRES, and jinja. 

APIs used -
Google Distance API
https://developers.google.com/maps/documentation/distance-matrix/distance-matrix

This api is used to calculate distance from the logged in user to the 


BoardGameGeek API

https://boardgamegeek.com/wiki/page/BGG_XML_API2




how to install:

1.Clone repository.

2. Install flask and dependencies in requirements.txt

3. open cmd in directory and run flask

4. open browser and server on localhost. 

Deployed URL-

https://boardgamefriendfinder.onrender.com


how to Use:

Sign up for an account, entering your name, email address, location, password, and optionally an image url. For location, enter your city, State.

Once on the homepage, a list of the closest nearby players will be displayed. On the left sidebar, you can click on the "my games" button to be taken to your games page.

 On the game page, you can search for games in the search bar, and add your favorite games to your collection. Add and remove games until you 
are satisfied with your displayed list of games. This is the collection other users will see when they click on your profile. You can return to the homepage and look at the list of nearby users. 

Clicking on one of the users will bring you to the comparison page where you can get a more detailed view of the user you clicked on.
On this page you can see a list of games both you and the other user have in your collection and see if there are any you have in common. The user's email address will be displayed on this page if you choose to contact them.

On the homepage, you can click on the edit profile button on the sidebar to edit your profile information.
