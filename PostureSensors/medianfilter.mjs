const data = [15.6, 1216.2, 1216.1, 13.8, 1216.1, 16.9, 17, 1216.1, 1216.1, 15.4, 14, 15.4, 15, 14.8, 1216.1, 15, 15, 1216.1]
const filter_size = 5
 
// Simulate the time-series result after each new sample
for (let i = 0; i < data.length; i++) {
    //console.log(i)  
  const recent_history = data.slice(i - filter_size, i)
  //console.log(recent_history)
  const sorted = recent_history.sort((a,b)=>(a-b))
  //console.log(sorted)
  const median = sorted[Math.floor(sorted.length / 2)]
  //console.log(median)
  if (median) {
    console.log(median)
  }
}