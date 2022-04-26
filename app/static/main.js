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


//EVENT.HTML

const labels = [];
const dataPoints = [];

function buildChart(user_data){
    json = JSON.parse(user_data);

    json = json[0];

    const data = {
        datasets: [],
    };

    for(var i in json){      
        
        dataPoints[i] = [];

        r = Math.floor(Math.random()*255);
        g = Math.floor(Math.random()*255);
        b = Math.floor(Math.random()*255);
        colour = 'rgb(' + r + ', ' + g + ', ' + b + ')';

        for(var x = 1; x < json[i].length; x++){

            odds = json[i][x]["odds"];
            time = json[i][x]["time"];
            entry = {x: time, y: odds};

            dataPoints[i].push(entry);
        }

        data["datasets"].push({
            label: json[i][0]["pick"] + " to win",
            backgroundColor: json[i][0]["colour"],
            borderColor: json[i][0]["colour"],
            pointHoverBorderColor: json[i][0]["accent"],
            pointRadius: 2,
            data: dataPoints[i],
            spanGaps: true,
            showLine: true,
        })
    }

    const verticalLinePlugin = {
        getLinePosition: function (chart, pointIndex) {
            const meta = chart.getDatasetMeta(0); // first dataset is used to discover X coordinate of a point
            const data = meta.data;
            return data[pointIndex]._model.x;
        },
        renderVerticalLine: function (chartInstance, pointIndex) {
            const lineLeftOffset = this.getLinePosition(chartInstance, pointIndex);
            const scale = chartInstance.scales['y-axis-0'];
            const context = chartInstance.chart.ctx;
      
            // render vertical line
            context.beginPath();
            context.strokeStyle = '#ff0000';
            context.moveTo(lineLeftOffset, scale.top);
            context.lineTo(lineLeftOffset, scale.bottom);
            context.stroke();
      
            // write label
            context.fillStyle = "#ff0000";
            context.textAlign = 'center';
            context.fillText('MY TEXT', lineLeftOffset, (scale.bottom - scale.top) / 2 + scale.top);
        },
      
        afterDatasetsDraw: function (chart, easing) {
            if (chart.config.lineAtIndex) {
                chart.config.lineAtIndex.forEach(pointIndex => this.renderVerticalLine(chart, pointIndex));
            }
        }
    };

    //CUSTOM TOOLTIP TO SEND TOOLTIP TO TOP RIGHT OF CHART
    Chart.Tooltip.positioners.customTooltip = function(elements, eventPosition){
        var tooltip = this;

        return {
            x: myChart.chartArea.right,
            y: myChart.chartArea.top + 40,
        };
    };


    //CHART CONFIGURATION
    const config = {
        type: 'line',
        data,
        options: {
            animation:{
                easing: 'linear',
            },
            plugins: {
                title: {
                    display: false,
                    text: 'Current Listings'
                },
                subtitle: {
                    display: true,
                    text: 'Your best odds if you bet: '
                },
                tooltip: {
                    enabled: true,
                    xAlign: 'right',
                    usePointStyle: false,
                    boxPadding: 5,
                    cornerRadius: 5,
                    caretPadding: 5,
                    caretSize: 0,
                    backgroundColor: "rgba(0, 0, 0, 0.7)",
                    position: 'customTooltip',
                },
                annotation: {
                    annotations: {
                        line1: {
                            drawTime: 'afterDraw',
                            type: "line",
                            mode: "vertical",
                            scaleID: "xAxes",
                            borderColor: "rgba(0, 0, 0, 0.3",
                            borderWidth: 1,
                            value: dataPoints[1][10]['x'],
                            label: {
                                content: "TODAY",
                                enabled: false,
                                position: "top",
                            }
                        }
                    }
                },
                zoom: {
                    pan: {
                        enabled: true,
                        mode: 'xy',
                        modifierKey: 'ctrl',
                        overScaleMode: 'xy',
                    },
                    limits: {
                        y: {min: 0, max: 'original'},
                        x: {min: 'original', max: 'original'},
                    },
                    zoom: {
                        mode: 'xy',
                        overScaleMode: 'xy',
                        wheel: {
                            enabled: false,
                        },
                        drag: {
                            enabled: true,
                            backgroundColor: 'rgba(0, 0, 0, 0.3)',
                            speed: 0.2,
                            threshold: 100,
                        },
                        pinch: {
                            enabled: true,
                        },
                    },
                },
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
                        precision: 0,
                    },
                    grid: {
                        display: true,
                    },
                },
                xAxes: {
                    type: 'time',
                    time: {
                        tooltipFormat: 'MMM d p',
                    },
                    title: {
                        display: true,
                        text: "Time",
                        font: {
                            size: 15
                        }
                    },
                    ticks: {
                        precision: 0,
                        maxTicksLimit: 5,
                        maxRotation: 0,
                        autoSkip: false,
                    },
                    displayFormats: {
                        
                    },
                    offset: true,
                    grid: {
                        display: true,
                        drawTicks: false,
                    },
                },
            },
            interaction: {
                intersect: false,
                mode: "nearest",
                axis: "x",
            },
            events: [
                'mousemove', 'click'
            ],
            onHover: (e, activeEls) => {
                let datasetIndex = activeEls[0].datasetIndex;
                let dataIndex = activeEls[0].index;
                let datasetLabel = e.chart.data.datasets[datasetIndex].label;
                let value = e.chart.data.datasets[datasetIndex].data[dataIndex];                
                let x = value['x'];
                
                myChart.config.options.plugins.annotation.annotations.line1.value = x;
                myChart.config.options.animation.duration = 50;
                myChart.update();
            },
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
        $.get(path, buildChart);
    }
}

