let RunSentimentAnalysis = () => {
    let textToAnalyze = document.getElementById("textToAnalyze").value;

    let xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState === 4) {
            let responseElement = document.getElementById("system_response");
            responseElement.style.display = "block";
            if (this.status === 200) {
                responseElement.style.backgroundColor = "#e8f4fd";
                responseElement.style.color = "#0c5460";
                responseElement.style.border = "1px solid #bee5eb";
                responseElement.innerHTML = this.responseText;
            } else {
                responseElement.style.backgroundColor = "#f8d7da";
                responseElement.style.color = "#721c24";
                responseElement.style.border = "1px solid #f5c6cb";
                responseElement.innerHTML = this.responseText;
            }
        }
    };
    xhttp.open("GET", "emotionDetector?textToAnalyze=" + encodeURIComponent(textToAnalyze), true);
    xhttp.send();
};
