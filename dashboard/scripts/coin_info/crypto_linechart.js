
var line_chart_container = document.getElementById("coin_chart_data").getBoundingClientRect();

// set the dimensions and margins of the graph
const line_margin = {top: 20, right: 20, bottom: line_chart_container.height*0.5, left: 40},
    margin2 = {top: line_chart_container.height*0.6, right: 20, bottom: line_chart_container.height*0.01, left: 40},
    line_width = line_chart_container.width - line_margin.left - line_margin.right,
    line_height = line_chart_container.height - line_margin.top - line_margin.bottom,
    full_scope_height = line_chart_container.height - margin2.top - margin2.bottom;


// append the svg object to the body of the page
const line_svg = d3.select("#coin_chart_data")
    .append("svg")
    .attr("width", line_width + line_margin.left + line_margin.right)
    .attr("height", (line_height + full_scope_height) + line_margin.top + line_margin.bottom)
    .append("g")
    .attr("transform", `translate(${line_margin.left}, ${line_margin.top})`);

// List of groups (here I have one group per column)
var allGroup = Object.keys(historical_coin_data)

function create_coin_label(name_of_coin) {
    coin_name_ids = name_of_coin.split(" ").join("_")
    return [
        "<li class='coin_label' id='coin_id_" + coin_name_ids + "' onclick=update('" + coin_name_ids + "')>",
        "<a>", name_of_coin, "</a>",
        "</li>"
    ]
}

allGroup.forEach(e => document.getElementById("coin_select").innerHTML += create_coin_label(e).join(""))
//
// LINE COLOR DEFINITIONS
// A color scale: one color for each group
//
var myColor = d3.scaleOrdinal()
    .domain(allGroup)
    .range(d3.schemeSet2);

var areaGradient = line_svg.append("defs")
    .append("linearGradient")
    .attr("id", "areaGradient")
    .attr("x1", "0%").attr("y1", "0%")
    .attr("x2", "0%").attr("y2", "100%");

var area_top_col = areaGradient.append("stop")
var area_bottom_col = areaGradient.append("stop")

var rearrangedData = historical_coin_data[allGroup[0]].open.map(function (d, i) { return { "data": d, "timestamp": historical_coin_data[allGroup[0]].timestamp[i] }; });

//
// ACTUAL LINE DEFINITION
// Initialize line with first group of the list
//
var focus = line_svg.append("g")
    .attr("class", "focus")

var context = line_svg.append("g")
    .attr("class", "context")

var line = focus   // top line def
    .append('g')
    .append("path")

var area = focus // area def
    .append('g')
    .append("path")

var line_2 = context // bottom line def
    .append("g")
    .append("path")


//
// AXIS DEFINITIONS
//
// top chart
var line_x_axis = focus.append("g").attr("class", "line_axis_x")
.attr("transform", "translate(0," + line_height + ")")

var line_y_axis = focus.append("g").attr("class", "line_axis_y")

// bottom chart
var line_scope_x_axis = context.append("g").attr("class", "line_scope_axis_x")
.attr("transform", "translate(0," + (line_height + full_scope_height) + ")")



//
// This defines our brush and zoom
//

var line_brush = d3.brushX()
    .extent([[0, line_margin.bottom], [line_width, line_height + full_scope_height ]])

var brush_callback = context.append("g")
    .attr("class", "brush")
    .call(line_brush)

var zoom = d3.zoom()
    .scaleExtent([1, Infinity])
    .translateExtent([[0, 0], [line_width, line_height]])
    .extent([[0, 0], [line_width, line_height]])

var clip = line_svg.append("defs").append("svg:clipPath")
    .attr("id", "clip")
    .append("svg:rect")
    .attr("width", line_width)
    .attr("height", line_height)
    .attr("x", 0)
    .attr("y", 0); 

var zoom_rect = line_svg.append("rect")
    .attr("class", "zoom")
    .attr("width", line_width)
    .attr("height", line_height)
    .call(zoom);


