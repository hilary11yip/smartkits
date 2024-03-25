var maxValueInput = document.getElementById('maxValue');
var sampleSizeInput = document.getElementById('sampleSize');
var maxValueNumber = document.getElementById('maxValueNumber');
var sampleSizeNumber = document.getElementById('sampleSizeNumber');

maxValueInput.addEventListener('input', function () {
    maxValueNumber.innerText = maxValueInput.value;
    sampleSizeInput.max = maxValueInput.value - 1;

    //When select total number of questions without number of items to be drawn, set sample size display text and value = 50
    if(sampleSizeNumber.textContent.length === 0){
        sampleSizeInput.value = 50;
    }
    
    else if(sampleSizeInput.value >= sampleSizeInput.max){
        sampleSizeInput.value = sampleSizeInput.max;
    }

    sampleSizeNumber.innerText = sampleSizeInput.value;
});

sampleSizeInput.addEventListener('input', function () {
    sampleSizeNumber.innerText = sampleSizeInput.value;
});