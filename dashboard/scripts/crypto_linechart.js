

// set the dimensions and margins of the graph
const margin = { top: 10, right: 30, bottom: 30, left: 60 },
    width = 460 - margin.left - margin.right,
    height = 400 - margin.top - margin.bottom;

// append the svg object to the body of the page
const svg = d3.select("#my_dataviz")
    .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", `translate(${margin.left}, ${margin.top})`);


// List of groups (here I have one group per column)
var allGroup = Object.keys(historical_coin_data)

// add the options to the button
d3.select("#selectButton")
    .selectAll('myOptions')
    .data(allGroup)
    .enter()
    .append('option')
    .text(function (d) { return d; }) // text showed in the menu
    .attr("value", function (d) { return d; }) // corresponding value returned by the button

// A color scale: one color for each group
var myColor = d3.scaleOrdinal()
    .domain(allGroup)
    .range(d3.schemeSet2);


var x_axis = svg.append("g")
    .attr("transform", "translate(0," + height + ")")


var y_axis = svg.append("g")


var rearrangedData = historical_coin_data[allGroup[0]].open.map(function (d, i) { return { "data": d, "timestamp": historical_coin_data[allGroup[0]].timestamp[i] }; });

// Initialize line with first group of the list
var line = svg
    .append('g')
    .append("path")


// A function that update the chart
function update(selectedGroup) {

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
        .attr("d", d3.line().x(function (d) { return new_x(new Date(d.timestamp)) }).y(function (d) { return new_y(+d.data) }))
        .attr("stroke", function (d) { return myColor(selectedGroup) })
        .attr("fill", "none")
}

// When the button is changed, run the updateChart function
d3.select("#selectButton").on("change", function (d) {
    // recover the option that has been chosen
    var selectedOption = d3.select(this).property("value")
    update(selectedOption)
})

update(allGroup[0])