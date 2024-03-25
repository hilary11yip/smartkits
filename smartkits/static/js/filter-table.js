function filterTable() {
  const subjectSelect = document.getElementById("subjectSelect");
  const moduleSelect = document.getElementById("moduleSelect");
  const keywordInput = document.getElementById("keywordInput");
  const meaningInput = document.getElementById("meaningInput");
  const dataTable = document.getElementById("dataTable");
  const rows = dataTable.getElementsByTagName("tr");
  var found = false;
  var counter = 0;

  for (let i = 1; i < rows.length; i++) {
    const row = rows[i];
    const subjectCell = row.getElementsByTagName("td")[0];
    const moduleCell = row.getElementsByTagName("td")[1];
    const keywordCell = row.getElementsByTagName("td")[2];
    const meaningCell = row.getElementsByTagName("td")[3];

    const subjectFilter = subjectSelect.value.toLowerCase();
    const moduleFilter = moduleSelect.value.toLowerCase();
    const keywordFilter = keywordInput.value.toLowerCase();
    const meaningFilter = meaningInput.value.toLowerCase();

    const subjectMatch = (subjectFilter === "") || (subjectCell.textContent.toLowerCase() === subjectFilter);
    const moduleMatch = (moduleFilter === "") || (moduleCell.textContent.toLowerCase() === moduleFilter);
    const keywordMatch = (keywordFilter === "") || (keywordCell.textContent.toLowerCase().includes(keywordFilter));
    const meaningMatch = (meaningFilter === "") || (meaningCell.textContent.toLowerCase().includes(meaningFilter));

    if (subjectMatch && moduleMatch && keywordMatch && meaningMatch) {
      row.style.display = "";
      found = true;
      counter ++;
    } else {
      row.style.display = "none";
    }
  }

  var resultCountMessage = document.getElementById("resultCountMessage");

  if(counter == 1){
    resultCountMessage.textContent = "There is " + counter + " related result(s).";
  }
  else{
    resultCountMessage.textContent = "There are " + counter + " related result(s).";
  }
}