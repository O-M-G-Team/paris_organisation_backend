# Install virtual environment
```
pip install pipenv
```

# Run virtual environment
```
pipenv shell
```
```
pipenv install -r requirements.txt
```

# Deactivate virtual environment
```
deactivate
```

# Connect to local MongoDB database
1. Run mongo container in docker
2. Open MongoDB Compass
3. Connect to ```mongodb://localhost:27017```


# How to run 
1. Make sure you connect to the mongodb database as specified above.
2. Run the following command in terminal.
```
uvicorn main:app --reload
```

# To try and test api 
Please visit 
```http://127.0.0.1:8000/docs```