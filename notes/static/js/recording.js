window.SpeechRecognition = window.webkitSpeechRecognition || window.SpeechRecognition;
const synth = window.speechSynthesis;
const recognition = new SpeechRecognition();

recognition.lang = 'vi-VN';

const icon = document.querySelector('button.btn-search')

icon.addEventListener('click', () => {
    dictate();
});

const dictate = () => {
    recognition.start();
    recognition.onresult = (event) => {
        const speechToText = event.results[0][0].transcript;
        
        console.log(speechToText)
    
        if (event.results[0].isFinal) {

            window.open(`http://localhost:8000/notes/?text=${speechToText}`, replace=true)
    
            // if (speechToText.includes('what is the weather in')) {
            //     getTheWeather(speechToText);
            // };

        }
    }
}

// const speak = (action) => {
//     utterThis = new SpeechSynthesisUtterance(action());
//     synth.speak(utterThis);
// };

// const getTheWeather = (speech) => {
//     fetch(`http://localhost:8000/notes/?text=hihi`)
//     fetch(`http://api.openweathermap.org/data/2.5/weather?q=${speech.split(' ')[5]}&appid=58b6f7c78582bffab3936dac99c31b25&units=metric`)
//     .then(function(response){
//         return response.json();
//     })
//     .then(function(weather){
//         if (weather.cod === '404') {
//             utterThis = new SpeechSynthesisUtterance(`I cannot find the weather for ${speech.split(' ')[5]}`);
//             synth.speak(utterThis);
//             return;
//         }
//         utterThis = new SpeechSynthesisUtterance(`the weather condition in ${weather.name} is mostly full of ${weather.weather[0].description} at a temperature of ${weather.main.temp} degrees Celcius`);
//         synth.speak(utterThis);
//     });
// };