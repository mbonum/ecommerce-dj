var removeBtn = document.getElementsByClassName("rem");
for (var i = 0; i < removeBtn.length; i++) {
  var btn = removeBtn[i];
  btn.addEventListener("click", function (event) {
    var btnClicked = event.target
    btnClicked.parentElement.remove()
  })
}