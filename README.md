# Run virtual environment
pip install pipenv
pipenv shell
pipenv install -r requirements.txt


# How to run 
uvicorn main:app --reload