//FILTER TABLE BY PICK
$(document).on('input', '#tablePickFilter', function() {  
    $("#eventTable tbody tr").hide(); //hide all rows
    var refine = $(this).val(); //retrieve wanted status
    var regex = new RegExp(refine);

    if(refine=="All") {
        $("#eventTable tbody tr").show(); //show all rows if want to see All
    } else {

        $("#eventTable tbody tr").each(function() { //loop over each row
             if($(this).find(".yourPick").text().match(regex)) { //check value of TD
                 $(this).show(); //show the row 
             }
        });

    }
});

//Sort  by default
$(document).ready(function(){
    $("#yourOdds").each(function(){
      sorttable.innerSortFunction.apply(this, []);
    })
})

//CREATE A LISTING POPUP
function createListing(event_id){
    $("#createListingPopup").removeClass("hidden");

    $("#pick_selector").trigger('input');
    updateReturn();
}

function createListingClose(){
    $("#createListingPopup").addClass("hidden");
}

//Close popup when clicking off
$(document).mouseup(function(e) {
    var container = $("#createListingPopup");

    // if the target of the click isn't the container nor a descendant of the container
    if (!container.is(e.target) && container.has(e.target).length === 0 && !container.hasClass('hidden')){
        createListingClose();
    }
});

function round(num) {
    //var m = Number((Math.abs(num) * 100).toPrecision(15));
    //return Math.round(m) / 100 * Math.sign(num);

    return Math.floor(num * 100) / 100;
}

//Update reciprical odds when user enters odds
$(document).on('keyup mouseup', '#user_odds', function() {  
    
    user_odds = $(this).val();
    
    their_odds = round((1/(user_odds-1)+1));
    $('#their_odds').val(their_odds); 
    
    //Change return amount
    updateReturn();

});

