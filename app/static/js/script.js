let page = 1;
let url = `https://perenual.com/api/species-list?page=${page}&key=sk-GpRy644963aed0f69653`;
const section = document.querySelector("#display-block");
const searchContainer = document.querySelector("#searchContainer");
let replacedUrl = url.replace(/\//g, ",").replace("?", "@");

fetch(`/cache/${replacedUrl}`)
  .then((response) => response.json())
  .then((data) => {
    data = JSON.parse(data);
    data.data.forEach((species) => {
      const li = document.createElement("li");
      const a = document.createElement("a");
      const img = document.createElement("img");
      const h2 = document.createElement("h2");
      const h3 = document.createElement("h3");

      li.setAttribute("class", "species");

      a.href = `/info/${species.id}`;
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

    page++;
  })
  .catch((error) => {
    console.log("First fetch failed:", error);
    APIfetch();
  });

const APIfetch = () => {
  const updatedUrl = url.replace(/page=\d+/, `page=${page}`);

  fetch(updatedUrl)
    .then((response) => response.json())
    .then((data) => {
      console.log(`API pung!!`);
      fetch(`/cache/${replacedUrl}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      })
        .then((response) => response.json())
        .then((data) => console.log(data))
        .catch((error) => console.error(error));

      data.data.forEach((species) => {
        const li = document.createElement("li");
        const a = document.createElement("a");
        const img = document.createElement("img");
        const h2 = document.createElement("h2");
        const h3 = document.createElement("h3");

        li.setAttribute("class", "species");

        a.href = `/info/${species.id}`;
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

      page++;
      replacedUrl = updatedUrl.replace(/\//g, ",").replace("?", "@");
    })
    .catch((error) => console.error(error));
};

const plantList = document.querySelector("#display-block");
const plantSearch = document.getElementById("searchBox");
function searchItems() {
  for (item of plantList.getElementsByTagName("li")) {
    if (
      item.innerHTML.includes(plantSearch.value) ||
      item.innerHTML.toUpperCase().includes(plantSearch.value.toUpperCase())
    ) {
      item.removeAttribute("class", "hidden");
      item.setAttribute("class", "species");
    } else {
      item.setAttribute("class", "hidden");
    }
  }
}
plantSearch.addEventListener("input", searchItems);


window.addEventListener("scroll", () => {
  const { scrollTop, scrollHeight, clientHeight } = document.documentElement;
  if (scrollTop + clientHeight >= scrollHeight) {
    APIfetch();
  }
});
