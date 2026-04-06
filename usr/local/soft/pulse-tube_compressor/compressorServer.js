var {exec} = require("child_process");

function LogCompressorData() {
    //call the code that logs the data
    exec("./compressorLogger.py", (error, stdout, stderr) => {
        if (error) {
            console.log("error", error.message);
            return;
        }
        if (stderr) {
            console.log("stderr", stderr);
            return;
        }
        console.log(stdout);
    });
}
//define the logging interval
var logTime = 1*60*1000; //logging interval in milliseconds (1 minute)
setInterval(LogCompressorData, logTime);
