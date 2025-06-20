let editingRoleId = null;

// 加载角色列表
function loadRoles(keyword = '') {
  let url = '/roles/list';
  if (keyword.trim() !== '') {
    url = `/roles/search?keyword=${encodeURIComponent(keyword.trim())}`;
  }

  fetch(url)
    .then(res => res.json())
    .then(data => {
      const tbody = document.querySelector('#rolesTable tbody');
      tbody.innerHTML = '';
      data.forEach(role => {
        const row = document.createElement('tr');
        row.innerHTML = `
          <td>${role.role_id}</td>
          <td>${role.role_name}</td>
          <td>${role.actor_name || ''}</td>
          <td>${role.movie_title || ''}</td>
          <td>
            <button onclick="editRole(${role.role_id}, '${role.role_name}', ${role.actor_id}, ${role.movie_id})">编辑</button>
            <button onclick="deleteRole(${role.role_id})">删除</button>
          </td>
        `;
        tbody.appendChild(row);
      });
    })
    .catch(err => console.error('加载角色失败:', err));
}

// 加载演员列表供选择
function loadActors() {
  fetch('/actors/list')
    .then(res => res.json())
    .then(data => {
      const select = document.getElementById('actorSelect');
      select.innerHTML = '<option value="">请选择演员</option>';
      data.forEach(actor => {
        const option = document.createElement('option');
        option.value = actor.actor_id;
        option.textContent = actor.name;
        select.appendChild(option);
      });
    });
}

// 加载电影列表供选择
function loadMovies() {
  fetch('/movies/list')
    .then(res => res.json())
    .then(data => {
      const select = document.getElementById('movieSelect');
      select.innerHTML = '<option value="">请选择电影</option>';
      data.forEach(movie => {
        const option = document.createElement('option');
        option.value = movie.movie_id;
        option.textContent = movie.title;
        select.appendChild(option);
      });
    });
}

function showForm(title) {
  document.getElementById('formTitle').innerText = title;
  document.getElementById('roleForm').style.display = 'block';
}

function hideForm() {
  document.getElementById('roleForm').style.display = 'none';
  document.getElementById('roleNameInput').value = '';
  document.getElementById('actorSelect').value = '';
  document.getElementById('movieSelect').value = '';
  editingRoleId = null;
}

document.getElementById('saveBtn').addEventListener('click', () => {
  const role_name = document.getElementById('roleNameInput').value.trim();
  const actor_id = document.getElementById('actorSelect').value;
  const movie_id = document.getElementById('movieSelect').value;

  if (!role_name) {
    alert('角色名称不能为空');
    return;
  }
  if (!actor_id) {
    alert('请选择演员');
    return;
  }
  if (!movie_id) {
    alert('请选择电影');
    return;
  }

  const url = editingRoleId ? `/roles/${editingRoleId}` : '/roles/add';
  const method = editingRoleId ? 'PUT' : 'POST';

  fetch(url, {
    method: method,
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ role_name, actor_id, movie_id })
  })
    .then(res => res.json())
    .then(data => {
      alert(data.message || '操作成功');
      hideForm();
      loadRoles();
    })
    .catch(err => {
      console.error('提交失败:', err);
      alert('提交失败');
    });
});

document.getElementById('cancelBtn').addEventListener('click', hideForm);

document.getElementById('addBtn').addEventListener('click', () => {
  editingRoleId = null;
  showForm('添加角色');
  loadActors();
  loadMovies();
});

function editRole(id, role_name, actor_id, movie_id) {
  editingRoleId = id;
  document.getElementById('roleNameInput').value = role_name;
  showForm('编辑角色'); 
  loadActors();
  loadMovies();

}

function deleteRole(id) {
  if (!confirm('确定要删除这个角色吗？')) return;

  fetch(`/roles/${id}`, { method: 'DELETE' })
    .then(res => res.json())
    .then(data => {
      alert(data.message || '删除成功');
      loadRoles();
    })
    .catch(err => {
      console.error('删除失败:', err);
      alert('删除失败');
    });
}

document.getElementById('refreshBtn').addEventListener('click', () => {
  document.getElementById('searchInput').value = '';
  loadRoles();
});

document.getElementById('searchBtn').addEventListener('click', () => {
  const keyword = document.getElementById('searchInput').value;
  loadRoles(keyword);
});

window.onload = () => {
  loadRoles();
};
