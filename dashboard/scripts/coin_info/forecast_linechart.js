
var forecast_chart_container = document.getElementById("forecast_coin_chart").getBoundingClientRect();

// set the dimensions and margins of the graph
const forecast_line_margin = { top: 20, right: 20, bottom: 30, left: 50 },
    forecast_line_width = (forecast_chart_container.width - forecast_line_margin.left - forecast_line_margin.right),
    forecast_line_height = (forecast_chart_container.height - forecast_line_margin.top - forecast_line_margin.bottom)

console.log(forecast_chart_container)
// append the svg object to the body of the page

const forecast_chart = d3.select("#forecast_coin_chart")
    .append("svg")
    .attr("width", forecast_line_width + forecast_line_margin.left + forecast_line_margin.right)
    .attr("height", forecast_line_height + forecast_line_margin.top + forecast_line_margin.bottom)
    .append("g")
    .attr("transform", `translate(${forecast_line_margin.left}, ${forecast_line_margin.top})`);


var formatted_forecast_data = new Object()

Object.keys(sevenD_forecast).forEach((coin_name) => {
    formatted_forecast_data[coin_name.replace(" ", "_")] = {}
    Object.keys(sevenD_forecast[coin_name]).forEach((line_element) => {
        if (line_element == "forecast") {
            formatted_forecast_data[coin_name.replace(" ", "_")]["forecast"] = sevenD_forecast[coin_name][line_element].timestamp.map(function (d, i) {
                return {
                    "timestamp": d,
                    "open_forecast": sevenD_forecast[coin_name][line_element].open_forecast[i],
                    "upper_bound": sevenD_forecast[coin_name][line_element].open_up_interval[i],
                    "lower_bound": sevenD_forecast[coin_name][line_element].open_down_interval[i],
                };
            });
        } else {
            formatted_forecast_data[coin_name.replace(" ", "_")]["actual"] = sevenD_forecast[coin_name][line_element].timestamp.map(function (d, i) {
                return {
                    "timestamp": d,
                    "actual_data": sevenD_forecast[coin_name][line_element].data[i]
                };
            });
        }
    })
})


// LINE DEFS

const forecast_area = forecast_chart.append('g').append("path")

const actual_data_forecast = forecast_chart.append('g').append("path")
const forecast_line = forecast_chart.append('g').append("path")

// AXIS
var sentiment_x_axis = forecast_chart.append("g")
    .attr("class", "line_axis_x")
    .attr("transform", "translate(0," + forecast_line_height + ")")

var sentiment_y_axis = forecast_chart.append("g")
    .attr("class", "line_axis_y")


function update_forecast(selectedGroup) {

    //Add X axis --> it is a date format
    var x_forecast = d3.scaleLinear()
        .domain([d3.min(sevenD_forecast[selectedGroup]["past_data"]["timestamp"]), d3.max(sevenD_forecast[selectedGroup]["forecast"]["timestamp"])])
        .range([0, forecast_line_width]);

    y_forecast_min = d3.min(sevenD_forecast[selectedGroup]["forecast"]["open_down_interval"])
    y_actual_min = d3.min(sevenD_forecast[selectedGroup]["past_data"]["data"])

    y_forecast_max = d3.max(sevenD_forecast[selectedGroup]["forecast"]["open_up_interval"])
    y_actual_max = d3.max(sevenD_forecast[selectedGroup]["past_data"]["data"])

    true_max = Math.max(y_forecast_max, y_actual_max)
    true_min = Math.min(y_forecast_min, y_actual_min)
    true_range = true_max - true_min

    var y_forecast = d3.scaleLinear()
        .domain([true_min - true_range * 0.1, true_max + true_range * 0.1])
        .range([forecast_line_height, 0]);

    sentiment_x_axis.call(d3.axisBottom(x_forecast).ticks(3).tickFormat(d => { return (new Date(d / 1000000)).toLocaleDateString("en-CA") }));
    sentiment_y_axis.call(d3.axisLeft(y_forecast).ticks(8));

    var rearranged_historical = formatted_forecast_data[selectedGroup]["actual"];

    actual_data_forecast.datum(rearranged_historical)
        .transition()
        .duration(1000)
        .attr("d", d3.line()
            .x(function (d) { return x_forecast(d.timestamp) })
            .y(function (d) { return y_forecast(+d.actual_data) })
        )
        .attr("stroke", function (d) { return myColor(selectedGroup) })
        .attr("stroke-width", "3px")
        .attr("fill", "none")
        .style("filter", "drop-shadow(0px 0px 5px " + myColor(selectedGroup) + ")")


    var rearranged_forecast = formatted_forecast_data[selectedGroup]["forecast"];

    // Forecast line indicating most likely forecast
    forecast_line.datum(rearranged_forecast)
        .transition()
        .duration(1000)
        .attr("d", d3.line()
            .curve(d3.curveBasis)
            .x(function (d) { return x_forecast(d.timestamp) })
            .y(function (d) { return y_forecast(+d.open_forecast) })
        )
        .attr("stroke", "white")
        .attr("stroke-width", "5px")
        .attr("fill", "none")
        .style("filter", "drop-shadow(0px 0px 5px white)")


    // confidence interval area
    forecast_area.datum(rearranged_forecast)
        .transition()
        .duration(1000)
        .attr("d", d3.area()
            .curve(d3.curveBasis)
            .x(function (d) { return x_forecast(d.timestamp) })
            .y1(function (d) { return y_forecast(+d.upper_bound) })
            .y0(function (d) { return y_forecast(+d.lower_bound) })
        )
        .attr("stroke", "none")
        .attr("stroke-width", "3px")
        .attr("fill", "grey")
        .style("opacity", 0.5)
        .style("filter", "drop-shadow(0px 0px 5px white)")

}