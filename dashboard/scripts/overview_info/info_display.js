var coin_map_to_slug = new Object()
top_100_coins.forEach(coin => coin_map_to_slug[coin.slug] = { "name": coin.name, "slug": coin.slug, "symbol": coin.symbol });

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

const coin_joyplot_lines = new Object();


trueJoy_height = joyplot_diagram_height * 10

var yName = d3.scaleBand()
    .domain(Object.keys(formatted_historical_data))
    .range([joyplot_diagram_height, trueJoy_height])
    .paddingInner(1)


Object.keys(formatted_historical_data).forEach((key_name) => {
    let joy_x = d3.scaleLinear()
        .domain(d3.extent(historical_coin_data[key_name]["timestamp"], function (d) { return new Date(d) }))
        .range([0, joyplot_diagram_width]);

    // y axis data
    let y_min = d3.min(historical_coin_data[key_name]["open"], function (d) { return d })
    let y_max = d3.max(historical_coin_data[key_name]["open"], function (d) { return d })
    let y_range = y_max - y_min

    var joy_y = d3.scaleLinear()
        .domain([y_min - y_range * 0.1, y_max + y_range * 0.1])
        .range([0, yName.step()])

    // Define the area 
    let area = coin_joyplot_svg
        .append('g')
        .append("path")
        .attr("id", "joy_lines_" + coin_map_to_name[key_name.toLowerCase()].slug)
        .attr("transform", (d) => "translate(0," + (yName(key_name) - joyplot_diagram_height) + ")");

    area.datum(formatted_historical_data[key_name])
        .attr("stroke", "#000")
        .attr("stroke-width", 3)
        .attr("d", d3.line()
            .curve(d3.curveBasis)
            .x((d) => joy_x(new Date(d.timestamp)))
            .y((d) => joy_y(d.data))
        )
        .attr("fill", "none")
        .style("opacity", 0.5)
});

function filter_joy_plot(coin_data) {
    let associated_coins;
    try {
        associated_coins = Object.keys(network_keyword_count[coin_data.name])
    } catch {
        associated_coins = null;
    }
    top_100_coins.forEach((coin_in_list) => {

        let opacity = 0.1
        try {
            if (associated_coins.indexOf(coin_in_list.slug) != -1) {
                opacity = 0.9
            }
        } catch {
            opacity = 0.5
        } finally {

            d3.selectAll("#joy_lines_" + coin_in_list.slug)
                .transition()
                .duration(500)
                .style("opacity", opacity)
                .attr("stroke", coin_data == null || coin_in_list.slug != coin_data.name ? "#000" : "#AAA")
                .transition()
                .duration(100)
                .attr("filter", coin_data == null || coin_in_list.slug != coin_data.name ? "none" : ("drop-shadow(0px 0px 5px #CCC)"));
        }
    })

}

function display_coin_info(coin_data) {
    filter_joy_plot(coin_data)
    if (coin_data == null) {
        console.log("displaying an overview")
        document.getElementById("additional_coin_info_box_title").innerHTML = "OVERVIEW"
    } else {
        console.log("displaying info on a specific coin")
        document.getElementById("additional_coin_info_box_title").innerHTML = coin_data.name.toUpperCase()
    }
}

display_coin_info(null);
