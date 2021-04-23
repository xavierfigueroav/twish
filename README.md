# covidhelpfilter
*covidhelpfilter* is a web application that allows you to classify COVID19-related tweets into three categories: **help offer**, **help wanted** and **noise**. You enter a query string, the app uses it as search term to collect tweets, it classifies them and shows them classified to you.

Build with Django and React.

## Set up
1. Install [Docker Compose](https://docs.docker.com/compose/install) on your machine.
2. Get the source code on to your machine via git.

`git clone https://github.com/xavierfigueroav/covidhelpfilter && cd covidhelpfilter`

3. Build and run the Docker containers.

`docker-compose up --build`

4. That's it. Open a web browser and hit the URL http://127.0.0.1:3000.
