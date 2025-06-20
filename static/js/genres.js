let editingGenreId = null;

function loadGenres(keyword = '') {
  let url = '/genres/list';
  if (keyword.trim() !== '') {
    url = `/genres/search?keyword=${encodeURIComponent(keyword.trim())}`;
  }

  fetch(url)
    .then(res => res.json())
    .then(data => {
      renderGenres(data);
    })
    .catch(err => console.error('加载类型失败:', err));
}

function renderGenres(genres) {
  const tbody = document.querySelector('#genresTable tbody');
  tbody.innerHTML = '';
  genres.forEach(genre => {
    const row = document.createElement('tr');
    row.innerHTML = `
      <td>${genre.genre_id}</td>
      <td>${genre.name}</td>
      <td>
        <button onclick="editGenre(${genre.genre_id}, '${genre.name.replace(/'/g, "\\'")}')">编辑</button>
        <button onclick="deleteGenre(${genre.genre_id})">删除</button>
      </td>
    `;
    tbody.appendChild(row);
  });
}

function showForm(title) {
  document.getElementById('formTitle').innerText = title;
  document.getElementById('genreForm').style.display = 'block';
}

function hideForm() {
  document.getElementById('genreForm').style.display = 'none';
  document.getElementById('nameInput').value = '';
  editingGenreId = null;
}

document.getElementById('saveBtn').addEventListener('click', () => {
  const name = document.getElementById('nameInput').value.trim();
  if (!name) {
    alert('类型名称不能为空');
    return;
  }

  const url = editingGenreId ? `/genres/${editingGenreId}` : '/genres/add';
  const method = editingGenreId ? 'PUT' : 'POST';

  fetch(url, {
    method,
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name })
  })
    .then(res => res.json())
    .then(data => {
      alert(data.message || '操作成功');
      hideForm();
      loadGenres();
    })
    .catch(err => {
      console.error('提交失败:', err);
      alert('提交失败');
    });
});

document.getElementById('cancelBtn').addEventListener('click', hideForm);

document.getElementById('addBtn').addEventListener('click', () => {
  editingGenreId = null;
  showForm('添加类型');
});

function editGenre(id, name) {
  editingGenreId = id;
  document.getElementById('nameInput').value = name;
  showForm('编辑类型');
}

function deleteGenre(id) {
  if (!confirm('确定要删除这个类型吗？')) return;

  fetch(`/genres/${id}`, { method: 'DELETE' })
    .then(res => res.json())
    .then(data => {
      alert(data.message || '删除成功');
      loadGenres();
    })
    .catch(err => {
      console.error('删除失败:', err);
      alert('删除失败');
    });
}

document.getElementById('refreshBtn').addEventListener('click', () => loadGenres(''));

window.onload = () => loadGenres('');


