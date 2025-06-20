let editingCompanyId = null;

function loadCompanies(keyword = '') {
  let url = '/companies/list';
  if (keyword.trim() !== '') {
    url = `/companies/search?keyword=${encodeURIComponent(keyword.trim())}`;
  }

  fetch(url)
    .then(res => res.json())
    .then(data => {
      const tbody = document.querySelector('#companiesTable tbody');
      tbody.innerHTML = '';
      data.forEach(company => {
        const row = document.createElement('tr');
        row.innerHTML = `
          <td>${company.production_company_id}</td>
          <td>${company.name}</td>
          <td>${company.city || ''}</td>
          <td>
            <button onclick="editCompany(${company.production_company_id}, '${company.name}', '${company.city || ''}')">编辑</button>
            <button onclick="deleteCompany(${company.production_company_id})">删除</button>
          </td>
        `;
        tbody.appendChild(row);
      });
    })
    .catch(err => console.error('加载公司失败:', err));
}

function showForm(title) {
  document.getElementById('formTitle').innerText = title;
  document.getElementById('companyForm').style.display = 'block';
}

function hideForm() {
  document.getElementById('companyForm').style.display = 'none';
  document.getElementById('nameInput').value = '';
  document.getElementById('cityInput').value = '';
  editingCompanyId = null;
}

document.getElementById('saveBtn').addEventListener('click', function () {
  const name = document.getElementById('nameInput').value;
  const city = document.getElementById('cityInput').value;

  if (!name) {
    alert('公司名称不能为空');
    return;
  }

  const url = editingCompanyId ? `/companies/${editingCompanyId}` : '/companies/add';
  const method = editingCompanyId ? 'PUT' : 'POST';

  fetch(url, {
    method: method,
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name, city })
  })
    .then(res => res.json())
    .then(data => {
      alert(data.message || '操作成功');
      hideForm();
      loadCompanies();
    })
    .catch(err => {
      console.error('提交失败:', err);
      alert('提交失败');
    });
});

document.getElementById('cancelBtn').addEventListener('click', hideForm);

document.getElementById('addBtn').addEventListener('click', () => {
  editingCompanyId = null;
  showForm('添加公司');
});

function editCompany(id, name, city) {
  editingCompanyId = id;
  document.getElementById('nameInput').value = name;
  document.getElementById('cityInput').value = city;
  showForm('编辑公司');
}

function deleteCompany(id) {
  if (!confirm('确定要删除这个公司吗？')) return;

  fetch(`/companies/${id}`, { method: 'DELETE' })
    .then(res => res.json())
    .then(data => {
      alert(data.message || '删除成功');
      loadCompanies();
    })
    .catch(err => {
      console.error('删除失败:', err);
      alert('删除失败');
    });
}

// 新增搜索框和搜索按钮事件绑定
document.getElementById('refreshBtn').addEventListener('click', () => {
  document.getElementById('searchInput').value = '';
  loadCompanies();
});

document.getElementById('searchBtn').addEventListener('click', () => {
  const keyword = document.getElementById('searchInput').value;
  loadCompanies(keyword);
});

window.onload = () => {
  loadCompanies();
};

