function updateTimeOptions() {
  const dateSelect = document.getElementById('date-select');
  const timeSelect = document.getElementById('time-select');
  const selectedDate = dateSelect.value;
  const times = Object.keys(data[selectedDate]);

  timeSelect.innerHTML = '';

  times.forEach(time => {
    const option = document.createElement('option');
    option.value = time;
    option.textContent = time;
    timeSelect.appendChild(option);
  });

  updateTable();
  updateChart();
}

function updateTable() {
  const dateSelect = document.getElementById('date-select');
  const timeSelect = document.getElementById('time-select');
  const selectedDate = dateSelect.value;
  const selectedTime = timeSelect.value;
  const testcases = data[selectedDate][selectedTime].testcases;
  const tbody = document.getElementById('data-table').getElementsByTagName('tbody')[0];

  tbody.innerHTML = '';

  testcases.forEach((testcase, index) => {
    const tr = document.createElement('tr');
    const nameTd = document.createElement('td');
    const filePathTd = document.createElement('td');
    const statusTd = document.createElement('td');

    nameTd.textContent = testcase.name;
    nameTd.classList.add('clickable');
    nameTd.onclick = () => showPopup(selectedDate, selectedTime, index);

    filePathTd.textContent = testcase.file_path;
    statusTd.textContent = testcase.outcome;

    switch (testcase.outcome.toLowerCase()) {
      case 'passed':
        nameTd.style.color = 'darkgreen';
        statusTd.style.color = 'darkgreen';
        filePathTd.style.color = 'darkgreen';
        break;
      case 'failed':
      case 'error':
        nameTd.style.color = 'red';
        statusTd.style.color = 'red';
        filePathTd.style.color = 'red';
        break;
      case 'skipped':
        nameTd.style.color = 'darkorange';
        statusTd.style.color = 'darkorange';
        filePathTd.style.color = 'darkorange';
        break;
      default:
        nameTd.style.color = 'black';
        statusTd.style.color = 'black';
        filePathTd.style.color = 'black';
        break;
    }

    tr.appendChild(nameTd);
    tr.appendChild(statusTd);
    tr.appendChild(filePathTd);
    tbody.appendChild(tr);

  });

}

function showPopup(date, time, index) {
  const testcase = data[date][time].testcases[index];
  const popupContent = document.getElementById('popup-content');

  let content = "";

  if (testcase.logs && testcase.logs.length > 0) {
    content += "<div><strong>Logs:</strong></div><ul>";
    testcase.logs.forEach(log => {
      content += `<li>${log}</li>`;
    });
    content += "</ul>";
  }

  if (testcase.reason && testcase.reason.length > 0) {
    content += "<div><strong>Reason:</strong></div><ul>";
    testcase.reason.forEach(reason => {
      content += `<li style="color: red;">${reason}</li>`;
    });
    content += "</ul>";
  }
  popupContent.innerHTML = content;

  document.getElementById('popup').style.display = 'block';
  document.getElementById('overlay').style.display = 'block';
}

function closePopup() {
  document.getElementById('popup').style.display = 'none';
  document.getElementById('overlay').style.display = 'none';
}

google.charts.load('current', { 'packages': ['corechart'] });
google.charts.setOnLoadCallback(initializePage);
let chartData = [
  ["Task", "Count"],
  ["Passed", 0],
  ["Failed", 0],
  ["Skipped", 0],
  ["Error", 0]
];
const options = {
  title: 'Trend VD Chart',
  width: 300,
  height: 200
};
function initializePage() {
  drawChart();
  const dateSelect = document.getElementById('date-select');
  const timeSelect = document.getElementById('time-select');
  dateSelect.addEventListener('change', updateChart);
  timeSelect.addEventListener('change', updateChart);
  timeSelect.addEventListener('change', updateTable);

}

function updateChart() {
  const selectedDate = document.getElementById('date-select').value;
  const selectedTime = document.getElementById('time-select').value;

  const testCases = data[selectedDate][selectedTime].testcases;

  let passedCount = 0;
  let failedCount = 0;
  let skippedCount = 0;
  let errorCount = 0;

  testCases.forEach(testcase => {
    switch (testcase.outcome) {
      case 'passed':
        passedCount++;
        break;
      case 'failed':
        failedCount++;
        break;
      case 'skipped':
        skippedCount++;
        break;
      case 'error':
        errorCount++;
        break;
    }
  });

  chartData = [
    ["Task", "Count"],
    ["Passed", passedCount],
    ["Failed", failedCount],
    ["Skipped", skippedCount],
    ["Error", errorCount]
  ];

  drawChart();
}

function drawChart() {
  console.log(chartData);
  const data = google.visualization.arrayToDataTable(chartData);
  const chart = new google.visualization.PieChart(document.getElementById('piechart'));
  chart.draw(data, options);
}


