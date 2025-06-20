let editingNarrationId = null;

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
    })
    .catch(err => console.error('加载演员失败:', err));
}

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
    })
    .catch(err => console.error('加载电影失败:', err));
}

function loadNarrations(keyword = '') {
  let url = '/narrations/list';
  if (keyword.trim() !== '') {
    url = `/narrations/search?keyword=${encodeURIComponent(keyword.trim())}`;
  }

  fetch(url)
    .then(res => res.json())
    .then(data => {
      const tbody = document.querySelector('#narrationsTable tbody');
      tbody.innerHTML = '';
      data.forEach(n => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
          <td>${n.narration_id}</td>
          <td>${n.content}</td>
          <td>${n.actor_name || ''}</td>
          <td>${n.movie_title || ''}</td>
          <td>
            <button onclick="editNarration(${n.narration_id})">编辑</button>
            <button onclick="deleteNarration(${n.narration_id})">删除</button>
          </td>
        `;
        tbody.appendChild(tr);
      });
    })
    .catch(err => console.error('加载旁白失败:', err));
}

function showForm(title) {
  document.getElementById('formTitle').textContent = title;
  document.getElementById('narrationForm').style.display = 'block';
}

function hideForm() {
  document.getElementById('narrationForm').style.display = 'none';
  document.getElementById('contentInput').value = '';
  document.getElementById('actorSelect').value = '';
  document.getElementById('movieSelect').value = '';
  editingNarrationId = null;
}

document.getElementById('saveBtn').addEventListener('click', () => {
  const content = document.getElementById('contentInput').value.trim();
  const actor_id = document.getElementById('actorSelect').value || null;
  const movie_id = document.getElementById('movieSelect').value;

  if (!content) {
    alert('内容不能为空');
    return;
  }
  if (!movie_id) {
    alert('请选择电影');
    return;
  }

  const data = { content, actor_id, movie_id };

  const url = editingNarrationId ? `/narrations/${editingNarrationId}` : '/narrations/add';
  const method = editingNarrationId ? 'PUT' : 'POST';

  fetch(url, {
    method: method,
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  })
    .then(res => res.json())
    .then(data => {
      alert(data.message || '操作成功');
      hideForm();
      loadNarrations();
    })
    .catch(err => {
      console.error('提交失败:', err);
      alert('提交失败');
    });
});

document.getElementById('cancelBtn').addEventListener('click', hideForm);

document.getElementById('addBtn').addEventListener('click', () => {
  editingNarrationId = null;
  showForm('添加旁白');
});

function editNarration(id) {
  fetch('/narrations/list')
    .then(res => res.json())
    .then(data => {
      const narr = data.find(n => n.narration_id === id);
      if (narr) {
        editingNarrationId = id;
        showForm('编辑旁白');
        document.getElementById('contentInput').value = narr.content;
        document.getElementById('actorSelect').value = narr.actor_id || '';
        document.getElementById('movieSelect').value = narr.movie_id || '';
      } else {
        alert('未找到该旁白');
      }
    })
    .catch(err => console.error('获取旁白信息失败:', err));
}

function deleteNarration(id) {
  if (!confirm('确定删除这条旁白吗？')) return;

  fetch(`/narrations/${id}`, { method: 'DELETE' })
    .then(res => res.json())
    .then(data => {
      alert(data.message || '删除成功');
      loadNarrations();
    })
    .catch(err => {
      console.error('删除失败:', err);
      alert('删除失败');
    });
}

document.getElementById('searchBtn').addEventListener('click', () => {
  const keyword = document.getElementById('searchInput').value;
  loadNarrations(keyword);
});

document.getElementById('refreshBtn').addEventListener('click', () => {
  document.getElementById('searchInput').value = '';
  loadNarrations();
});

window.onload = () => {
  loadActors();
  loadMovies();
  loadNarrations();
  hideForm();
};


