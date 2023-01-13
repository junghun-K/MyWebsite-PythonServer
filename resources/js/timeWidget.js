// referenced from: https://stackoverflow.com/questions/3830244/how-to-get-the-current-date-or-and-time-in-seconds

function timeUntil(currentTime) {
  // Date(2022, 12, 22)
  const endOfSem = new Date(2022, 11, 22);
  // console.log(endOfSem);

  let result = endOfSem - currentTime;
  if (result <= 0) {
    return result;
  }

  let seconds = Math.floor(result/1000);

  let days = Math.floor(seconds/86400);
  seconds = seconds % 86400;

  let hours = Math.floor(seconds/3600);
  seconds = seconds % 3600;

  let minutes = Math.floor(seconds/60);
  
  seconds = seconds % 60;

  return {days: days, hours: hours, minutes: minutes, seconds: seconds};
} 

function showTime() {  
  let text = "";
  let current = Date.now();
  let result = timeUntil(current);

  // Check if the semester is over or not!
  if (result <= 0) {
    text = "Semester is over!"
  } else {
    text = result['days']+' Days '+result['hours']+' Hours '+result['minutes']+' Minutes '+result['seconds']+' Seconds';
  }

  document.getElementById('timeResult').innerText = text;
}

window.addEventListener("load", function () {
  this.setInterval(showTime, 1000);
});