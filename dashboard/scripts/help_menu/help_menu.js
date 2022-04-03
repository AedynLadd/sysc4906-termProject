
help_modal = document.getElementById("settings_modal");
var settingsOpen = false
var mouse1Used = true
var mouse2Used = true
var mouse3Used = true
var mouse4Used = true
var mouse5Used = true
var mouse6Used = true
var mouse7Used = true

function create_help_card(){
    return [
        "<div>",
        "</div>"
    ].join("")
}



function openHelpMenu(){
    console.log("Opening Menu")
    console.log(help_menu_visual_info)
    settingsOpen = true
    displayMouseHoeverInformation()
    document.body.style.background = 'black';
    
}

function closeHelpMenu(){
    console.log("Closing Menu")
    settingsOpen = false
}




function displayMouseHoeverInformation(){
    document.getElementById("coin_select").onmouseover = function() {mouseOver1()};
    document.getElementById("cyclic_coin_info").onmouseover = function() {mouseOver2()};
    document.getElementById("keyword_network_diagram").onmouseover = function() {mouseOver3()};
    document.getElementById("network_diagram_data").onmouseover = function() {mouseOver4()};
    document.getElementById("coin_chart_data").onmouseover = function() {mouseOver5()};
    document.getElementById("coin_sentiment_heatmap").onmouseover = function() {mouseOver6()};
    document.getElementById("forecast_coin_chart").onmouseover = function() {mouseOver7()};
}

function mouseOver1(){
    if (document.getElementById("coin_select") && (settingsOpen==true) && (mouse1Used==true)) {
        console.log(help_menu_visual_info.coin_select.name + help_menu_visual_info.coin_select.description);
        //alert(help_menu_visual_info.coin_select.name);
        alert(help_menu_visual_info.coin_select.name + "\n" + help_menu_visual_info.coin_select.description);
        mouse1Used = false
    }}
function mouseOver2(){
    if (document.getElementById("cyclic_coin_info")&& (settingsOpen==true) && (mouse2Used==true)) {
        console.log(help_menu_visual_info.cyclic_coin_info.name + help_menu_visual_info.cyclic_coin_info.description);
        //alert(help_menu_visual_info.cyclic_coin_info.name);
        alert(help_menu_visual_info.cyclic_coin_info.name + "\n" + help_menu_visual_info.cyclic_coin_info.description);
        mouse2Used = false
    }}
    function mouseOver3(){
    if (document.getElementById("keyword_network_diagram")&& (settingsOpen==true) && (mouse3Used==true)) {
        console.log(help_menu_visual_info.keyword_network_diagram.name + help_menu_visual_info.keyword_network_diagram.description);
        //alert(help_menu_visual_info.keyword_network_diagram.name);
        alert(help_menu_visual_info.keyword_network_diagram.name + "\n" + help_menu_visual_info.keyword_network_diagram.description);
        mouse3Used = false
    }}
    function mouseOver4(){
    if (document.getElementById("network_diagram_data")&& (settingsOpen==true) && (mouse4Used==true)) {
        console.log(help_menu_visual_info.network_diagram_data.name + help_menu_visual_info.network_diagram_data.description);
        //alert(help_menu_visual_info.network_diagram_data.name);
        alert(help_menu_visual_info.network_diagram_data.name + "\n" + help_menu_visual_info.network_diagram_data.description);
        mouse4Used = false
    }}
    function mouseOver5(){
    if (document.getElementById("coin_chart_data")&& (settingsOpen==true) && (mouse5Used==true)) {
        console.log(help_menu_visual_info.coin_chart_data.name + help_menu_visual_info.coin_chart_data.description);
        //alert(help_menu_visual_info.coin_chart_data.name);
        alert(help_menu_visual_info.coin_chart_data.name + "\n" + help_menu_visual_info.coin_chart_data.description);
        mouse5Used = false
    }}
    function mouseOver6(){
    if (document.getElementById("coin_sentiment_heatmap")&& (settingsOpen==true) && (mouse6Used==true)) {
        console.log(help_menu_visual_info.coin_sentiment_heatmap.name + help_menu_visual_info.coin_sentiment_heatmap.description);
        //alert(help_menu_visual_info.coin_sentiment_heatmap.name);
        alert(help_menu_visual_info.coin_chart_data.name + "\n" + help_menu_visual_info.coin_sentiment_heatmap.description);
        mouse6Used = false
    }}
    function mouseOver7(){
    if (document.getElementById("forecast_coin_chart") && (settingsOpen==true) && (mouse7Used==true)) {
        console.log(help_menu_visual_info.forecast_coin_chart.name + help_menu_visual_info.forecast_coin_chart.description);
        //alert(help_menu_visual_info.forecast_coin_chart.name);
        alert(help_menu_visual_info.forecast_coin_chart.name + "\n" + help_menu_visual_info.forecast_coin_chart.description);
        mouse7Used = false
    }}
