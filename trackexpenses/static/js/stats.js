//For expenses dashboard
const renderChart = (data, labels) => {
 const ctx = document.getElementById("myChart");

 new Chart(ctx, {
   type: "bar",
   data: {
     labels: labels,
     datasets: [
       {
         label: "Last 3 months expenses",
         data: data,
         borderWidth: 1,
         borderColor: "#3f4242",

         backgroundColor: [
           "rgba(25, 99, 132, 0.5)",
           "rgba(255, 159, 64, 0.5)",
           "rgba(255, 205, 86, 0.5)",
           "rgba(75, 192, 192, 0.5)",
           "rgba(54, 162, 235, 0.5)",
           "rgba(153, 102, 255, 0.5)",
           "rgba(201, 203, 207, 0.5)",
           "rgba(201, 20, 207, 0.5)",
           "rgba(101, 20, 207, 0.5)",
         ],
       },
     ],
   },
   options: {
     title: {
       display: true,
       text: "Expenses by category",
     },
   },
 });
};

const getChartData = () => {
 const showExpense = document.querySelector("#show-expense");
 fetch("/expense_category_summary")
   .then((res) => res.json())
   .then((results) => {
     console.log("results", results);
     showExpense.innerHTML = `Rs${results.total_sum}`;

     const category_data = results.expense_category_data;
     const [label, data] = [
       Object.keys(category_data),
       Object.values(category_data),
     ];

     renderChart(data, label);
   });
};
document.onload = getChartData();
//For income dashboard
const renderChartIncome = (data, labels) => {
 const ctxIncome = document.getElementById("myChartIncome");

 new Chart(ctxIncome, {
   type: "bar",
   data: {
     labels: labels,
     datasets: [
       {
         label: "Last 3 months expenses",
         data: data,
         borderWidth: 1,
         borderColor: "#3f4242",
         backgroundColor: [
           "rgba(25, 99, 132, 0.5)",
           "rgba(255, 159, 64, 0.5)",
           "rgba(255, 205, 86, 0.5)",
         ],
       },
     ],
   },
   options: {
     title: {
       display: true,
       text: "Income by source",
     },
   },
 });
};
//For income overview
const getChartDataIncome = () => {
 const showIncome = document.querySelector("#show-income");

 fetch("/income_source_summary")
   .then((res) => res.json())
   .then((results) => {
     console.log("results", results);
     showIncome.innerHTML = `Rs. ${results.total_sum}`;
     const source_data = results.income_category_data;
     const [label, data] = [
       Object.keys(source_data),
       Object.values(source_data),
     ];

     renderChartIncome(data, label);
   });
};
document.onload = getChartDataIncome();

const renderChartIncomeAll = (data, labels) => {
 const ctxIncomeAll = document.getElementById("myChartIncomeAll");

 new Chart(ctxIncomeAll, {
   type: "line",
   data: {
     labels: labels,
     datasets: [
       {
         label: "Overview of Income by Source",
         data: data,
         borderWidth: 1,
         borderColor: "#3f4242",
         backgroundColor: [
           "rgba(25, 99, 132, 0.5)",
           "rgba(255, 159, 64, 0.5)",
           "rgba(255, 205, 86, 0.5)",
         ],
       },
     ],
   },
   options: {
     title: {
       display: true,
       text: "Income by source",
     },
   },
 });
};
const getChartDataIncomeAll = () => {
 fetch("/income/income_source_summary_all")
   .then((res) => res.json())
   .then((results) => {
     console.log("results", results);

     const source_data = results.income_category_data_all;
     const [label, data] = [
       Object.keys(source_data),
       Object.values(source_data),
     ];

     renderChartIncomeAll(data, label);
   });
};
document.onload = getChartDataIncomeAll();

//Overview below expense
const renderChartExpenseAll = (data, labels) => {
 const ctxExpenseAll = document.getElementById("myChartExpenseAll");

 new Chart(ctxExpenseAll, {
   type: "line",
   data: {
     labels: labels,
     datasets: [
       {
         label: "Overview Expense by Category",
         data: data,
         borderWidth: 1,
         borderColor: "#3f4242",

         backgroundColor: [
           "rgba(25, 99, 132, 0.5)",
           "rgba(255, 159, 64, 0.5)",
           "rgba(255, 205, 86, 0.5)",
           "rgba(75, 192, 192, 0.5)",
           "rgba(54, 162, 235, 0.5)",
           "rgba(153, 102, 255, 0.5)",
           "rgba(201, 203, 207, 0.5)",
           "rgba(201, 20, 207, 0.5)",
           "rgba(101, 20, 207, 0.5)",
         ],
       },
     ],
   },
   options: {
     title: {
       display: true,
       text: "Expenses by category",
     },
   },
 });
};

const getChartDataExpenseAll = () => {
 fetch("income/expense_category_summary_all")
   .then((res) => res.json())
   .then((results) => {
     console.log("results", results);

     const category_data = results.expense_category_data_all;
     const [label, data] = [
       Object.keys(category_data),
       Object.values(category_data),
     ];

     renderChartExpenseAll(data, label);
   });
};
document.onload = getChartDataExpenseAll();
