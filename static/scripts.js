window.setTimeout("document.getElementById('error_alert').style.display='none';", 5000);



function showForm() {
var myForm = document.getElementById("hiddenForm");
if (myForm.style.display === "none") {
  myForm.style.display = "block";
  } else {
    myForm.style.display = "none";
  }
}
