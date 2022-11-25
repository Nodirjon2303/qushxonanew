from celery import Celery
BROKER_URL = "redis://:postgres@127.0.0.1:6379/0"
app = Celery('main', BROKER_URL)
@app.main
def maximum(x, y):
    if x > y:
        return x
    else:
        return y
# redis://:postges@;localhost:5432/