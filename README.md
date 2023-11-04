# bac-visualization

## Web tool for estimating and visualizing blood alcohol concentration

A web application to estimate and visualize blood alchohol concentration (BAC). Many BAC calculators are available online (eg. https://paihdelinkki.fi/fi/testit-ja-laskurit/laskurit/promillelaskuri). This web application works in the same way, but also plots the estimated BAC as a function of time.

How it works:

  - Users can create an account and log in to the website
  - Users can then choose alcoholic beverages from a list of different types of drinks, along with the time of consumption.
  - The alcohol content and timestamp of the user's beverages will be saved into a database.
  - Upon user request, a plot of estimated BAC will be generated (BAC in permilles on the y-axis, time on the x-axis)
      - This will be done by taking the alcoholic beverages attributed to the user and using them to calculate time series data of the user's estimated BAC (eg. 5-10 minute intervals). This data will then be used to plot the estimated BAC over time.

  - There could also be a group functionality, where users could create/join a "room" using a keyword.
      - Users in the same room could generate a plot that shows the estimated BAC of all the users in the room.
      - The rooms could be either public, where they are listed on the website, or private, where only users that know the keyword can join.
   
The point of this project is not to encourage irresponsible drinking, but to act as a coding exercise for myself. I don't recommend anyomne to use this application to make actual decisions concerning their blood alcohol concentration, as results might be inaccurate. There are various more reliable BAC calculators online (eg. the one at päihdelinkki).


This project was inspired by the "blakkisvuohi" project by ultsi: https://gitlab.com/ultsi-projects/blakkisvuohi
