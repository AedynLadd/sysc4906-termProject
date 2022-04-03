
help_modal = document.getElementById("settings_modal");


function create_help_card(){
    return [
        "<div>",
        "</div>"
    ].join("")
}



function openHelpMenu(){
    console.log("Opening Menu")
    console.log(help_menu_visual_info)
    displayMouseHoeverInformation()
    
}

function closeHelpMenu(){
    console.log("Closing Menu")
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
    if (document.getElementById("coin_select")) {
        console.log(help_menu_visual_info.coin_select.name + help_menu_visual_info.coin_select.description);
    }}
function mouseOver2(){
    if (document.getElementById("cyclic_coin_info")) {
        console.log(help_menu_visual_info.cyclic_coin_info.name + help_menu_visual_info.cyclic_coin_info.description);
    }}
    function mouseOver3(){
    if (document.getElementById("keyword_network_diagram")) {
        console.log(help_menu_visual_info.keyword_network_diagram.name + help_menu_visual_info.keyword_network_diagram.description);
    }}
    function mouseOver4(){
    if (document.getElementById("network_diagram_data")) {
        console.log(help_menu_visual_info.network_diagram_data.name + help_menu_visual_info.network_diagram_data.description);
    }}
    function mouseOver5(){
    if (document.getElementById("coin_chart_data")) {
        console.log(help_menu_visual_info.coin_chart_data.name + help_menu_visual_info.coin_chart_data.description);
    }}
    function mouseOver6(){
    if (document.getElementById("coin_sentiment_heatmap")) {
        console.log(help_menu_visual_info.coin_sentiment_heatmap.name + help_menu_visual_info.coin_sentiment_heatmap.description);
    }}
    function mouseOver7(){
    if (document.getElementById("forecast_coin_chart")) {
        console.log(help_menu_visual_info.forecast_coin_chart.name + help_menu_visual_info.forecast_coin_chart.description);
    }}