//
// THIS FUNCTION UPDATES THE DATA AND THE CHART
// 
function update_graph(selectedGroup) {
    selectedGroup = selectedGroup.split("_").join(" ")
    // Add X axis --> it is a date format
    var new_x = d3.scaleLinear()
        .domain(d3.extent(historical_coin_data[selectedGroup]["timestamp"], function (d) { return new Date(d) }))
        .range([0, line_width]);

    var x2 = d3.scaleLinear()
        .domain(new_x.domain())
        .range([0, line_width])
    
    
    line_x_axis.call(d3.axisBottom(new_x).ticks(7).tickFormat(d => { return (new Date(d)).toLocaleDateString("en-CA") }));
    line_scope_x_axis.call(d3.axisBottom(new_x).ticks(7).tickFormat(d => { return (new Date(d)).toLocaleDateString("en-CA") }));
    
    // y axis data
    let y_min = d3.min(historical_coin_data[selectedGroup]["open"], function (d) { return d })
    let y_max = d3.max(historical_coin_data[selectedGroup]["open"], function (d) { return d })
    let y_range = y_max - y_min

    // Add Y axis
    var new_y = d3.scaleLinear()
        .domain([y_min - y_range * 0.1, y_max + y_range * 0.1])
        .range([line_height, 0]);

    var new_scope_y = d3.scaleLinear()
        .domain([y_min - y_range * 0.1, y_max + y_range * 0.1])
        .range([line_height + full_scope_height, full_scope_height + 50]);

    line_y_axis.call(d3.axisLeft(new_y).ticks(5));
    // Create new data with the selection
    var rearrangedData = historical_coin_data[selectedGroup].open.map(function (d, i) { return { "data": d, "timestamp": historical_coin_data[selectedGroup].timestamp[i] }; });
        
    // Give these new data points to update line
    area
        .datum(rearrangedData)
        .transition()
        .duration(1000)
        .attr("d", d3.area()
            .x(function (d) { return new_x(new Date(d.timestamp)) })
            .y1(function (d) { return new_y(+d.data) })
            .y0(function (d) { return new_y(y_min - y_range * 0.1) })

        )
        .attr("fill", "url(#areaGradient)")

    line
        .datum(rearrangedData)
        .transition()
        .duration(1000)
        .attr("d", d3.line()
            .x(function (d) { return new_x(new Date(d.timestamp)) })
            .y(function (d) { return new_y(+d.data) })
        )
        .attr("stroke", function (d) { return myColor(selectedGroup) })
        .attr("stroke-width", "3px")
        .attr("fill", "none")

    area_top_col.transition()
        .duration(1000)
        .attr("offset", "0%")
        .attr("stop-color", myColor(selectedGroup) + "A0");

    area_bottom_col.transition()
        .duration(1000)
        .attr("offset", "100%")
        .attr("stop-color", "none")
        .attr("stop-opacity", 0);

    // Add the line number 2 data this shows all time as opposed to brushed area
    line_2.datum(rearrangedData)
        .transition()
        .duration(1000)
        .attr("d", d3.line()
            .x(function (d) { return new_x(new Date(d.timestamp)) })
            .y(function (d) { return new_scope_y(+d.data)})
        )
        .attr("stroke", function (d) { return myColor(selectedGroup) })
        .attr("stroke-width", "1px")
        .attr("fill", "none")
    
    brush_callback.call(line_brush.move, new_x.range());
    
    line_brush.on("brush end", brushed);
    function brushed(event) {
        if (event.sourceEvent == undefined) return; // ignore brush-by-zoom
        var s = event.selection || x2.range();
        new_x.domain(s.map(x2.invert, x2));
    
        line.datum(rearrangedData)
            .attr("d", d3.line()
                .x(function (d) { return new_x(new Date(d.timestamp)) })
                .y(function (d) { return new_y(+d.data) })
            )
        
        area
            .datum(rearrangedData)
            .attr("d", d3.area()
                .x(function (d) { return new_x(new Date(d.timestamp)) })
                .y1(function (d) { return new_y(+d.data) })
                .y0(function (d) { return new_y(y_min - y_range * 0.1) })
            )

        focus.select(".line_axis_x").call(d3.axisBottom(new_x).ticks(7).tickFormat(d => { return (new Date(d)).toLocaleDateString("en-CA") }));

        line_svg.select(".zoom").call(zoom.transform, d3.zoomIdentity
                .scale(line_width / (s[1] - s[0]))
                .translate(-s[0], 0));
    }
    

    zoom.on("zoom", zoomed);
    function zoomed(event) {
        console.log(event)
        if (event.sourceEvent == undefined || event.sourceEvent.type != "wheel") return; // ignore zoom-by-brush
        
        var t = event.transform;
        new_x.domain(t.rescaleX(x2).domain());

        line.datum(rearrangedData)
            .attr("d", d3.line()
                .x(function (d) { return new_x(new Date(d.timestamp)) })
                .y(function (d) { return new_y(+d.data) })
            )
        
        area
            .datum(rearrangedData)
            .attr("d", d3.area()
                .x(function (d) { return new_x(new Date(d.timestamp)) })
                .y1(function (d) { return new_y(+d.data) })
                .y0(function (d) { return new_y(y_min - y_range * 0.1) })
            )
        focus.select(".axis--x").call(d3.axisBottom(new_x));
        context.select(".brush").call(line_brush.move, new_x.range().map(t.invertX, t));
    }
}

  