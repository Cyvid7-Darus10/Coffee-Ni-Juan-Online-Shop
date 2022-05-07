var myModal = document.getElementById('myModal')
var myInput = document.getElementById('myInput')

myModal.addEventListener('shown.bs.modal', function () {
  myInput.focus()
})



// var subjectObject = {
//   "Cash on Delivery", "Pick-up", "Online Payment", "Bank Transfer"
// }
// window.onload = function() {
//   var subjectSel = document.getElementById("subject");

//   for (var x in subjectObject) {
//     subjectSel.options[subjectSel.options.length] = new Option(x, x);
//   }
//   subjectSel.onchange = function() {
//     //empty Chapters- and Topics- dropdowns
//     chapterSel.length = 1;
//     topicSel.length = 1;
//     //display correct values
//   }

// }