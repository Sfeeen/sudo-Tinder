# sudo Tinder 💃💃
A desktop GUI written in python that interacts with the tinder-servers. It provides some of the basic functionality (swiping, checking pictures) but more importantly it provides some extra features:

* Load multiple potential swipes at once and choose who you swipe and who you do not want to swipe (or swipe later).
* Change your location, fill in the longitude and latitude of were you want to be and the server will think that you are on that location. You will fetch swipes from the same area
* See some people who like you (tinder provides some blurred pictures of people who like you and you could see the pictures if you buy a premium account: those pictures are shown without a blur).

### Note
* This project is not fully finished, errors might occur! feel free to improve the GUI / logic
* If you fetch a lot of swipes, like constantly, than you might get temporarly blocked, there is no check for this in the app yet.

### Usage
run: `python3 app.py` 

windows users can use the generated `app.exe` 

### Preview
![alt text](https://github.com/Sfeeen/sudo-Tinder/blob/master/sudo_tinder.JPG "preview")

### Credits 
I started of from the Tinder api calls found by [fbessez](https://github.com/fbessez/Tinder). The fb-authenthication seemed not to work anymore, so that got fixed and I added some new calls e.g. to change the location without a premium account, to get all the likes pictures


