// search.js — Client-side search using index.json (No API key needed)

let index = [];

async function loadIndex() {
  try {
    const res = await fetch('index.json');
    index = await res.json();
    render(index);
  } catch (e) {
    document.getElementById('no-results').hidden = false;
  }
}

function render(items) {
  const grid = document.getElementById('results');
  const noResults = document.getElementById('no-results');
  grid.innerHTML = '';

  if (items.length === 0) {
    noResults.hidden = false;
    return;
  }
  noResults.hidden = true;

  items.forEach(item => {
    const card = document.createElement('a');
    card.className = 'card';
    card.href = `posts/${item.slug}.html`;
    card.innerHTML = `
      <h3>${item.title}</h3>
      <p>${item.description}</p>
      <div class="tags">
        ${item.tags.map(t => `<span class="tag">${t}</span>`).join('')}
      </div>
    `;
    grid.appendChild(card);
  });
}

function applyFilters() {
  const query = document.getElementById('search').value.toLowerCase();
  const activeBtn = document.querySelector('.filter-btn.active');
  const cat = activeBtn ? activeBtn.dataset.cat : 'all';

  let filtered = index;
  if (cat !== 'all') filtered = filtered.filter(i => i.category === cat);
  if (query)         filtered = filtered.filter(i =>
    i.title.toLowerCase().includes(query) ||
    i.description.toLowerCase().includes(query) ||
    i.tags.join(' ').toLowerCase().includes(query)
  );
  render(filtered);
}

document.getElementById('search').addEventListener('input', applyFilters);

document.querySelectorAll('.filter-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    applyFilters();
  });
});

loadIndex();
