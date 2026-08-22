from fastapi import FastAPI, Request, Query, Path
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .repository import (
    graph_summary,
    list_people,
    list_skills,
    person_profile,
    recommendations,
    shortest_learning_path,
)
from .db import close_driver

app = FastAPI(title='SkillGraph', version='1.1.0')
app.mount('/static', StaticFiles(directory='static'), name='static')
templates = Jinja2Templates(directory='templates')


@app.on_event('shutdown')
def shutdown():
    close_driver()


def _log_error(context: str, exc: Exception):
    print(f'[SkillGraph] {context}: {exc!r}')


def render_error(request: Request, exc: Exception, status_code: int = 503):
    _log_error('page error', exc)
    return templates.TemplateResponse(
        'error.html',
        {'request': request, 'message': 'Graph database is temporarily unavailable. Please try again.'},
        status_code=status_code,
    )


def unavailable(exc: Exception):
    _log_error('api error', exc)
    return JSONResponse({'error': 'Graph database is temporarily unavailable.'}, status_code=503)


@app.get('/', response_class=HTMLResponse)
def home(request: Request):
    try:
        return templates.TemplateResponse(
            'index.html',
            {
                'request': request,
                'summary': graph_summary(),
                'skills': list_skills(),
            },
        )
    except Exception as exc:
        return render_error(request, exc)


@app.get('/api/people')
def api_people(search: str = Query('', max_length=80)):
    try:
        return list_people(search)
    except Exception as exc:
        return unavailable(exc)


@app.get('/api/skills')
def api_skills():
    try:
        return list_skills()
    except Exception as exc:
        return unavailable(exc)


@app.get('/api/person/{person_id}')
def api_person(person_id: str = Path(..., min_length=1, max_length=80)):
    try:
        profile = person_profile(person_id)
        if not profile:
            return JSONResponse({'error': 'Person not found'}, status_code=404)
        return profile
    except Exception as exc:
        return unavailable(exc)


@app.get('/api/recommendations')
def api_recommendations(
    skill: str = Query(..., min_length=1, max_length=80),
    target_role: str = Query('', max_length=80),
):
    try:
        return recommendations(skill, target_role)
    except Exception as exc:
        return unavailable(exc)


@app.get('/api/learning-path')
def api_learning_path(
    person_id: str = Query(..., min_length=1, max_length=80),
    target_skill: str = Query(..., min_length=1, max_length=80),
):
    try:
        return shortest_learning_path(person_id, target_skill)
    except Exception as exc:
        return unavailable(exc)


@app.get('/health')
def health():
    try:
        return {'status': 'ok', 'graph': graph_summary()}
    except Exception as exc:
        
        _log_error('health error', exc)
        return JSONResponse({'status': 'error', 'detail': 'Graph database is unavailable.'}, status_code=503)
