async function getJson(url){
  const r=await fetch(url);
  const data=await r.json();
  if(!r.ok) throw new Error(data.error||data.detail||'Request failed');
  return data;
}

const peopleList=document.getElementById('peopleList');
const peopleCount=document.getElementById('peopleCount');
const personSearch=document.getElementById('personSearch');
const skillSelect=document.getElementById('skillSelect');
const pathSkill=document.getElementById('pathSkill');
const pathPerson=document.getElementById('pathPerson');
const recBox=document.getElementById('recommendations');
const pathBox=document.getElementById('pathResult');

function escapeHtml(value){
  return String(value??'').replace(/[&<>'"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[c]));
}

async function loadSkills(){
  try{
    const rows=await getJson('/api/skills');
    const options='<option value="">Choose a skill</option>'+rows.map(s=>`<option value="${escapeHtml(s.name)}">${escapeHtml(s.name)}</option>`).join('');
    skillSelect.innerHTML=options;
    pathSkill.innerHTML='<option value="">Target skill</option>'+rows.map(s=>`<option value="${escapeHtml(s.name)}">${escapeHtml(s.name)}</option>`).join('');
  }catch(e){
    skillSelect.innerHTML='<option value="">Skills unavailable</option>';
    pathSkill.innerHTML='<option value="">Skills unavailable</option>';
  }
}

async function loadPeople(){
  peopleList.innerHTML='<div class="loading">Loading people…</div>';
  try{
    const data=await getJson('/api/people?search='+encodeURIComponent(personSearch.value));
    peopleCount.textContent=data.length+' people';
    peopleList.innerHTML=data.length
      ? data.map(p=>`<div class="person" data-id="${escapeHtml(p.id)}"><div><strong>${escapeHtml(p.name)}</strong><small>${escapeHtml(p.role)} · ${escapeHtml(p.company)}</small></div><span class="skill-count">${p.skill_count} skills</span></div>`).join('')
      : '<div class="empty">No matching people.</div>';
    document.querySelectorAll('.person').forEach(el=>el.addEventListener('click',()=>showPerson(el.dataset.id)));
  }catch(e){
    peopleCount.textContent='unavailable';
    peopleList.innerHTML='<div class="empty">'+escapeHtml(e.message)+'</div>';
  }
}

async function showPerson(id){
  try{
    const p=await getJson('/api/person/'+encodeURIComponent(id));
    const projects=(p.projects||[]).map(x=>x.name).filter(Boolean).join(', ')||'None listed';
    alert(`${p.name}\n${p.role} · ${p.company}\n\n${p.bio||''}\n\nSkills: ${(p.skills||[]).join(', ')}\n\nProjects: ${projects}`);
  }catch(e){alert(e.message)}
}

document.getElementById('searchBtn').onclick=loadPeople;
personSearch.addEventListener('keydown',e=>{if(e.key==='Enter')loadPeople()});

document.getElementById('recommendBtn').onclick=async()=>{
  const skill=skillSelect.value;
  if(!skill){recBox.innerHTML='<div class="empty">Choose a skill first.</div>';return}
  recBox.innerHTML='<div class="loading">Traversing connected projects and roles…</div>';
  try{
    const rows=await getJson('/api/recommendations?skill='+encodeURIComponent(skill)+'&target_role='+encodeURIComponent(document.getElementById('roleInput').value));
    recBox.innerHTML=rows.length
      ? rows.map(r=>`<div class="rec"><div class="rec-top"><strong>${escapeHtml(r.name)}</strong><span class="score">${r.score}% connected</span></div><small>${escapeHtml(r.role)} · ${escapeHtml(r.company)}</small><div>${(r.shared_projects||[]).filter(Boolean).map(x=>`<span class="tag">${escapeHtml(x)}</span>`).join('')}</div></div>`).join('')
      : '<div class="empty">No connected candidates found.</div>';
  }catch(e){recBox.innerHTML='<div class="empty">'+escapeHtml(e.message)+'</div>'}
};

async function populatePathPeople(){
  try{
    const rows=await getJson('/api/people');
    pathPerson.innerHTML='<option value="">Choose a person</option>'+rows.map(p=>`<option value="${escapeHtml(p.id)}">${escapeHtml(p.name)} — ${escapeHtml(p.role)}</option>`).join('');
  }catch(e){pathPerson.innerHTML='<option value="">Unavailable</option>'}
}

document.getElementById('pathBtn').onclick=async()=>{
  const person_id=pathPerson.value,target_skill=pathSkill.value;
  if(!person_id||!target_skill){pathBox.innerHTML='<div class="empty">Choose both a person and target skill.</div>';return}
  pathBox.innerHTML='<div class="loading">Finding shortest relationship path…</div>';
  try{
    const rows=await getJson('/api/learning-path?person_id='+encodeURIComponent(person_id)+'&target_skill='+encodeURIComponent(target_skill));
    if(!rows.length){pathBox.innerHTML='<div class="empty">No path found.</div>';return}
    const r=rows[0];
    pathBox.innerHTML=`<div class="path">${r.nodes.map((n,i)=>`${i?'<span class="arrow">→</span>':''}<span class="node">${escapeHtml(n)}</span>`).join('')}</div><p class="muted">${r.hops} hops. This is a graph traversal across relationship types.</p>`;
  }catch(e){pathBox.innerHTML='<div class="empty">'+escapeHtml(e.message)+'</div>'}
};

Promise.all([loadSkills(),loadPeople(),populatePathPeople()]);
