let editingActorId = null;

// 加载所有演员
function loadActors() {
  fetch('/actors/list')
    .then(res => res.json())
    .then(data => {
      renderActors(data);
    })
    .catch(err => console.error('加载演员失败:', err));
}

// 渲染演员表格
function renderActors(data) {
  const tbody = document.querySelector('#actorsTable tbody');
  tbody.innerHTML = '';
  data.forEach(actor => {
    const dobStr = actor.dob ? actor.dob : '';
    const row = document.createElement('tr');
    row.innerHTML = `
      <td>${actor.actor_id}</td>
      <td>${actor.name}</td>
      <td>${dobStr}</td>
      <td>
        <button onclick="editActor(${actor.actor_id}, '${actor.name.replace(/'/g, "\\'")}', '${dobStr}')">编辑</button>
        <button onclick="deleteActor(${actor.actor_id})">删除</button>
        <button onclick="viewActorDetail(${actor.actor_id})">详情</button>
      </td>
    `;
    tbody.appendChild(row);
  });
}

// 搜索演员
document.getElementById('searchBtn').addEventListener('click', () => {
  const keyword = document.getElementById('searchInput').value.trim();
  if (!keyword) {
    loadActors(); // 搜索框空则加载所有
    return;
  }
  fetch(`/actors/search?keyword=${encodeURIComponent(keyword)}`)
    .then(res => res.json())
    .then(data => {
      renderActors(data);
    })
    .catch(err => console.error('搜索失败:', err));
});

// 展示表单
function showForm(title) {
  document.getElementById('formTitle').innerText = title;
  document.getElementById('actorForm').style.display = 'block';
}

// 隐藏表单
function hideForm() {
  document.getElementById('actorForm').style.display = 'none';
  document.getElementById('nameInput').value = '';
  document.getElementById('dobInput').value = '';
  editingActorId = null;
}

// 保存（添加或更新）
document.getElementById('saveBtn').addEventListener('click', () => {
  const name = document.getElementById('nameInput').value.trim();
  const dob = document.getElementById('dobInput').value;

  if (!name) {
    alert('演员姓名不能为空');
    return;
  }

  const url = editingActorId ? `/actors/${editingActorId}` : '/actors/add';
  const method = editingActorId ? 'PUT' : 'POST';

  fetch(url, {
    method: method,
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name, dob })
  })
    .then(res => res.json())
    .then(data => {
      alert(data.message || '操作成功');
      hideForm();
      loadActors();
    })
    .catch(err => {
      console.error('提交失败:', err);
      alert('提交失败');
    });
});

// 取消
document.getElementById('cancelBtn').addEventListener('click', hideForm);

// 添加按钮
document.getElementById('addBtn').addEventListener('click', () => {
  editingActorId = null;
  showForm('添加演员');
});

// 编辑按钮
function editActor(id, name, dob) {
  editingActorId = id;
  document.getElementById('nameInput').value = name;
  document.getElementById('dobInput').value = dob;
  showForm('编辑演员');
}

// 删除
function deleteActor(id) {
  if (!confirm('确定要删除这个演员吗？')) return;

  fetch(`/actors/${id}`, { method: 'DELETE' })
    .then(res => res.json())
    .then(data => {
      alert(data.message || '删除成功');
      loadActors();
    })
    .catch(err => {
      console.error('删除失败:', err);
      alert('删除失败');
    });
}

// 查看详情
function viewActorDetail(id) {
  fetch(`/actors/detail/${id}`)
    .then(res => {
      if (!res.ok) {
        throw new Error(`服务器返回状态码 ${res.status}`);
      }
      return res.json();
    })
    .then(data => {
      if (data.error) {
        alert(data.error);
        return;
      }
      if (!data.actor) {
        alert('未获取到演员信息');
        return;
      }

      const actor = data.actor;
      const roles = data.roles || [];
      const narrations = data.narrations || [];

      let message = `演员ID: ${actor.actor_id}\n姓名: ${actor.name}\n出生日期: ${actor.dob || '未知'}\n\n`;

      if (roles.length > 0) {
        message += '角色列表:\n';
        roles.forEach(role => {
          message += ` - 角色名: ${role.role_name}, 电影: ${role.title}\n`;
        });
      } else {
        message += '无角色信息\n';
      }

      if (narrations.length > 0) {
        message += '\n旁白列表:\n';
        narrations.forEach(narration => {
          message += ` - 内容: ${narration.content}, 电影: ${narration.title}\n`;
        });
      } else {
        message += '无旁白信息\n';
      }

      alert(message);
    })
    .catch(err => {
      console.error('获取详情失败:', err);
      alert('获取详情失败');
    });
}



document.getElementById('refreshBtn').addEventListener('click', loadActors);

window.onload = loadActors;





















