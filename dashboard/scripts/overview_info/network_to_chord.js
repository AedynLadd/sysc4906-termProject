var coin_map_to_slug = new Object()
var name_identifier = new Object()
top_100_coins.forEach(coin => coin_map_to_slug[coin.slug] = { "name": coin.name, "slug": coin.slug, "symbol": coin.symbol });
top_100_coins.forEach(coin => name_identifier[coin.symbol] = coin.name)

var network_diagram_container = document.getElementById("keyword_network_diagram").getBoundingClientRect();

// set the dimensions and margins of the graph
const network_diagram = { top: 0, right: 0, bottom: 30, left: 0 },
    network_width = network_diagram_container.width - network_diagram.left - network_diagram.right,
    network_height = network_diagram_container.height - network_diagram.top - network_diagram.bottom;

var isChord = false;
var selected_node = null;

const network_svg = d3.select("#keyword_network_diagram")
    .append("svg")
    .attr("width", "100%")
    .attr("height", "100%")

// initialize the simulation forces
const simulation = d3.forceSimulation(network_data.nodes)
    .force("link", d3.forceLink()
        .id(function (d) { return d.id; })
        .links(network_data.links)
    )
    .force("charge", d3.forceManyBody().strength(-100))
    .force("x", d3.forceX(0))
    .force("y", d3.forceY(-50))
    .force("collide", d3.forceCollide(d => 30))

var allNodes = network_data.nodes.map(function (d) { return d.name })

var idToNode = {};
network_data.nodes.forEach(n => idToNode[n.id] = n);

var x = d3.scalePoint()
    .range([0, network_width])
    .domain(allNodes)

function circlify(point) {
    var theta = (Math.PI / (network_width / 2)) * x(point);
    var radius = (network_height / 2) * 0.90
    var y_value = radius * Math.sin(theta)
    var x_value = radius * Math.cos(theta)
    return [x_value, y_value]
}

var keyword_scale = d3.scaleLinear().range([0.8, 1]).domain([0, 100]);
var keyword_color_scale = d3.scaleSequential().interpolator(d3.interpolateMagma).domain([0, 100])

// Initialize Network diagrams
// Initialize the links
const link = network_svg.append("g").attr("id", "network_diagram_g")
    .attr("transform", "translate(" + network_width / 2 + ',' + network_height / 2 + ")")
    .selectAll("path")
    .data(network_data.links)
    .join("path")
    .attr("class", "networkGraph-link")
    .style("opacity", a => { return keyword_scale(network_keyword_count[a.source.name][a.target.name] == null ? 1 : network_keyword_count[a.source.name][a.target.name]) });

var graphNodes = network_svg.selectAll("g graphNodes")
    .data(network_data.nodes)

/*Create and place the "blocks" containing the circle and the text */
graphNodeEnter = graphNodes.enter()
    .append("g")

var node_color_scale = d3.scaleSequential().interpolator(d3.interpolateMagma).domain([0, 1])

const node = graphNodeEnter.attr("transform", "translate(" + network_width / 2 + ',' + network_height / 2 + ")")
    .append("circle")
    .attr("r", 9)
    .attr("class", "networkGraph-node")
    // .style("fill", (d) =>{
    //     return node_color_scale(d.data.normalized_betweeness)
    // })

const nodeLabel = graphNodeEnter.attr("transform", "translate(" + network_width / 2 + ',' + network_height / 2 + ")")
    .append("text")
    .attr("dx", d => { return -10 })
    .text(d => {
        try {
            return coin_map_to_slug[d.name.toLowerCase()].symbol
        } catch {
            return d.name
        }
    })
    .attr("class", "networkGraph-node-label")

