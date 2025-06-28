const addButton = document.getElementById("addButton");
const ul = document.getElementById("taskList");
const pul = document.getElementById("pendingList");
const cul = document.getElementById("completedList");
const tasks = [];

addButton.addEventListener("click", event => {
  event.preventDefault();
  const taskTitle = document.getElementById("taskTitle");
  const title = taskTitle.value.trim();
  if (!title) return; 

  tasks.push({
    id: Date.now(),
    title,
    completed: false,
  });
  taskTitle.value = "";
  render();
});

function render() {
  ul.innerHTML = "";
  pul.innerHTML = "";
  cul.innerHTML = "";

  tasks.forEach(task => {
    // Create elements
    const label = document.createElement("label");
    const input = document.createElement("input");
    const span = document.createElement("span");
    const del = document.createElement("button");
    const li = document.createElement("li");

    // Setup checkbox and text
    input.type = "checkbox";
    input.checked = task.completed;
    span.textContent = task.title;
    del.textContent = "🗑️";

    // Add CSS classes
    li.className = "task-item";
    label.className = "task-label";
    input.className = "task-checkbox";
    span.className = "task-text";
    del.className = "task-delete";

    // Append elements
    ul.appendChild(li);
    li.appendChild(label);
    li.appendChild(del);
    label.appendChild(input);
    label.appendChild(span);

    // Pending/completed lists
    const filterli = document.createElement("li");
    filterli.textContent = task.title;
    filterli.className = "filter-item";

    if (task.completed) {
      cul.appendChild(filterli);
    } else {
      pul.appendChild(filterli);
    }

    // Event listeners
    input.addEventListener("change", () => {
      task.completed = input.checked;
      render();
    });

    del.addEventListener("click", () => {
      const index = tasks.findIndex(t => t.id === task.id);
      if (index > -1) {
        tasks.splice(index, 1);
        render();
      }
    });
  });
}
