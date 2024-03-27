const addForm = document.querySelector(".add");
const list = document.querySelector(".todos");
const search = document.querySelector(".search input");

// add new todos
const generateTemplate = (todo) => {
  const html = `
        <li class="list-group-item d-flex justify-content-between align-items-center">
        <span>${todo}</span>
        <i class="far fa-trash-alt delete"></i>
        </li>
        `;
  list.innerHTML += html;
};

function deleteTask(taskId) {
    // Make an AJAX request to delete the task
    fetch(`/tasks/${taskId}`, {
      method: 'DELETE',
    })
      .then(response => {
        if (response.ok) {
          // Task deleted successfully, remove the corresponding list item
        //   const listItem = document.getElementById(`deleteForm${taskId}`).closest('li');
        //   listItem.remove();
        // Reload the page after successful deletion
            location.reload();
        } else {
          // Handle error response
          console.error('Failed to delete task');
        }
      })
      .catch(error => {
        console.error('An error occurred while deleting the task', error);
      });
  }

const filterTodos = (term) => {
  Array.from(list.children)
    .filter((todo) => !todo.textContent.toLowerCase().includes(term))
    .forEach((todo) => todo.classList.add("filtered"));

  Array.from(list.children)
    .filter((todo) => todo.textContent.toLowerCase().includes(term))
    .forEach((todo) => todo.classList.remove("filtered"));
};

// keyup event
search.addEventListener("keyup", () => {
  const term = search.value.trim().toLowerCase();
  filterTodos(term);
});

function toggleCompletion(taskId) {
    // Make an AJAX request to toggle the task completion status
    fetch(`/tasks/${taskId}/toggle-completion`, {
      method: 'GET',
    })
      .then(response => {
        if (response.ok) {
          // Task completion status toggled successfully
          // Reload the page after successful toggle
          location.reload();
        } else {
          // Handle error response
          console.error('Failed to toggle task completion status');
        }
      })
      .catch(error => {
        console.error('An error occurred while toggling the task completion status', error);
      });
  }