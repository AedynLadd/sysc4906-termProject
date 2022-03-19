////
// DATA
////
// Rearrange our top coin data so that its usefull to us
var coin_map_to_name = new Object()
top_100_coins.forEach(coin => coin_map_to_name[coin.name] = { "name": coin.name, "slug": coin.slug, "symbol": coin.symbol });


////
// CONTAINER
////
var heatmap_container_bounds = document.getElementById("coin_sentiment_heatmap").getBoundingClientRect();

// set the dimensions and margins of the graph
const heat_margin = { top: 10, right: 30, bottom: 30, left: 60 },
    heat_width = heatmap_container_bounds.width - heat_margin.left - heat_margin.right,
    heat_height = heatmap_container_bounds.height - heat_margin.top - heat_margin.bottom;

// append the svg object to the body of the page
const heat_svg = d3.select("#coin_chart_data")
    .append("svg")
    .attr("width", heat_width + heat_margin.left + heat_margin.right)
    .attr("height", heat_height + heat_margin.top + heat_margin.bottom)
    .append("g")
    .attr("transform", `translate(${heat_margin.left}, ${heat_margin.top})`);

var Dates = new Set()
var Subreddits = new Set() // Could also make these subreddits instead

Object.values(reddit_summary).forEach(val => {
    Subreddits.add(val.source)
    Dates.add(val.timestamp)
})

function sentiment_heatmap(selectedGroup) {
    selectedGroup = selectedGroup.split("_").join(" ")

    var keywords_of_interest = Object.values(coin_map_to_name[selectedGroup])

    var rearranged_data = []
    Object.values(reddit_summary).forEach(val => {
        let overall_score = 0; 
        Object.entries(val.keyword_based_sentiment).forEach(keyword_val => {
            if (keywords_of_interest.includes(keyword_val[0])) {
                overall_score += keyword_val[1].sentiment
            }
        });
        rearranged_data.push({ "timestamp": val.timestamp, "subreddit": val.source, "value": overall_score });
    });

    // Build X scales and axis:
    var x = d3.scaleBand()
        .range([0, heat_width])
        .domain(Dates)
        .padding(0);

    // Build Y scales and axis:
    var y = d3.scaleBand()
        .range([heat_height, 0])
        .domain(Subreddits)
        .padding(0);

    // Build color scale
    var myColor = d3.scaleSequential()
        .interpolator(d3.interpolateInferno)
        .domain([0, 1])

    // add the squares
    heat_svg.selectAll("rect").remove();

    heat_svg.selectAll()
        .data(rearranged_data)
        .enter()
        .append("rect")
        .attr("x", function (d) { return x(d["timestamp"]) })
        .attr("y", function (d) { return y(d["subreddit"]) })
        .attr("width", x.bandwidth())
        .attr("height", y.bandwidth())
        .style("fill", function (d) { return myColor(d.value) })
        .style("stroke-width", 0)
        .style("stroke", "none")
        .style("opacity", 0.5)
}
