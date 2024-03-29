Mix pairs of song lyrics to form new lyrics.

Songs can be picked either by the user or randomly by the application.


# Development

Run tests with `pipenv run pytest -v`

You can enable console print by running `pipenv run pytest -s`

Code coverage: `pipenv run pytest -v --cov=. --cov-report html`, then access the coverage report at `htmlcov/index.html`

Skip slow tests: `pipenv run pytest --without-slow-integration` (see https://pypi.org/project/pytest-integration/).


# Runtime

## Standalone scripts

### Mix lyrics parsing artists from free text

```bash
pipenv run python mixlyrics_parse_free_text.py 'Madonna, Slayer'
```


## REST API
Implemented using [Flask](https://palletsprojects.com/p/flask/)

See: `lyrics_mixer/rest_api.py` and `lyrics_mixer/rest_api.py`.

Run locally with:

```bash
pipenv shell
gunicorn lyrics_mixer.rest_api:app
```

### Endpoints

`HTTP GET http://localhost:8000/`: gives status

`HTTP GET http://localhost:8000/mix/random`: mix two random songs

`HTTP GET http://localhost:8000/mix/artists/<artist1>/<artist2>`: mix random lyrics from two artists

`HTTP GET http://localhost:8000/mix/songs/<artist1>/<title1>/<artist2>/<title2>`: mix two specific lyrics


## Twitter Bot
Implemented using [Tweepy](https://www.tweepy.org/).


# Deployment

## Environment variables

Environment variables for storing auth tokens:

`LYRICS_MIXER_TWITTER_CONSUMER_KEY`

`LYRICS_MIXER_TWITTER_CONSUMER_SECRET`

`LYRICS_MIXER_TWITTER_ACCESS_TOKEN`

`LYRICS_MIXER_TWITTER_ACCESS_TOKEN_SECRET`

Environment variable for the database URL:

`LYRICS_MIXER_DATABASE_URL`

## Docker
A `docker-compose.yml` file is available for running the PostgreSQL and Twitter Bot Docker containers.

By default, docker-compose will look for an `.env` file in this directory with the definitions of the environment variables listed above.

To build the Docker image of the Twitter bot:

```bash
docker-compose build
```

To run the containers:

```bash
docker-compose up
```

To run the containers in the background and support host restart:

```bash
docker-compose up -d
```

## Heroku
The file `Procfile` describes both the REST API app and the Twitter bot (as a worker).

### Database setup
Enable PostgreSQL add-on on Heroku dashboard.

`twitter_bot.py` creates tables on startup.

Verify:

```bash
heroku pg:info
```

should show 1 table (streamcursor table)

### Keep awake Heroku instance
Keep awake Heroku instance by running a schedule job.

#### Cron
Every 30 minutes except between 2 am and 8 am, since Heroku force sleep free instances 6 hours a day:

`0/30 0-2,8-23 * * * /usr/bin/curl https://lyricsmixer.herokuapp.com > /tmp/lyricsmixer-ping.log`

#### Systemd Timer
Install unit provided in the `heroku` directory: `heroku_lyricsmixer_ping.timer`, `heroku_lyricsmixer_ping.service`

```bash
cd heroku
sudo cp heroku_lyricsmixer_ping.* /etc/systemd/system
sudo systemctl enable heroku_lyricsmixer_ping.timer
sudo systemctl start heroku_lyricsmixer_ping.service
```

Check timer is installed:

```bash
sudo systemctl list-timers --all
```
