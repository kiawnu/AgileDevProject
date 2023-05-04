const url = 'https://perenual.com/api/species-list?page=1&key=sk-GpRy644963aed0f69653';
const section = document.querySelector('#display-block');

fetch(url)
  .then(response => response.json())
  .then(data => {
    data.data.forEach(species => {
      const li = document.createElement('li');
      const a = document.createElement('a');
      const img = document.createElement('img');
      const h2 = document.createElement('h2');
      const h3 = document.createElement('h3');

      a.href = species.default_image.original_url;
      img.src = species.default_image.medium_url;
      img.alt = species.common_name;
      h2.textContent = species.common_name;
      h3.textContent = species.scientific_name[0];

      a.appendChild(img);
      a.appendChild(h2);
      a.appendChild(h3);
      li.appendChild(a);
      section.appendChild(li);
    });
  })
  .catch(error => console.error(error));
