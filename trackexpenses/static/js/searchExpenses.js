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
// // // searchField.addEventListener("keyup", (e) => {
// // //   const searchValue = e.target.value.trim();

// // //   if (searchValue.length > 0) {
// // //     paginationContainer.style.display = "none";
// // //     tableBody.innerHTML = "";

// // //     fetch("/search_expenses", {
// // //       body: JSON.stringify({
// // //         searchText: searchValue,
// // //       }),
// // //       method: "POST",
// // //     })
// // //       .then((res) => res.json())
// // //       .then((data) => {
// // //         console.log("data", data);
// // //         appTable.style.display = "none";
// // //         tableOutput.style.display = "block";

// // //         if (data.length === 0) {
// // //           tableOutput.innerHTML = "No results found!";
// // //         } else {
// // //           const fragment = document.createDocumentFragment(); // Create a document fragment

// // //           data.forEach((item) => {
// // //             const row = document.createElement("tr"); // Create a table row
// // //             row.innerHTML = `
// // //               <td>${item.date}</td>
// // //               <td>${item.amount}</td>
// // //               <td>${item.category}</td>
// // //               <td>${item.description}</td>
// // //             `;
// // //             fragment.appendChild(row); // Append the row to the fragment
// // //           });

// // //           tableBody.appendChild(fragment); // Append the fragment to the table body
// // //         }
// // //       });
// // //   } else {
// // //     tableOutput.style.display = "none";
// // //     appTable.style.display = "block";
// // //     paginationContainer.style.display = "block";
// // //     tableBody.innerHTML = "";
// // //   }
// // // });
// // // searchField.addEventListener("keyup", (e) => {
// // //   const searchValue = e.target.value.trim();

// // //   if (searchValue.length > 0) {
// // //     paginationContainer.style.display = "none";
// // //     tableBody.innerHTML = "";

// // //     fetch("/search_expenses", {
// // //       body: JSON.stringify({
// // //         searchText: searchValue,
// // //       }),
// // //       method: "POST",
// // //     })
// // //       .then((res) => res.json())
// // //       .then((data) => {
// // //         console.log("data", data);
// // //         appTable.style.display = "none";
// // //         tableOutput.style.display = "block";

// // //         if (data.length === 0) {
// // //           tableOutput.innerHTML = "No results found!";
// // //         } else {
// // //           data.forEach((item) => {
// // //             const row = document.createElement("tr"); // Create a table row

// // //             // Create table cells and populate with data
// // //             const dateCell = document.createElement("td");
// // //             dateCell.textContent = item.date;
// // //             row.appendChild(dateCell);

// // //             const amountCell = document.createElement("td");
// // //             amountCell.textContent = item.amount;
// // //             row.appendChild(amountCell);

// // //             const categoryCell = document.createElement("td");
// // //             categoryCell.textContent = item.category;
// // //             row.appendChild(categoryCell);

// // //             const descriptionCell = document.createElement("td");
// // //             descriptionCell.textContent = item.description;
// // //             row.appendChild(descriptionCell);

// // //             tableBody.appendChild(row); // Append the row to the table body
// // //           });
// // //         }
// // //       });
// // //   } else {
// // //     tableOutput.style.display = "none";
// // //     appTable.style.display = "block";
// // //     paginationContainer.style.display = "block";
// // //     tableBody.innerHTML = "";
// // //   }
// // // });

// // searchField.addEventListener("keyup", (e) => {
// //   const searchValue = e.target.value.trim();

// //   if (searchValue.length > 0) {
// //     paginationContainer.style.display = "none";
// //     tableBody.innerHTML = "";

// //     fetch("/search_expenses", {
// //       body: JSON.stringify({
// //         searchText: searchValue,
// //       }),
// //       method: "POST",
// //     })
// //       .then((res) => res.json())
// //       .then((data) => {
// //         console.log("data", data);
// //         appTable.style.display = "none";
// //         tableOutput.style.display = "block";

// //         if (data.length === 0) {
// //           tableBody.innerHTML = ""; // Clear previous search results
// //           tableOutput.innerHTML = "No results found!";
// //         } else {
// //           data.forEach((item) => {
// //             const row = document.createElement("tr"); // Create a table row

// //             // Create table cells and populate with data
// //             const dateCell = document.createElement("td");
// //             dateCell.textContent = item.date;
// //             row.appendChild(dateCell);

// //             const amountCell = document.createElement("td");
// //             amountCell.textContent = item.amount;
// //             row.appendChild(amountCell);

// //             const categoryCell = document.createElement("td");
// //             categoryCell.textContent = item.category;
// //             row.appendChild(categoryCell);

// //             const descriptionCell = document.createElement("td");
// //             descriptionCell.textContent = item.description;
// //             row.appendChild(descriptionCell);

// //             tableBody.appendChild(row); // Append the row to the table body
// //           });
// //         }
// //       });
// //   } else {
// //     // If search field is empty, clear the table and hide the "No results found!" message
// //     tableOutput.style.display = "none";
// //     appTable.style.display = "block";
//     paginationContainer.style.display = "block";
//     tableBody.innerHTML = ""; // Clear previous search results
//   }
// })