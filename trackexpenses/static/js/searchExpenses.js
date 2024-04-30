const searchField = document.querySelector("#searchField");
const tableOutput = document.querySelector(".table-output");
const appTable = document.querySelector(".app-table");
const paginationContainer = document.querySelector(".pagination-container");
const tableBody = document.querySelector(".table-body");
tableOutput.style.display = "none";

//to detect when the user is typing  we use eventlistener
searchField.addEventListener("keyup", (e) => {
  const searchValue = e.target.value.trim(); //it returns what the user is typing in each keystroke
  if (searchValue.trim().length > 0) {
    paginationContainer.style.display = "none";
    tableBody.innerHTML = "";
    //search_expenses is the  url itself
    fetch("/search_expenses", {
      body: JSON.stringify({
        searchText: searchValue,
      }), //turn js object into correct json
      method: "POST",
    })
      .then((res) => res.json())
      .then((data) => {
        console.log("data", data);
        appTable.style.display = "none";

        tableOutput.style.display = "block";

        if (data.length === 0) {
          tableOutput.innerHTML = "No results found!";
        } else {

          data.forEach((item) => {
            tableBody.innerHTML += `
            <tr>
            <td>${item.date}</td>
            <td>${item.amount}</td>
            <td>${item.category}</td>
            <td>${item.description}</td>


            </tr>
            `;
          });
        }
      });
  } else {
    tableOutput.style.display = "none";
    appTable.style.display = "block";
    paginationContainer.style.display = "block";
    tableBody.innerHTML = "";
    location.reload()

  }
});
