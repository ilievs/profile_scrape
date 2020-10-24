# profile_scrape
Some python code for scraping the profiles of a specific site just for fun :)

Install the required packages:

```
pip install -r requirements.txt
```

Start the database:

```bash
docker-compose up -d
```

Starting the scrape:

```
python main.py scrape
```

For starting the server:

```
python main.py serve
```

The scraping and the server can run simultaneously as separate processes. 