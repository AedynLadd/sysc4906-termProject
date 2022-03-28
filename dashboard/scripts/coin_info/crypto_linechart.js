
var line_chart_container = document.getElementById("coin_chart_data").getBoundingClientRect();

// set the dimensions and margins of the graph
const line_margin = {top: 20, right: 20, bottom: line_chart_container.height*0.5, left: 40},
    margin2 = {top: line_chart_container.height*0.6, right: 20, bottom: line_chart_container.height*0.01, left: 40},
    line_width = (line_chart_container.width - line_margin.left - line_margin.right)*0.99,
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

var formatted_historical_data = new Object()

Object.keys(historical_coin_data).forEach((coin_name)=>{
    formatted_historical_data[coin_name] = historical_coin_data[coin_name].open.map(function (d, i) { return { "data": d, "timestamp": historical_coin_data[coin_name].timestamp[i] }; });
})

//
// ACTUAL LINE DEFINITION
// Initialize line with first group of the list
//
var focus = line_svg.append("g")
    .attr("class", "focus")
    .attr("id", "cryptoLinechartFocus")

var context = line_svg.append("g")
    .attr("class", "context")

var sentiment_line = focus
    .append('g')
    .append("path");

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
var line_x_axis = focus.append("g")
    .attr("class", "line_axis_x")
    .attr("transform", "translate(0," + line_height + ")")

var line_y_axis = focus.append("g")
    .attr("class", "line_axis_y")

var sentiment_line_y_axis = focus.append("g")
    .attr("class", "sentiment_line_axis_y")
    .attr("transform", "translate(" + line_width + ",0)");

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

var clip = focus.append("defs").append("svg:clipPath")
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
    var rearrangedData = formatted_historical_data[selectedGroup];
        
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
        .attr("clip-path", "url(#clip)")

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
        .style("filter", "drop-shadow(0px 0px 5px " + myColor(selectedGroup) + ")")
        .attr("clip-path", "url(#clip)")

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


    // Creation of the sentiment line
    sentiment_line_data_format = []
    
    var sentiment_min = null;
    var sentiment_max = null;

    Object.keys(day_summary_data).forEach(function(key){ 
        if (new_x(key) <= 0) return;
        sentiment_max = sentiment_max == null ? day_summary_data[key] : (sentiment_max < day_summary_data[key] ? day_summary_data[key] : sentiment_max);
        sentiment_min = sentiment_min == null ? day_summary_data[key] : (sentiment_min > day_summary_data[key] ? day_summary_data[key] : sentiment_min);
        sentiment_line_data_format.push({"timestamp": key, "data": day_summary_data[key]});
    })

    var sentiment_range = Math.abs(sentiment_min - sentiment_max);

    var sentiment_y = d3.scaleLinear()
        .domain([sentiment_min - sentiment_range * 0.1, (sentiment_min == sentiment_max & sentiment_max == 0) ? 1 : sentiment_max + sentiment_range * 0.1])
        .range([line_height, 0]);

    sentiment_line.datum(sentiment_line_data_format)
        .transition()
        .duration(1000)
        .attr("d", d3.line().curve(d3.curveBundle)
            .x(function (d) { return new_x(d.timestamp) })
            .y(function (d) { return sentiment_y(d.data)})
        )
        .attr("stroke", "white")
        .attr("stroke-width", "3px")
        .style("opacity", 0.3)
        .attr("fill", "none")
        .style("filter", "drop-shadow(0px 0px 5px black)")
        .attr("clip-path", "url(#clip)");
    
    sentiment_line_y_axis.call(d3.axisRight(sentiment_y).ticks(5));

    // Brushed and zoom events
    brush_callback.call(line_brush.move, new_x.range());
    
    brushed = (event) => {
        if (event.sourceEvent == undefined) return; // ignore brush-by-zoom
        var s = event.selection || x2.range();
        new_x.domain(s.map(x2.invert, x2));
    
        line.datum(rearrangedData)
            .attr("d", d3.line()
                .x(function (d) { return new_x(new Date(d.timestamp)) })
                .y(function (d) { return new_y(+d.data) })
            );
        
        area
            .datum(rearrangedData)
            .attr("d", d3.area()
                .x(function (d) { return new_x(new Date(d.timestamp)) })
                .y1(function (d) { return new_y(+d.data) })
                .y0(function (d) { return new_y(y_min - y_range * 0.1) })
            );

        sentiment_line
            .datum(sentiment_line_data_format)
            .attr("d", d3.line().curve(d3.curveBundle)
                .x(function (d) { return new_x(d.timestamp) })
                .y(function (d) { return sentiment_y(d.data)})
            );

        focus.select(".line_axis_x").call(d3.axisBottom(new_x).ticks(7).tickFormat(d => { return (new Date(d)).toLocaleDateString("en-CA") }));

        line_svg.select(".zoom").call(zoom.transform, d3.zoomIdentity
                .scale(line_width / (s[1] - s[0]))
                .translate(-s[0], 0));
    }
    
    zoomed = (event) => {
        if (event.sourceEvent == undefined || (event.sourceEvent.type == "wheel" || event.sourceEvent.type == "mousemove") != true) return; // ignore zoom-by-brush
        
        var t = event.transform;
        new_x.domain(t.rescaleX(x2).domain());

        line.datum(rearrangedData)
            .attr("d", d3.line()
                .x(function (d) { return new_x(new Date(d.timestamp)) })
                .y(function (d) { return new_y(+d.data) })
            );
        
        area
            .datum(rearrangedData)
            .attr("d", d3.area()
                .x(function (d) { return new_x(new Date(d.timestamp)) })
                .y1(function (d) { return new_y(+d.data) })
                .y0(function (d) { return new_y(y_min - y_range * 0.1) })
            );

        sentiment_line
            .datum(sentiment_line_data_format)
            .attr("d", d3.line().curve(d3.curveBundle)
                .x(function (d) { return new_x(d.timestamp) })
                .y(function (d) { return sentiment_y(d.data)})
            );
        focus.select(".axis--x").call(d3.axisBottom(new_x));
        context.select(".brush").call(line_brush.move, new_x.range().map(t.invertX, t));
    }

    zoom.on("zoom", zoomed);
    line_brush.on("brush end", brushed);
}

  