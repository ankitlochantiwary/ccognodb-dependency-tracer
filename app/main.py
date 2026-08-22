from fastapi import FastAPI, Request, Query
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from .repository import graph_summary, list_people, list_skills, person_profile, recommendations, shortest_learning_path
from .db import close_driver

app = FastAPI(title='CognoDB SkillGraph', version='1.0.0')
app.mount('/static', StaticFiles(directory='static'), name='static')
templates = Jinja2Templates(directory='templates')

@app.on_event('shutdown')
def shutdown():
    close_driver()

def error(request: Request, message: str, status_code=503):
    return templates.TemplateResponse('error.html', {'request': request, 'message': message}, status_code=status_code)

@app.get('/', response_class=HTMLResponse)
def home(request: Request):
    try:
        return templates.TemplateResponse('index.html', {'request': request, 'summary': graph_summary(), 'skills': list_skills()})
    except Exception as exc:
        return error(request, str(exc))

@app.get('/api/people')
def api_people(search: str = Query('', max_length=80)):
    try: return list_people(search)
    except Exception as exc: return JSONResponse({'error': str(exc)}, status_code=503)

@app.get('/api/person/{person_id}')
def api_person(person_id: str):
    try:
        profile = person_profile(person_id)
        return profile if profile else JSONResponse({'error':'Person not found'}, status_code=404)
    except Exception as exc: return JSONResponse({'error': str(exc)}, status_code=503)

@app.get('/api/recommendations')
def api_recommendations(skill: str):
    try: return recommendations(skill)
    except Exception as exc: return JSONResponse({'error': str(exc)}, status_code=503)

@app.get('/api/learning-path')
def api_learning_path(person_id: str, target_skill: str):
    try: return shortest_learning_path(person_id, target_skill)
    except Exception as exc: return JSONResponse({'error': str(exc)}, status_code=503)

@app.get('/health')
def health():
    try: return {'status':'ok', 'graph':graph_summary()}
    except Exception as exc: return JSONResponse({'status':'error','detail':str(exc)}, status_code=503)