document.addEventListener('DOMContentLoaded', () => {
  const dateSelect = document.getElementById('date-select');
  const dates = Object.keys(data);

  dates.forEach(date => {
    const option = document.createElement('option');
    option.value = date;
    option.textContent = date;
    dateSelect.appendChild(option);
  });

  updateTimeOptions();
});
'use strict';

class SortableTable {
  constructor(tableNode) {
    this.tableNode = tableNode;

    this.columnHeaders = tableNode.querySelectorAll('thead th');

    this.sortColumns = [];

    for (var i = 0; i < this.columnHeaders.length; i++) {
      var ch = this.columnHeaders[i];
      var buttonNode = ch.querySelector('button');
      if (buttonNode) {
        this.sortColumns.push(i);
        buttonNode.setAttribute('data-column-index', i);
        buttonNode.addEventListener('click', this.handleClick.bind(this));
      }
    }

    this.optionCheckbox = document.querySelector(
      'input[type="checkbox"][value="show-unsorted-icon"]'
    );

    if (this.optionCheckbox) {
      this.optionCheckbox.addEventListener(
        'change',
        this.handleOptionChange.bind(this)
      );
      if (this.optionCheckbox.checked) {
        this.tableNode.classList.add('show-unsorted-icon');
      }
    }
  }

  setColumnHeaderSort(columnIndex) {
    if (typeof columnIndex === 'string') {
      columnIndex = parseInt(columnIndex);
    }

    for (var i = 0; i < this.columnHeaders.length; i++) {
      var ch = this.columnHeaders[i];
      var buttonNode = ch.querySelector('button');
      if (i === columnIndex) {
        var value = ch.getAttribute('aria-sort');
        if (value === 'descending') {
          ch.setAttribute('aria-sort', 'ascending');
          this.sortColumn(
            columnIndex,
            'ascending',
            ch.classList.contains('num')
          );
        } else {
          ch.setAttribute('aria-sort', 'descending');
          this.sortColumn(
            columnIndex,
            'descending',
            ch.classList.contains('num')
          );
        }
      } else {
        if (ch.hasAttribute('aria-sort') && buttonNode) {
          ch.removeAttribute('aria-sort');
        }
      }
    }
  }

  sortColumn(columnIndex, sortValue, isNumber) {
    function compareValues(a, b) {
      if (sortValue === 'ascending') {
        if (a.value === b.value) {
          return 0;
        } else {
          if (isNumber) {
            return a.value - b.value;
          } else {
            return a.value < b.value ? -1 : 1;
          }
        }
      } else {
        if (a.value === b.value) {
          return 0;
        } else {
          if (isNumber) {
            return b.value - a.value;
          } else {
            return a.value > b.value ? -1 : 1;
          }
        }
      }
    }

    if (typeof isNumber !== 'boolean') {
      isNumber = false;
    }

    var tbodyNode = this.tableNode.querySelector('tbody');
    var rowNodes = [];
    var dataCells = [];

    var rowNode = tbodyNode.firstElementChild;

    var index = 0;
    while (rowNode) {
      rowNodes.push(rowNode);
      var rowCells = rowNode.querySelectorAll('th, td');
      var dataCell = rowCells[columnIndex];

      var data = {};
      data.index = index;
      data.value = dataCell.textContent.toLowerCase().trim();
      if (isNumber) {
        data.value = parseFloat(data.value);
      }
      dataCells.push(data);
      rowNode = rowNode.nextElementSibling;
      index += 1;
    }

    dataCells.sort(compareValues);

    // remove rows
    while (tbodyNode.firstChild) {
      tbodyNode.removeChild(tbodyNode.lastChild);
    }

    // add sorted rows
    for (var i = 0; i < dataCells.length; i += 1) {
      tbodyNode.appendChild(rowNodes[dataCells[i].index]);
    }
  }

  /* EVENT HANDLERS */

  handleClick(event) {
    var tgt = event.currentTarget;
    this.setColumnHeaderSort(tgt.getAttribute('data-column-index'));
  }

  handleOptionChange(event) {
    var tgt = event.currentTarget;

    if (tgt.checked) {
      this.tableNode.classList.add('show-unsorted-icon');
    } else {
      this.tableNode.classList.remove('show-unsorted-icon');
    }
  }
}

// Initialize sortable table buttons
window.addEventListener('load', function () {
  var sortableTables = document.querySelectorAll('table.sortable');
  for (var i = 0; i < sortableTables.length; i++) {
    new SortableTable(sortableTables[i]);
  }
});

function searchTable() {
  const input = document.getElementById("searchInput");
  const filter = input.value.toLowerCase();
  const table = document.getElementById("data-table");
  const tr = table.getElementsByTagName("tr");

  for (let i = 1; i < tr.length; i++) {
      const tdArray = tr[i].getElementsByTagName("td");
      let isVisible = false;

      for (let j = 0; j < tdArray.length; j++) {
          const td = tdArray[j];
          if (td) {
              if (td.innerText.toLowerCase().indexOf(filter) > -1) {
                  isVisible = true;
                  break;
              }
          }
      }

      tr[i].style.display = isVisible ? "" : "none";
  }
}