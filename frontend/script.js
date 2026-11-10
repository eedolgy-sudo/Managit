const form = document.querySelector('#task-form');
const input = document.querySelector('#task-name');
const list = document.querySelector('#task-list');
const message = document.querySelector('#message');

async function request(url, options = {}) {
  const response = await fetch(url, options);
  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  if (response.status === 204) return null;
  return response.json();
}

async function loadTasks() {
  try {
    message.textContent = '';
    const tasks = await request('/tasks');
    list.replaceChildren();
    for (const task of tasks) {
      const item = document.createElement('li');
      const label = document.createElement('span');
      label.textContent = task.name;
      const remove = document.createElement('button');
      remove.type = 'button';
      remove.textContent = 'Delete';
      remove.addEventListener('click', async () => {
        try {
          await request(`/tasks/${task.id}`, { method: 'DELETE' });
          await loadTasks();
        } catch (error) { message.textContent = `Could not delete task: ${error.message}`; }
      });
      item.append(label, remove);
      list.append(item);
    }
  } catch (error) { message.textContent = `Could not load tasks: ${error.message}`; }
}

form.addEventListener('submit', async (event) => {
  event.preventDefault();
  const name = input.value.trim();
  if (!name) return;
  try {
    await request('/tasks', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name })
    });
    input.value = '';
    await loadTasks();
  } catch (error) { message.textContent = `Could not create task: ${error.message}`; }
});

loadTasks();
