// 加载导演列表
function loadDirectors(keyword = '') {
  let url = '/directors/list';
  if (keyword.trim() !== '') {
    url = `/directors/search?keyword=${encodeURIComponent(keyword.trim())}`;
  }

  fetch(url)
    .then(res => res.json())
    .then(data => {
      const tbody = document.querySelector('#directorsTable tbody');
      tbody.innerHTML = '';
      data.forEach(director => {
        const movies = director.movies ? director.movies : ''; // 显示电影名称
        tbody.innerHTML += `
          <tr>
            <td>${director.director_id}</td>
            <td>${director.name}</td>
            <td>${director.dob || ''}</td>
            <td>${movies}</td> <!-- 新增显示参与电影 -->
            <td>
              <button onclick="editDirector(${director.director_id}, '${escapeQuotes(director.name)}', '${director.dob || ''}', '${director.movie_ids || ''}')">编辑</button>
              <button onclick="deleteDirector(${director.director_id})">删除</button>
            </td>
          </tr>
        `;
      });
    })
    .catch(err => console.error('加载导演失败:', err));
}

// 加载所有电影到“参与电影”多选框
function loadMovies() {
  fetch('/movies/list')
    .then(res => res.json())
    .then(data => {
      const select = document.getElementById('moviesSelect');
      select.innerHTML = '';
      data.forEach(movie => {
        select.innerHTML += `<option value="${movie.movie_id}">${movie.title}</option>`;
      });
    })
    .catch(err => console.error('加载电影失败:', err));
}

// 搜索按钮
document.getElementById('searchBtn').onclick = () => {
  const keyword = document.getElementById('searchInput').value;
  loadDirectors(keyword);
};

// 刷新按钮
document.getElementById('refreshBtn').onclick = () => {
  loadDirectors();
};

// 添加按钮
document.getElementById('addBtn').onclick = () => {
  document.getElementById('formTitle').textContent = '添加导演';
  document.getElementById('nameInput').value = '';
  document.getElementById('dobInput').value = '';
  document.getElementById('moviesSelect').selectedIndex = -1;
  document.getElementById('directorForm').style.display = 'block';
  currentEditingId = null;
};

// 取消按钮
document.getElementById('cancelBtn').onclick = () => {
  document.getElementById('directorForm').style.display = 'none';
};

// 保存按钮
document.getElementById('saveBtn').onclick = () => {
  const name = document.getElementById('nameInput').value.trim();
  const dob = document.getElementById('dobInput').value;
  const selectedMovies = Array.from(document.getElementById('moviesSelect').selectedOptions)
                              .map(option => parseInt(option.value));

  if (!name) {
    alert('导演姓名不能为空');
    return;
  }

  const data = { name, dob, movies: selectedMovies };
  let url = '/directors/add';
  let method = 'POST';

  if (currentEditingId !== null) {
    url = `/directors/${currentEditingId}`;
    method = 'PUT';
  }

  fetch(url, {
    method: method,
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  })
  .then(res => res.json())
  .then(result => {
    alert(result.message || '操作成功');
    document.getElementById('directorForm').style.display = 'none';
    loadDirectors();
  })
  .catch(err => console.error('保存失败:', err));
};

// 编辑导演
let currentEditingId = null;
function editDirector(id, name, dob, movieIds) {
  currentEditingId = id;
  document.getElementById('formTitle').textContent = '编辑导演';
  document.getElementById('nameInput').value = name;
  document.getElementById('dobInput').value = dob;

  const movieSelect = document.getElementById('moviesSelect');
  const movieIdArray = movieIds ? movieIds.split(',') : [];
  Array.from(movieSelect.options).forEach(option => {
    option.selected = movieIdArray.includes(option.value);
  });

  document.getElementById('directorForm').style.display = 'block';
}

// 删除导演
function deleteDirector(id) {
  if (confirm('确定要删除这个导演吗？')) {
    fetch(`/directors/${id}`, { method: 'DELETE' })
      .then(res => res.json())
      .then(result => {
        alert(result.message);
        loadDirectors();
      })
      .catch(err => console.error('删除失败:', err));
  }
}

// 防止引号导致的HTML错误
function escapeQuotes(str) {
  return str.replace(/'/g, "\\'");
}

// 页面加载时执行
window.onload = () => {
  loadDirectors();
  loadMovies();
};


