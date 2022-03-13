//javascript to be used throughout website

//redirects to homepage ie index.html
function toHome(){
    window.location.replace("/");
}

//INDEX.HTML
$('.carousel').carousel({
    interval: 10000
});


//REGISTER.HTML
function validateUsername(){
    if($('.required').html() == None){
        return false;
    }else{
        return true;
    }
}


//QUIZ.HTML
$("#questions").ready(loadQuestion);
var current_q;
var questions;
var quiz_title;
var answers = [];

//initialises question, checks length and sets message to be presented to the user in the form of a question
function loadQuestion(){
    questions = $("#questions").children();

    for(i = 1; i < questions.length; i++){
        $(questions[i]).addClass("question-hidden");
    }

    current_q = 1;

    quiz_title = $("#quiz-title").html();
    var message = quiz_title + ": Question " + current_q + " of " + questions.length;
    $("#quiz-title").html(message);

//submits question upon clicking
    if(questions.length == 1){
        $("#nextQuestionButton").attr('value', 'Submit');
        $("#nextQuestionButton").attr('onclick', 'submitQuiz()');
    }
}

//iterates to the next question
function nextQuestion(){

    var answer = $(questions[current_q-1]).find('input').val();
    answers.push(answer);

    current_q += 1;

    if(current_q == questions.length){
        //Final question
        $("#nextQuestionButton").attr('value', 'Submit');
        $("#nextQuestionButton").attr('onclick', 'submitQuiz()');
    }else if(current_q == 2){
        $("#prevQuestionButton").removeClass("hidden");
    }

    var message = quiz_title + ": Question " + current_q + " of " + questions.length;
    $("#quiz-title").html(message);

    $(questions[current_q-2]).removeClass("question-visible");
    $(questions[current_q-2]).addClass("question-hidden");
    $(questions[current_q-1]).removeClass("question-hidden");
    $(questions[current_q-1]).addClass("question-visible");

}

//moves to the previous question
function prevQuestion(){
    current_q -= 1;

    if(current_q == 1){
        //Going back to first question
        $("#prevQuestionButton").addClass("hidden");
    }

    var message = quiz_title + ": Question " + current_q + " of " + questions.length;
    $("#quiz-title").html(message);

    $(questions[current_q-1]).removeClass("question-hidden");
    $(questions[current_q-1]).addClass("question-visible");
    $(questions[current_q]).removeClass("question-visible");
    $(questions[current_q]).addClass("question-hidden");
}
//testing
function handleMarking(data){
    console.log(data);
}

function submitQuiz(){

    var answer = $(questions[current_q-1]).find('input').val();
    answers.push(answer);

    //Handle submit form
    jsonResults = [{"title": quiz_title}];

    for(i = 0; i < answers.length; i++){
        jsonResults.push({
            "question": $(questions[i]).find('p').html(),
            "answer": answers[i]
        });
    }

    //result = $.post( "/submit_quiz", JSON.stringify(jsonResults));

    post_quiz(jsonResults);


    $("#prevQuestionButton").addClass("hidden");
    $("#nextQuestionButton").addClass("hidden");
    $("#questions").addClass("hidden");

}

//parse results
function post_quiz(results){
    $.ajax({
        type: "POST",
        url: "/submit_quiz",
        data: JSON.stringify(results),
        contentType: "text/json; charset=utf-8",
        dataType: "text",
        success: function (msg) {
            handleFeedback(msg);
        }
    });
}

//display userfeedback in a friendlier format 
function handleFeedback(data){
    $("#feedback-div").removeClass("hidden");

    data = JSON.parse(data);

    for (var key in data){
        if (key != 'score'){
            var style;

            var m = data[key][0].replace(/\s/g, '').toLowerCase();
            var u = data[key][1].replace(/\s/g, '').toLowerCase();

            if(u != m){
                style = "background-color: rgba(219, 76, 76, 0.2);"
            }else{
                style = "background-color: rgba(85, 219, 76, 0.2);"
            }

            var new_row = "<tr style='"+style+"'><td>"+key+"</td><td>"+data[key][0]+"</td><td>"+data[key][1]+"</td></tr>";
            $("#feedback").append(new_row);
        }
    };

    var score = "<p>Well done! You scored "+data['score'][0]+" out of "+data['score'][1]+".</p>"

    $("#feedback-div").append(score);
}


