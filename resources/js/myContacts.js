

// EXTRA CREDIT! - sort by all columns
function sortBy(h) {
  let tbl = document.getElementById('contact_table');
  let rows = tbl.getElementsByTagName('tr');
  let names = [];

  // Referenced from: https://stackoverflow.com/questions/12752834/read-the-first-column-values-of-a-html-table-with-jquery
  for (let i = 1; i < rows.length; i++) {
    names.push(rows[i].cells[h].innerText);
  }

  // Referenced from: https://www.w3schools.com/jsref/jsref_sort.asp
  names.sort();

  for (let i = 0; i < names.length; i++) {
    for (let j = 1; j < rows.length; j++) {
      if (names[i] == rows[j].cells[h].innerText) {
        let row = rows[j];
        // Referenced from: https://www.w3schools.com/jsref/met_table_insertrow.asp
        tbl.deleteRow(j);
        // Referenced from: https://stackoverflow.com/questions/18333427/how-to-insert-a-row-in-an-html-table-body-in-javascript
        tbl.appendChild(row);
      } 
    }
  }
}

function changeImage(newImage) {
  let img = document.getElementById('img_top');
  img.src=newImage;  
}

// console.log(document.getElementsByTagName('th'));
// table.querySelector('#header_name').addEventListener('click', function(){sortBy(0);});