// Add interactions
node.call(d3.drag()
    .on("start", drag_started)
    .on("drag", dragged)
    .on("end", drag_ended))
    .on('click', function (event, d) {
        selected_node = selected_node == d.id ? null : d.id;
        display_coin_info(selected_node == null ? null : d)
        // Highlight the node
        if (isChord) {
            // Highlight the links
            link.attr("class", a => {
                if (selected_node == null) {
                    return 'chord-link'
                }
                else {
                    return a.source.id === d.id || a.target.id === d.id ? 'chord-link-Highlighted' : 'chord-link'
                }
            })
                .style("opacity", a => {
                    if (selected_node == null) {
                        return 0.1;
                    } else {
                        return a.source.id === d.id || a.target.id === d.id ? 0.8 : 0.1;
                    }
                });;

            node.attr('class', a => a.id === d.id && selected_node != null ? 'networkGraph-node-Highlighted' : "networkGraph-node")
        } else {
            node.attr('class', a => a.id === d.id && selected_node != null ? 'networkGraph-node-Highlighted' : "networkGraph-node")
            // Highlight the links
            link.attr("class", a => {
                if (selected_node == null) {
                    return 'networkGraph-link'
                } else {
                    return a.source.id === d.id || a.target.id === d.id ? 'networkGraph-link-Highlighted' : 'networkGraph-link';
                }
            }).style("opacity", a => { return keyword_scale(network_keyword_count[a.source.name][a.target.name] == null ? 1 : network_keyword_count[a.source.name][a.target.name]) })
        }
    })
    .on('dblclick', function (event, d) {
        isChord = (isChord) ? false : true;
        selected_node = selected_node == d.id ? null : d.id;

        display_coin_info(selected_node == null ? null : d)
        if (isChord) {
            simulation.stop()
            //Highlight the selected!
            d3.select(this).attr('class', 'networkGraph-node-Highlighted')
            link.attr("class", a => a.source.id === d.id || a.target.id === d.id ? 'chord-link-Highlighted' : 'chord-link');

            node.transition()
                .duration(100)
                .attr("transform", function (d) {
                    coords = circlify(d.name);
                    return "translate(" + coords[0] + "," + coords[1] + ")"
                });

            nodeLabel.transition()
                .duration(100)
                .attr("class", 'chord-node-label')
                .attr("transform", function (d) {
                    coords = circlify(d.name);
                    return "translate(" + coords[0] + "," + coords[1] + ")"
                });

            link
                .transition()
                .duration(200)
                .attr("d", d => ["M", circlify(d.source.name)[0], circlify(d.source.name)[1],  // M P1X P1Y
                    "Q", 0, 0, // Q C1X C1Y
                    circlify(d.target.name)[0], circlify(d.target.name)[1] // P2X P2Y
                ].join(" ")) 
                .style("stroke", a => { return keyword_color_scale(network_keyword_count[a.source.name][a.target.name] == null ? 1 : network_keyword_count[a.source.name][a.target.name]) })
                .style("opacity", a => a.source.id === d.id || a.target.id === d.id ? 1 : 0.04);
        } else {
            simulation.restart();
            // Network highlighting
            node.attr('class', a => a.id === d.id ? 'networkGraph-node-Highlighted' : "networkGraph-node")
            // Highlight the links
            link.attr("class", a => a.source.id === d.id || a.target.id === d.id ? 'networkGraph-link-Highlighted' : 'networkGraph-link')
                .style("stroke", null)
                .style("opacity", a => { return keyword_scale(network_keyword_count[a.source.name][a.target.name] == null ? 1 : network_keyword_count[a.source.name][a.target.name]) });
            nodeLabel.attr('class', 'networkGraph-node-label')
        }

    });

function filter_coin_nodes(filter){
    node.style("stroke", function(d){
        if(filter == "") {
            return "rgba(82, 82, 82, 0.3)";
        }

        try{
            if(name_identifier[d.name.toUpperCase()].toUpperCase().indexOf(filter.toUpperCase()) > -1){
                return "red";
            } else {
                return "rgba(82, 82, 82, 0.3)";
            }
        } catch {
            return "rgba(82, 82, 82, 0.3)";
        }
    })
};

// Circle Dragging
function drag_started(event, d) {
    if (isChord) return;
    if (!event.active) simulation.alphaTarget(0.1).restart();
    d.fx = validate_point(d.x, network_width);
    d.fy = validate_point(d.y, network_height);

}

function dragged(event, d) {
    if (isChord) return;
    d.fx = validate_point(event.x, network_width);
    d.fy = validate_point(event.y, network_height);

}

function drag_ended(event, d) {
    if (isChord) return;
    if (!event.active) simulation.alphaTarget(0.1);
    d.fx = null;
    d.fy = null;

}

// Simulation
simulation.on("tick", ticked)

function ticked(transition_duration = 50) {
    link.transition()
        .duration(transition_duration)
        .attr("d", d => "M" + validate_point(d.source.x, network_width) + " " + validate_point(d.source.y, network_height) + "L" + validate_point(d.target.x, network_width) + " " + validate_point(d.target.y, network_width) + "Z");
    node.transition()
        .duration(transition_duration)
        .attr("transform", function (d) {
            return "translate(" + validate_point(d.x, network_width) + "," + validate_point(d.y, network_height) + ")";
        })
    nodeLabel.transition()
        .duration(transition_duration)
        .attr("transform", function (d) {
            return "translate(" + validate_point(d.x, network_width) + "," + validate_point(d.y, network_height - 15) + ")";
        })

}

function validate_point(point, bounds) {
    bounds = bounds / 2
    return (Math.abs(point) < bounds ? point : Math.sign(point) * bounds);
}

function simulation_visible(isVisible){
    if(isVisible){}
    else { simulation.stop(); }
}