$(document).on('keyup mouseup', '#their_odds', function() {  
    their_odds = $(this).val();
    
    user_odds = round((1/(their_odds-1)+1));
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
    user_return = (current_amount * user_odds).toFixed(2);

    $('#return').html("Return: $" + user_return);  
}


//SET BEST ODDS FOR OPTION ON CHANGE
$(document).on('input', '#pick_selector', function() {  
    best_odds = $('option:selected', this).attr('data-best_odds');
    best_odds_amount = $('option:selected', this).attr('data-best_odds_amount');
    $("#best_odds").html("Current best odds offered: $" + best_odds + " ($" + best_odds_amount + " bet)");
});


//POST A LISTING
function postListing(user_id){

    //Perhaps use an alert to show uneditable details before submitting

    //Get data for listing
    let pick = $('option:selected', "#pick_selector").val();
    let user_odds = $("#user_odds").val();
    let their_odds = $("#their_odds").val();
    let amount = $("#amount").val();
    let event_id = $('option:selected', "#pick_selector").attr('data-event_id');
    let listing_return = user_odds * amount;

    //Format data for listing post
    data = [
        {
            "user_id": user_id,
            "option_id": pick,
            "user_odds": user_odds,
            "their_odds": their_odds,
            "amount": amount,
            "event_id": event_id,
            "listing_return": listing_return,
        }
    ];


    $.ajax({
        type: "POST",
        url: "/post_listing",
        data: JSON.stringify(data),
        contentType: "text/json; charset=utf-8",
        dataType: "text",
        success: function (msg) {
            msg = JSON.parse(msg);
            switch(msg['result']){
                case 'success':
                    window.location.replace("/event/" + msg['event_id']);
                    break;
                case 'failure':
                    alert(msg['error']);
                    break;
            }
        },
        error: function (jqXHR, textStatus, errorThrown) {
            alert('error');
        }
    });
}

//MATCH A LISTING

//Match confirmation popup
function matchPopup(listing){
    //Data available: id, option, odds, amount, username, daymonth, other_options, user_return, match_amount, user_id

    //Populate popup data
    bet_amount = listing.user_return - listing.amount
    text = "Bet <b>$" + bet_amount + "</b> on <b>" + listing.pick + " @ $" + listing.odds + "</b> odds, against <b>" + listing.username + "</b>.<br>Expected return: <b>$" + listing.user_return + "</b>.<br>" + "Event start time: <b>" + listing.daymonth + "</b>.";

    $("#matchPopup p").html(text);
    $("#matchConfirm").attr('data-listing_id', listing.id);

    //Make popup visible
    $("#matchPopup").toggleClass('hidden');
}

//Close popup when clicking off
$(document).mouseup(function(e) {
    var container = $("#matchPopup");

    // if the target of the click isn't the container nor a descendant of the container
    if (!container.is(e.target) && container.has(e.target).length === 0 && !container.hasClass('hidden')){
        if(!$("#matchPopup").hasClass('hidden')){
            $("#matchPopup").toggleClass('hidden');
        }
    }
});

//Hide popup on cancel
function cancelMatching(){
    //Make popup invisible
    if(!$("#matchPopup").hasClass('hidden')){
        $("#matchPopup").toggleClass('hidden');
    }
}

function matchListing(user_id){

    //Format data for listing post
    let listing_id = $("#matchConfirm").attr('data-listing_id');
    data = [
        {
            'listing_id': listing_id,
            'user_id': user_id,
        }
    ];

    //Make request
    $.ajax({
        type: "POST",
        url: "/match_listing",
        data: JSON.stringify(data),
        contentType: "text/json; charset=utf-8",
        dataType: "text",
        success: function (msg) {
            msg = JSON.parse(msg);
            switch(msg['result']){
                case 'success':
                    window.location.replace("/user");
                    break;
                case 'failure':
                    alert(msg['error']);
                    break;
            }
        },
        error: function (jqXHR, textStatus, errorThrown) {
            alert('error');
        }
    });

}


// BANK PAGE ---------------------------------------
function deposit(){
    amount = $("#deposit_amount").val();

    window.location.replace("/deposit?amount="+ amount);
}
