$(document).ready(function () {
var y = document.getElementById("y").value,
  year = document.getElementById("year");
  if (y != null) {
    var numerus = document.createTextNode(romanize(y));
    year.appendChild(numerus);
  }
function romanize (num) {
  if (!+num)
    return false;
  var digits = String(+num).split(""),
    key = ["","C","CC","CCC","CD","D","DC","DCC","DCCC","CM",
           "","X","XX","XXX","XL","L","LX","LXX","LXXX","XC",
           "","I","II","III","IV","V","VI","VII","VIII","IX"],
    roman = "",
    i = 3;
  while (i--)
    roman = (key[+digits.pop() + (i * 10)] || "") + roman;
  return Array(+digits.join("") + 1).join("M") + roman;
}

var date = document.getElementById("launchDate").value;
if (date != null) {
  window.onload = function() {
    countUpFromTime(date, "ctime");
  };
}
  function countUpFromTime(countFrom, id) {
    countFrom = new Date(countFrom).getTime();
    var now = new Date(),
        countFrom = new Date(countFrom),
        timeDifference = (now - countFrom);
    var secondsInADay = 60 * 60 * 1000 * 24,
        secondsInAHour = 60 * 60 * 1000;
    days = Math.floor(timeDifference / (secondsInADay) * 1);
    hours = Math.floor((timeDifference % (secondsInADay)) / (secondsInAHour) * 1);
    var idEl = document.getElementById(id);
    idEl.getElementsByClassName("days")[0].innerHTML = days;
    idEl.getElementsByClassName("hours")[0].innerHTML = hours;
    //romanize(hours);
    // idEl.getElementsByClassName("days")[0].title = days;​
    // idEl.getElementsByClassName("hours")[0].setAttribute("title", hours);​
    clearTimeout(countUpFromTime.interval);
    countUpFromTime.interval = setTimeout(function(){ countUpFromTime(countFrom, id); }, 1000);
  }
})
// d = document.createTextNode(romanize(days)),
// h = document.createTextNode(romanize(hours))
//     idEl.getElementsByClassName("days")[0].innerHTML(romanize(days));
//     idEl.getElementsByClassName("hours")[0].innerHTML(romanize(hours));
//     // idEl.getElementsByClassName("hours")[0].appendChild(h);