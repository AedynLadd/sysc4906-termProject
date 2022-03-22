var network_diagram_container = document.getElementById("keyword_network_diagram").getBoundingClientRect();

// set the dimensions and margins of the graph
const network_diagram = { top: 0, right: 30, bottom: 30, left: 60 },
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
    .force("charge", d3.forceManyBody().strength(-200))
    .force("x", d3.forceX(0))
    .force("y", d3.forceY(0))
    .force("collide", d3.forceCollide(d => 30))

var allNodes = network_data.nodes.map(function (d) { return d.name })

var idToNode = {};
network_data.nodes.forEach(n => idToNode[n.id] = n);

var x = d3.scalePoint()
    .range([0, network_width])
    .domain(allNodes)


function circlify(point) {
    var theta = (Math.PI / (network_width/2)) * x(point);
    var radius = (network_height / 2) * 0.90
    var y_value = radius * Math.sin(theta)
    var x_value = radius * Math.cos(theta)
    return [x_value, y_value]
}

// Initialize Network diagrams
// Initialize the links
const link = network_svg.append("g").attr("id", "network_diagram_g")
    .attr("transform", "translate(" + network_width / 2 + ',' + network_height / 2 + ")")
    .selectAll("path")
    .data(network_data.links)
    .join("path")
    .attr("class", "networkGraph-link")

// Initialize the nodes
const node = network_svg.append("g").attr("transform", "translate(" + network_width / 2 + ',' + network_height / 2 + ")")
    .selectAll("circle")
    .data(network_data.nodes)
    .join("circle")
    .attr("r", 10)
    .attr("class", "networkGraph-node")

// Add interactions
node.call(d3.drag()
    .on("start", drag_started)
    .on("drag", dragged)
    .on("end", drag_ended))
    .on('click', function (event, d) {
        selected_node = selected_node == d.id ? null : d.id;
        // Highlight the node
        if (isChord) {
            // Highlight the links
            link.attr("class", a => a.source.id === d.id || a.target.id === d.id && selected_node != null ? 'chord-link-Highlighted' : 'chord-link');
            node.attr('class', a => a.id === d.id && selected_node != null ? 'networkGraph-node-Highlighted' : "networkGraph-node")
        } else {
            node.attr('class', a => a.id === d.id && selected_node != null ? 'networkGraph-node-Highlighted' : "networkGraph-node")
            // Highlight the links
            link.attr("class", a => a.source.id === d.id || a.target.id === d.id && selected_node != null ? 'networkGraph-link-Highlighted' : 'networkGraph-link');
        }

        if(selected_node != null){
            // hide the menu and expand the grid
            console.log("showing menu")
        } else {
            // show the menu
            console.log("hiding menu")
        }

    })
    .on('dblclick', function (event, d) {
        isChord = (isChord) ? false : true;
        selected_node = selected_node == d.id ? null : d.id;
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

            link
                .transition()
                .duration(200)
                .attr("d", d => ["M", circlify(d.source.name)[0], circlify(d.source.name)[1],  // M P1X P1Y
                    "Q", 0, 0, // Q C1X C1Y
                    circlify(d.target.name)[0], circlify(d.target.name)[1]].join(" ")); // P2X P2Y
        } else {
            simulation.restart();
            // Network highlighting
            node.attr('class', a => a.id === d.id ? 'networkGraph-node-Highlighted' : "networkGraph-node")
            // Highlight the links
            link.attr("class", a => a.source.id === d.id || a.target.id === d.id ? 'networkGraph-link-Highlighted' : 'networkGraph-link');
        }

    });


// Circle Dragging
function drag_started(event, d) {
    if (isChord) return;
    if (!event.active) simulation.alphaTarget(0.001).restart();
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
    if (!event.active) simulation.alphaTarget(.03);
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

}

function validate_point(point, bounds) {
    bounds = bounds / 2
    return (Math.abs(point) < bounds ? point : Math.sign(point) * bounds);
}