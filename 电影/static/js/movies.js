let editingMovieId = null;

function loadMovies(keyword = '') {
  let url = '/movies/list';
  if (keyword.trim() !== '') {
    url = `/movies/search?keyword=${encodeURIComponent(keyword.trim())}`;
  }

  fetch(url)
    .then(res => res.json())
    .then(data => {
      const tbody = document.querySelector('#moviesTable tbody');
      tbody.innerHTML = '';
      data.forEach(movie => {
        const genres = movie.genres ? movie.genres.split(',').join(', ') : '';
        const directors = movie.directors ? movie.directors.split(',').join(', ') : '';
        tbody.innerHTML += `
          <tr>
            <td>${movie.movie_id}</td>
            <td>${movie.title}</td>
            <td>${movie.release_year}</td>
            <td>${movie.duration}</td>
            <td>${movie.company_name || ''}</td>
            <td>${genres}</td>
            <td>${directors}</td>
            <td>
              <button onclick="editMovie(${movie.movie_id}, '${escapeQuotes(movie.title)}', ${movie.release_year}, ${movie.duration}, ${movie.production_company_id || 'null'}, '${escapeQuotes(movie.synopsis || '')}', '${movie.genre_ids || ''}', '${movie.director_ids || ''}')">编辑</button>
              <button onclick="deleteMovie(${movie.movie_id})">删除</button>
            </td>
          </tr>
        `;
      });
    })
    .catch(err => console.error('加载电影失败:', err));
}

function showForm(title) {
  document.getElementById('formTitle').innerText = title;
  document.getElementById('movieForm').style.display = 'block';
}

function hideForm() {
  document.getElementById('movieForm').style.display = 'none';
  // 清空表单
  document.getElementById('titleInput').value = '';
  document.getElementById('releaseYearInput').value = '';
  document.getElementById('durationInput').value = '';
  document.getElementById('companySelect').value = '';
  document.getElementById('synopsisInput').value = '';
  // 复选框多选清空
  document.querySelectorAll('input[name="genresCheckbox"]').forEach(cb => cb.checked = false);
  document.querySelectorAll('input[name="directorsCheckbox"]').forEach(cb => cb.checked = false);
  editingMovieId = null;
}

document.getElementById('saveBtn').addEventListener('click', function () {
  const title = document.getElementById('titleInput').value.trim();
  const release_year = Number(document.getElementById('releaseYearInput').value);
  const duration = Number(document.getElementById('durationInput').value);
  const production_company_id = Number(document.getElementById('companySelect').value) || null;
  const synopsis = document.getElementById('synopsisInput').value.trim();

  if (!title) {
    alert('电影标题不能为空');
    return;
  }
  if (!release_year || !duration) {
    alert('上映年份和时长必须填写有效数字');
    return;
  }

  // 收集选中的类别和导演id
  const genres = Array.from(document.querySelectorAll('input[name="genresCheckbox"]:checked')).map(cb => Number(cb.value));
  const directors = Array.from(document.querySelectorAll('input[name="directorsCheckbox"]:checked')).map(cb => Number(cb.value));

  const url = editingMovieId ? `/movies/${editingMovieId}` : '/movies/add';
  const method = editingMovieId ? 'PUT' : 'POST';

  fetch(url, {
    method: method,
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ title, release_year, duration, production_company_id, synopsis, genres, directors })
  })
    .then(res => res.json())
    .then(data => {
      alert(data.message || '操作成功');
      hideForm();
      loadMovies();
    })
    .catch(err => {
      console.error('提交失败:', err);
      alert('提交失败');
    });
});

document.getElementById('cancelBtn').addEventListener('click', hideForm);

document.getElementById('addBtn').addEventListener('click', () => {
  editingMovieId = null;
  showForm('添加电影');
});

// 编辑电影时，填充表单
function editMovie(id, title, release_year, duration, production_company_id, synopsis, genre_ids, director_ids) {
  editingMovieId = id;
  document.getElementById('titleInput').value = title;
  document.getElementById('releaseYearInput').value = release_year;
  document.getElementById('durationInput').value = duration;
  document.getElementById('companySelect').value = production_company_id || '';
  document.getElementById('synopsisInput').value = synopsis;
  document.querySelectorAll('input[name="genresCheckbox"]').forEach(cb => cb.checked = false);
  document.querySelectorAll('input[name="directorsCheckbox"]').forEach(cb => cb.checked = false);

  if (genre_ids) {
    genre_ids.split(',').forEach(id => {
      const cb = document.querySelector(`input[name="genresCheckbox"][value="${id}"]`);
      if (cb) cb.checked = true;
    });
  }
  if (director_ids) {
    director_ids.split(',').forEach(id => {
      const cb = document.querySelector(`input[name="directorsCheckbox"][value="${id}"]`);
      if (cb) cb.checked = true;
    });
  }

  showForm('编辑电影');
}

function deleteMovie(id) {
  if (!confirm('确定要删除这部电影吗？')) return;

  fetch(`/movies/${id}`, { method: 'DELETE' })
    .then(res => res.json())
    .then(data => {
      alert(data.message || '删除成功');
      loadMovies();
    })
    .catch(err => {
      console.error('删除失败:', err);
      alert('删除失败');
    });
}

// 刷新和搜索
document.getElementById('refreshBtn').addEventListener('click', () => {
  document.getElementById('searchInput').value = '';
  loadMovies();
});

document.getElementById('searchBtn').addEventListener('click', () => {
  const keyword = document.getElementById('searchInput').value;
  loadMovies(keyword);
});

window.onload = () => {
  loadMovies();
};

// 辅助函数：防止字符串中的单引号/双引号破坏html模板
function escapeQuotes(str) {
  if (!str) return '';
  return str.replace(/\\/g, '\\\\').replace(/'/g, "\\'").replace(/"/g, '\\"');
}



