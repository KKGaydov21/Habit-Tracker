const api = {
  list: () => fetch('/api/habits').then(r => r.json()),
  add: (name) => fetch('/api/habits', {method:'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify({name})}).then(r => r.json()),
  toggle: (id) => fetch(`/api/habits/${id}/toggle`, {method:'POST'}).then(r => r.json()),
  del: (id) => fetch(`/api/habits/${id}`, {method:'DELETE'}).then(r => r.json()),
};

function el(tag, attrs = {}, ...children) {
  const e = document.createElement(tag);
  Object.entries(attrs).forEach(([k,v]) => {
    if (k === 'on') { Object.entries(v).forEach(([ev,fn]) => e.addEventListener(ev, fn)); }
    else e.setAttribute(k, v);
  });
  children.forEach(c => {
    if (typeof c === 'string') e.appendChild(document.createTextNode(c));
    else if (c) e.appendChild(c);
  });
  return e;
}

async function render() {
  const list = document.getElementById('habits-list');
  list.innerHTML = '';
  const habits = await api.list();
  if (habits.length === 0) {
    list.appendChild(el('li', {}, 'No habits yet. Add one!'));
    return;
  }
  habits.forEach(h => {
    const doneToday = h.last_completed === new Date().toISOString().slice(0,10);
    const nameEl = el('span', {class: 'habit-name' + (doneToday ? ' done' : '')}, h.name);
    const small = el('div', {class:'small'}, doneToday ? 'Done today' : '');
    const left = el('div', {}, nameEl, small);

    const toggleBtn = el('button', {class:'toggle-done', on: {click: async () => { await api.toggle(h.id); render(); }}}, doneToday ? 'Undo' : 'Done');
    const delBtn = el('button', {class:'delete-btn', on: {click: async () => { if (confirm('Delete habit?')) { await api.del(h.id); render(); }}}}, 'Delete');
    const actions = el('div', {class:'habit-actions'}, toggleBtn, delBtn);
    const li = el('li', {}, left, actions);
    list.appendChild(li);
  });
}

document.getElementById('new-habit-form').addEventListener('submit', async (e) => {
  e.preventDefault();
  const input = document.getElementById('habit-name');
  const name = input.value.trim();
  if (!name) return;
  await api.add(name);
  input.value = '';
  render();
});

render();
