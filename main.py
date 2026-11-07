from fastapi import Depends, FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from database import Session, engine, session
from models import Task, base

app = FastAPI()


def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()


base.metadata.create_all(bind=engine)
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
def home(req: Request , db: Session = Depends(get_db)):
    tasks = db.query(Task).order_by(Task.id.desc()).all()
   
    return templates.TemplateResponse(
    request=req, name="home.html", context={"result": tasks}
    )
    


@app.post("/")
def add_task(req: Request, task: str = Form(), db: Session = Depends(get_db)):
    task = Task(title=task)
    db.add(task)
    db.commit()

    return RedirectResponse(url="/", status_code=303)
@app.post("/{task_id}/complete")
def complete(req: Request, task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if task is not None:
        task.completed = True
        db.commit()
    return RedirectResponse(url="/", status_code=303)


@app.post("/{task_id}/delete")
def delete(req: Request, task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if task is not None:
        db.delete(task)
        db.commit()
    return RedirectResponse(url="/", status_code=303)
