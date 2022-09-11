from fastapi import FastAPI

app = FastAPI()

@app.get('/data')
def index():
    return {'data':{'name:':'Tom'}}


@app.get('/about')
def about():
    return {'data':'about page'}