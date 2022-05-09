var curDate=new Date().toLocaleDateString(navigator.language,{ weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' });

function printDate() {
document.getElementById("jsdate").innerHTML = curDate.toString();
}
