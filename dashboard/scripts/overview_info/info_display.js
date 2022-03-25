var joyplot_container = document.getElementById("coin_joyplots").getBoundingClientRect();

const joyplot_diagram = { top: 0, right: 0, bottom: 30, left: 0 },
      joyplot_diagram_width = joyplot_container.width - joyplot_diagram.left - joyplot_diagram.right,
      joyplot_diagram_height = joyplot_container.height - joyplot_diagram.top - joyplot_diagram.bottom;

// append the svg object to the body of the page
const coin_joyplot_svg = d3.select("#coin_joyplots")
    .append("svg")
    .attr("width", "100%")
    .attr("height", "100%")
    .append("g")

coin_joyplot_svg.selectAll("areas")


function display_coin_info(coin_data){
    if(coin_data == null){
        console.log("displaying an overview")
        document.getElementById("additional_coin_info_box_title").innerHTML = "OVERVIEW"

    } else {
        console.log("displaying info on a specific coin")
        console.log(coin_data)
        document.getElementById("additional_coin_info_box_title").innerHTML = coin_data.name.toUpperCase()
    }
}

display_coin_info(null);
