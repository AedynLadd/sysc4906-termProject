
var line_chart_container = document.getElementById("coin_chart_data").getBoundingClientRect();

// set the dimensions and margins of the graph
const margin = { top: 10, right: 30, bottom: 30, left: 60 },
    width = line_chart_container.width - margin.left - margin.right,
    height = line_chart_container.height - margin.top - margin.bottom;

// append the svg object to the body of the page
const svg = d3.select("#coin_chart_data")
    .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", `translate(${margin.left}, ${margin.top})`);


// List of groups (here I have one group per column)
var allGroup = Object.keys(historical_coin_data)

function create_coin_label(name_of_coin) {
    coin_name_ids = name_of_coin.split(" ").join("_")
    return [
        "<div class='coin_label' id='coin_id_" + coin_name_ids + "' onclick=update_graph('" + coin_name_ids + "')>",
        name_of_coin,
        "</div>"
    ]
}

allGroup.forEach(e => document.getElementById("coin_select").innerHTML += create_coin_label(e).join(""))

// A color scale: one color for each group
var myColor = d3.scaleOrdinal()
    .domain(allGroup)
    .range(d3.schemeSet2);

var areaGradient = svg.append("defs")
    .append("linearGradient")
    .attr("id", "areaGradient")
    .attr("x1", "0%").attr("y1", "0%")
    .attr("x2", "0%").attr("y2", "100%");

var area_top_col = areaGradient.append("stop")

var area_bottom_col = areaGradient.append("stop")



var x_axis = svg.append("g")
    .attr("transform", "translate(0," + height + ")")


var y_axis = svg.append("g")


var rearrangedData = historical_coin_data[allGroup[0]].open.map(function (d, i) { return { "data": d, "timestamp": historical_coin_data[allGroup[0]].timestamp[i] }; });

// Initialize line with first group of the list
var line = svg
    .append('g')
    .append("path")


// A function that update the chart
function update_graph(selectedGroup) {
    selectedGroup = selectedGroup.split("_").join(" ")
    // Add X axis --> it is a date format
    var new_x = d3.scaleLinear()
        .domain(d3.extent(historical_coin_data[selectedGroup]["timestamp"], function (d) { return new Date(d) }))
        .range([0, width]);

    x_axis.call(d3.axisBottom(new_x).ticks(7));

    // Add Y axis
    var new_y = d3.scaleLinear()
        .domain([0, d3.max(historical_coin_data[selectedGroup]["open"], function (d) { return d })])
        .range([height, 0]);

    y_axis.call(d3.axisLeft(new_y));
    // Create new data with the selection
    var rearrangedData = historical_coin_data[selectedGroup].open.map(function (d, i) { return { "data": d, "timestamp": historical_coin_data[selectedGroup].timestamp[i] }; });

    // Give these new data to update line
    line
        .datum(rearrangedData)
        .transition()
        .duration(1000)
        .attr("d", d3.area()
            .x(function (d) { return new_x(new Date(d.timestamp)) })
            .y0(function (d) { return new_y(0) })
            .y1(function (d) { return new_y(+d.data) })
        )

        .attr("stroke", function (d) { return myColor(selectedGroup) })
        .attr("fill", "url(#areaGradient)")

    area_top_col.transition().duration(1000).attr("offset", "0%")
        .attr("stop-color", myColor(selectedGroup) + "A0");

    area_bottom_col.transition().duration(1000).attr("offset", "100%")
        .attr("stop-color", "none")
        .attr("stop-opacity", 0);
}

// When the button is changed, run the updateChart function
d3.select("#selectButton").on("change", function (d) {
    // recover the option that has been chosen
    var selectedOption = d3.select(this).property("value")
    update_graph(selectedOption)
})

update_graph(allGroup[0])