//RESULT.HTML

const labels = [];
const dataPoints = [];

function addData(user_data){
    json = JSON.parse(user_data);

    json = json[0];

    const data = {
        labels: labels,
        datasets: [],
    };

    for(var i in json){
        for(var x = 1; x < json[i].length; x++){
            if(!labels.includes(json[i][x]["time"])){
                index = indexIntoSortedArray(labels, json[i][x]["time"]);
                labels.splice(index, 0, json[i][x]["time"]);
            }
        }
    }

    //labels[labels.length] = "";

    for(var i in json){      
        
        dataPoints[i] = [];

        r = Math.floor(Math.random()*255);
        g = Math.floor(Math.random()*255);
        b = Math.floor(Math.random()*255);
        colour = 'rgb(' + r + ', ' + g + ', ' + b + ')';

        for(var x = 1; x < json[i].length; x++){
            index = indexIntoSortedArray(labels, json[i][x]["time"]);
            //labels.splice(index, 0, json[i][x]["time"]);

            odds = json[i][x]["odds"];

            dataPoints[i][index] = odds;
        }


        data["datasets"].push({
            label: json[i][0]["pick"] + " to win",
            backgroundColor: json[i][0]["colour"],
            borderColor: json[i][0]["colour"],
            pointBorderColor: json[i][0]["accent"],
            pointRadius: 0,
            data: dataPoints[i],
            spanGaps: true
        })
    }

    function indexIntoSortedArray(array, value) {
        var low = 0,
            high = array.length;
    
        while (low < high) {
            var mid = (low + high) >>> 1;
            if (array[mid] < value) low = mid + 1;
            else high = mid;
        }
        return low;
    }

    const config = {
        type: 'line',
        data,
        options: {
            plugins: {
                title: {
                    display: false,
                    text: 'Current Listings'
                },
                subtitle: {
                    display: true,
                    text: 'Your best odds if you bet: '
                }
            },
            responsive: true,
            scales: {
                yAxes: {
                    title: {
                        display: true,
                        text: "Best Odds ($)",
                        font: {
                            size: 15
                        }
                    },
                    ticks: {
                        precision: 0
                    }
                },
                xAxes: {
                    title: {
                        display: true,
                        text: "Time",
                        font: {
                            size: 15
                        }
                    },
                    ticks: {
                        precision: 0,
                    },
                    displayFormats: {
                        
                    },
                },
            },
            interaction: {
                intersect: false,
                mode: "index",
            }
        }
    };

    var myChart = new Chart(
        document.getElementById("eventChart").getContext("2d"),
        config
      );
}

function drawResults(event_id){
    if($("#eventChart").length > 0 ){
        path = `${location.origin}/get_event_json/` + event_id;
        $.get(path, addData);
    }
}


//CREATE A LISTING POPUP
function createListing(event_id){
    $("#createListingPopup").removeClass("hidden");

    $("#pick_selector").trigger('input');
    updateReturn();
}

function createListingClose(){
    $("#createListingPopup").addClass("hidden");
}

//Update reciprical odds when user enters odds
$(document).on('keyup mouseup', '#user_odds', function() {  
    user_odds = $(this).val();
    their_odds = (1/user_odds + 1).toFixed(2);
    $('#their_odds').val(their_odds);  
    
    //Change return amount
    updateReturn();                                                                                                              
});

$(document).on('keyup mouseup', '#their_odds', function() {  
    their_odds = $(this).val();
    user_odds = (1/their_odds + 1).toFixed(2);
    $('#user_odds').val(user_odds);  
    
    //Change return amount
    updateReturn();  
});

$(document).on('keyup mouseup', '#amount', function() {  
    //Change return amount
    updateReturn();  
});

function updateReturn(){
    //Change return amount
    current_amount = $("#amount").val();
    user_odds = $("#user_odds").val();
    $('#return').html("Return: $" + current_amount * user_odds);   
}


//SET BEST ODDS FOR OPTION ON CHANGE
$(document).on('input', '#pick_selector', function() {  
    best_odds = $('option:selected', this).attr('data-best_odds');
    $("#best_odds").html("Current best odds offered: $" + best_odds);
});