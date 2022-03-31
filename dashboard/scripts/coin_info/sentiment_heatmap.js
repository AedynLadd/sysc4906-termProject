////
// DATA
////
// Rearrange our top coin data so that its usefull to us
var coin_map_to_name = new Object()
top_100_coins.forEach(coin => coin_map_to_name[coin.name.toLowerCase()] = { "name": coin.name, "slug": coin.slug, "symbol": coin.symbol });

////
// CONTAINER
////
var heatmap_container_bounds = document.getElementById("coin_sentiment_heatmap").getBoundingClientRect();

// set the dimensions and margins of the graph
const heat_margin = { top: 10, right: 30, bottom: 30, left: 50 },
    heat_width = heatmap_container_bounds.width - heat_margin.left - heat_margin.right,
    heat_height = heatmap_container_bounds.height - heat_margin.top - heat_margin.bottom;

// append the svg object to the body of the page
const heat_svg = d3.select("#coin_sentiment_heatmap")
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

// Build X scales and axis:
var heat_x = d3.scaleBand()
    .range([0, heat_width])
    .domain(Dates)
    .padding(0);

// Build Y scales and axis:
var heat_y = d3.scaleBand()
    .range([heat_height, 0])
    .domain(Subreddits)
    .padding(0);


var heat_x_range = d3.scaleLinear()
    .domain([d3.min(Dates), d3.max(Dates)])
    .range([0, heat_width]);

var heat_x_axis = heat_svg.append("g")
    .attr("class", "heatmap_axis")
    .attr("transform", "translate(0," + heat_height + ")")
    .call(d3.axisBottom(heat_x_range).tickFormat(d => { return (new Date(d)).toLocaleDateString("en-CA") }));


var heat_y_axis = heat_svg.append("g")
    .attr("class", "heatmap_axis")
//     .call(d3.axisLeft(heat_y).tickSize(0));

// heat_y_axis.selectAll(".tick text")
//     .style("font-size", "10px")

fill_data = []
Dates.forEach(thisDate => { Subreddits.forEach(thisSub => { fill_data.push({ "timestamp": thisDate, "subreddit": thisSub, "value": 0 }) }) });

// Create Heatmap elements
heat_svg.selectAll(".sentiment_map")
    .data(fill_data)
    .enter()
    .append("rect")
    .attr("class", "sentiment_map")
    .attr("x", function (d) { return heat_x(d["timestamp"]) })
    .attr("y", function (d) { return heat_y(d["subreddit"]) })
    .attr("width", heat_x.bandwidth())
    .attr("height", heat_y.bandwidth())
    .style("opacity", 0.5);


// Create Labels
var sentiment_label_enter = heat_svg.selectAll(".heatMapRedditNames")
    .data(Array.from(Subreddits))
    .enter()
    .append("g").attr("class", "heatMapRedditNames").on("mouseover", function(event, d){
        
    })

sentiment_label_enter.append("rect")
    .attr("x", 0)
    .attr("y", d => heat_y(d) )
    .attr("width", heat_width)
    .attr("height", heat_y.bandwidth())

sentiment_label_enter.append("text")
    .attr("class", "heatMapRedditNames Labels")
    .attr("x", heat_width*0.1)
    .attr("y", function (d) { return heat_y(d) + heat_y.bandwidth()/2 })
    .text(d => {
        return "r/" + d
    })
    .style("font-size", heat_y.bandwidth()/2)

var heatMapColor = d3.scaleSequential()
    .interpolator(d3.interpolateInferno)
    .domain([0, 1])

day_summary_data = new Object();

function sentiment_heatmap(selectedGroup) {
    var selectedGroup = selectedGroup.split("_").join(" ")

    var keywords_of_interest = Object.values(coin_map_to_name[selectedGroup.toLowerCase()])

    var day_summary_data = new Object();
    var rearranged_data = new Object();
    var highest_val = 0;
    var lowest_val = 0;

    Object.values(reddit_summary).forEach(val => {
        let overall_score = 0;
        Object.entries(val.keyword_based_sentiment).forEach(keyword_val => {
            if (keywords_of_interest.includes(keyword_val[0])) {
                overall_score += keyword_val[1].sentiment*keyword_val[1].count
            }
        });
        rearranged_data[val.timestamp + ":" + val.source] = overall_score;

        if(overall_score > highest_val){
            highest_val = overall_score
        }

        if(overall_score < lowest_val){
            lowest_val = overall_score
        }

        day_summary_data[val.timestamp] = day_summary_data[val.timestamp] == null ? overall_score : (day_summary_data[val.timestamp] + overall_score);
    });


    heat_svg.selectAll(".sentiment_map")
        .transition()
        .duration(1000)
        .style("fill", function (d) {
            console.log(rearranged_data[d.timestamp + ":" + d.subreddit])
            if (rearranged_data[d.timestamp + ":" + d.subreddit] != null) {
                //return heatMapColor(rearranged_data[d.timestamp + ":" + d.subreddit] / highest_val);
                return heatMapColor(Math.log(rearranged_data[d.timestamp + ":" + d.subreddit])/ Math.log(highest_val));
            } else {
                console.log("Is this running ever?")
                return heatMapColor(d.val)
            }
        });
}



