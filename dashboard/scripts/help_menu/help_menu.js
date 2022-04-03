
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
    document.getElementById("coin_select").onmouseover = function() {mouseOver()};
    document.getElementById("cyclic_coin_info").onmouseover = function() {mouseOver()};
    document.getElementById("keyword_network_diagram").onmouseover = function() {mouseOver()};
    document.getElementById("network_diagram_data").onmouseover = function() {mouseOver()};
    document.getElementById("coin_chart_data").onmouseover = function() {mouseOver()};
    document.getElementById("coin_sentiment_heatmap").onmouseover = function() {mouseOver()};
    document.getElementById("forecast_coin_chart").onmouseover = function() {mouseOver()};
}

function mouseOver(){
    if (document.getElementById("coin_select")) {
        console.log(help_menu_visual_info.coin_select.name + help_menu_visual_info.coin_select.description);
    }
    if (document.getElementById("cyclic_coin_info")) {
        console.log(help_menu_visual_info.cyclic_coin_info.name + help_menu_visual_info.cyclic_coin_info.description);
    }
    if (document.getElementById("keyword_network_diagram")) {
        console.log(help_menu_visual_info.keyword_network_diagram.name + help_menu_visual_info.keyword_network_diagram.description);
    }
    if (document.getElementById("network_diagram_data")) {
        console.log(help_menu_visual_info.network_diagram_data.name + help_menu_visual_info.network_diagram_data.description);
    }
    if (document.getElementById("coin_chart_data")) {
        console.log(help_menu_visual_info.coin_chart_data.name + help_menu_visual_info.coin_chart_data.description);
    }
    if (document.getElementById("coin_sentiment_heatmap")) {
        console.log(help_menu_visual_info.coin_sentiment_heatmap.name + help_menu_visual_info.coin_sentiment_heatmap.description);
    }
    if (document.getElementById("forecast_coin_chart")) {
        console.log(help_menu_visual_info.forecast_coin_chart.name + help_menu_visual_info.forecast_coin_chart.description);
    }
}