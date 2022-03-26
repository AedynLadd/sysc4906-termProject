function create_coin_summary(id) {
    coin_info = top_100_coins[id]

    coin_name_ids = coin_info.name.split(" ").join("_")
    return [
        "<div class='coin_summary' id='coin_summary_" + id + "' onclick=update('" + coin_name_ids + "')>",
        "<div class='coin_summary layout'>",
        "<div class='coin_summary name'  id='coin_summary_display_name_" + id + "'>", coin_info.name, "</div>",
        "<div class='coin_summary symbol' id='coin_summary_display_symbol_" + id + "'>", coin_info.symbol, "</div>",
        "<div class='coin_summary rank'  id='coin_summary_display_rank_" + id + "'>", coin_info.rank, "</div>",
        "<div class='coin_summary chart' id='coin_summary_display_" + id + "'></div>",
        "</div>",
        "</div>"
    ]
}

var last_display_index = 0;
var line_chart_ref = []

function coin_display_init() {
    for (let i = 0; i < 5; i++) {
        last_display_index = i
        document.getElementById("cyclic_coin_info").innerHTML += create_coin_summary(i).join("")

        var line_chart_container = document.getElementById("coin_summary_display_" + i).getBoundingClientRect();

        // set the dimensions and margins of the graph
        var line_margin = { top: 10, right: 30, bottom: 30, left: 10 };
        var line_width = line_chart_container.width - line_margin.left - line_margin.right;
        var line_height = line_chart_container.height - line_margin.top - line_margin.bottom;

        line_chart_ref[i] = {"line_width": line_width, "line_height": line_height}

        d3.select("#coin_summary_display_" + i)
            .append("svg")
            .attr("width", line_width + line_margin.left + line_margin.right)
            .attr("height", line_height + line_margin.top + line_margin.bottom)
            .append("g")
            .attr("transform", `translate(${line_margin.left}, ${line_margin.top})`)
            .append('g')
            .append("path")
            .attr("id", "line_chart_summary_element_" + i)
    }

    for(let i = 0; i < 5; i++){
        update_coin_summary_graph((i % 5), i)
    }
}

// A function that update the chart
function update_coin_summary_graph(i, coin_id) {
    selectedCoin = top_100_coins[coin_id].name.split("_").join(" ")

    let y_min = d3.min(historical_coin_data[selectedCoin]["open"], function (d) { return d })
    let y_max = d3.max(historical_coin_data[selectedCoin]["open"], function (d) { return d })
    let y_range = y_max - y_min

    // Add X axis --> it is a date format
    var new_x = d3.scaleLinear()
        .domain(d3.extent(historical_coin_data[selectedCoin]["timestamp"], function (d) { return new Date(d) }))
        .range([0, line_chart_ref[i].line_width]);

    // Add Y axis
    var new_y = d3.scaleLinear()
        .domain([y_min - y_range*0.1, y_max + y_range*0.1])
        .range([line_chart_ref[i].line_height, 0]);

    // Create new data with the selection
    var rearrangedData = historical_coin_data[selectedCoin].open.map(function (d, i) { return { "data": d, "timestamp": historical_coin_data[selectedCoin].timestamp[i] }; });
    d3.select("#line_chart_summary_element_" + i)
        .datum(rearrangedData)
        .transition()
        .duration(1000)
        .attr("d", d3.line().curve(d3.curveBasis).x(function (d) { return new_x(new Date(d.timestamp)) }).y(function (d) { return new_y(+d.data) }))
        .attr("stroke", function (d) { return myColor(selectedCoin) })
        .attr("stroke-width", "3px")
        .attr("fill", "none")
        .style("filter","drop-shadow(0px 0px 3px " + myColor(selectedCoin) + ")");
}


current_ref = []
function transition_display() {
    if (document.getElementById("overview_info_container").style.display != "none") {
        last_display_index = (last_display_index + 1) % 100;

        var coin_info = top_100_coins[last_display_index]
        var coin_name_ids = coin_info.name.split(" ").join("_")

        document.getElementById("coin_summary_" + (last_display_index % 5)).onclick = () => update(coin_name_ids);
        document.getElementById("coin_summary_display_name_" + (last_display_index % 5)).innerHTML = coin_info.name
        document.getElementById("coin_summary_display_symbol_" + (last_display_index % 5)).innerHTML = coin_info.symbol
        document.getElementById("coin_summary_display_rank_" + (last_display_index % 5)).innerHTML = coin_info.rank

        update_coin_summary_graph((last_display_index % 5), last_display_index)
    }
}


var onInterval = window.setInterval(transition_display, 1000);

// Initialize the home page
coin_display_init();
