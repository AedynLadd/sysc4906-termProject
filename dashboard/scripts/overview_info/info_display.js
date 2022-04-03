var coin_map_to_slug = new Object()
var name_identifier = new Object()
top_100_coins.forEach(coin => coin_map_to_slug[coin.slug] = { "name": coin.name, "slug": coin.slug, "symbol": coin.symbol });
top_100_coins.forEach(coin => name_identifier[coin.symbol] = coin.name)

// calculate averages and top 10 connected coins
console.log(network_data)

rolling_average = {"avg": {"b": 0, "nb": 0, "d": 0}, "count": 0}

node_data_list = {}
id_to_name_map = {}
network_data["nodes"].forEach((node)=>{
    rolling_average.avg.b = (rolling_average.avg.b*rolling_average.count + node.data.betweeness)/(rolling_average.count+1)
    rolling_average.avg.nb = (rolling_average.avg.nb*rolling_average.count + node.data.normalized_betweeness)/(rolling_average.count+1)
    rolling_average.avg.d = (rolling_average.avg.d*rolling_average.count + node.data.degree)/(rolling_average.count+1)

    rolling_average.count += 1;

    id_to_name_map[node.id] = node.name
    node_data_list[node.name] = {
            "id": node.id, 
            "degree": node.data.degree,
            "betweeness": node.data.betweeness, 
            "normalized_betweeness":  node.data.normalized_betweeness, 
            "associated_keys": []
    }
});

network_data["links"].forEach((link)=>{ 
    node_data_list[id_to_name_map[link.source]]["associated_keys"].push({"target": id_to_name_map[link.target], "value": link.value })
    node_data_list[id_to_name_map[link.target]]["associated_keys"].push({"target": id_to_name_map[link.source], "value": link.value })
});

var overview_data = Object.keys(node_data_list).map(function(key) { 
    node_data_list[key].associated_keys.sort(function(first,second){ return second.value - first.value})
    return [key, node_data_list[key]];
});

overview_data.sort(function(first, second) { return second[1].degree - first[1].degree; });




function updateSubstat_cards(coin_data){
    if(coin_data == null){
        document.getElementById("coin_degree_title").innerHTML = "Degree"
        document.getElementById("coin_degree_subtitle").innerHTML = rolling_average.avg.d.toFixed(4)

        document.getElementById("coin_norm_betweeness_title").innerHTML = "Norm. Betweeness"
        document.getElementById("coin_norm_betweeness_subtitle").innerHTML = rolling_average.avg.nb.toFixed(4)

        document.getElementById("coin_betweeness_title").innerHTML = "Betweeness"
        document.getElementById("coin_betweeness_subtitle").innerHTML = rolling_average.avg.b.toFixed(4)
        
        return null
    } else {
        document.getElementById("coin_degree_title").innerHTML = "Degree"
        document.getElementById("coin_degree_subtitle").innerHTML = coin_data.data.degree.toFixed(4)

        document.getElementById("coin_norm_betweeness_title").innerHTML = "Norm. Betweeness"
        document.getElementById("coin_norm_betweeness_subtitle").innerHTML = coin_data.data.normalized_betweeness.toFixed(4)

        document.getElementById("coin_betweeness_title").innerHTML = "Betweeness"
        document.getElementById("coin_betweeness_subtitle").innerHTML = coin_data.data.betweeness.toFixed(4)
        
        return coin_data.data.degree.toFixed(4)
    }
}

function overview_table(){
    var base_div = document.getElementById("coin_stats_table")
    var base_tbl = document.createElement('table');

    base_tbl.className = "coin_stats_table disp"
    try {
        // Data keys
        // Append the data
        let max_rows = overview_data.length;
        let max_columns = 4;
        for (let rows = 0; rows <= (max_rows); rows++) {
            var tbl_row = base_tbl.insertRow();
            for (let columns = 0; columns <= (max_columns - 1); columns++) {
                
                var cell_element = tbl_row.insertCell();
                if (rows == 0) {
                    tbl_row.className = "coin_stats_table_headers"
                    cell_element.style.fontWeight = "bold";
                    switch(columns){
                        case 0:
                            cell_element.className = "coin_stats_table_symbol_cell"
                            cell_info = "Symbol"
                            break;
                        case 1:
                            cell_info = "Name"
                            break;
                        case 2:
                            cell_info = "Betweeness"
                            break;
                        case 3:
                            cell_info = "Degree"
                            break;
                        default:
                            cell_info = ""
                            break;
                    }
                } else {
                    var _row_overview_data = overview_data[rows-1]
                    switch(columns){
                        case 0:
                            cell_element.className = "coin_stats_table_symbol_cell"
                            cell_info = _row_overview_data[0]
                            break;
                        case 1:
                            cell_info = name_identifier[_row_overview_data[0]]
                            break;
                        case 2:
                            cell_info = _row_overview_data[1].betweeness.toFixed(4)
                            break;
                        case 3:
                            cell_info = _row_overview_data[1].degree.toFixed(4)
                            break;
                        default:
                            cell_info = ""
                            break;
                    }
                }

                cell_element.appendChild(document.createTextNode(cell_info + ''));
            }
        }

        // Create table
        base_div.innerHTML = ""
        base_div.append(base_tbl)
    } catch (ex){
        console.log(ex.toString())
        console.log("An error occured creating Table")
    }
}


function generate_coin_specific_table(coin_name){
    var base_div = document.getElementById("coin_stats_table")
    var base_tbl = document.createElement('table');

    console.log(node_data_list[coin_name.name].associated_keys)
    base_tbl.className = "coin_stats_table disp"
    try {
        // Data keys
        // Append the data
        let max_rows = node_data_list[coin_name.name].associated_keys.length;
        let max_columns = 3;
        for (let rows = 0; rows <= (max_rows); rows++) {
            var tbl_row = base_tbl.insertRow();
            for (let columns = 0; columns <= (max_columns - 1); columns++) {
                
                var cell_element = tbl_row.insertCell();
                if (rows == 0) {
                    tbl_row.className = "coin_stats_table_headers"
                    cell_element.style.fontWeight = "bold";
                    switch(columns){
                        case 0:
                            cell_element.className = "coin_stats_table_symbol_cell"
                            cell_info = "Symbol"
                            break;
                        case 1:
                            cell_info = "Name"
                            break;
                        case 2:
                            cell_info = "Number of Posts"
                            break;
                        default:
                            cell_info = ""
                            break;
                    }
                } else {
                    var _row_overview_data = node_data_list[coin_name.name].associated_keys[rows-1]
                    switch(columns){
                        case 0:
                            cell_element.className = "coin_stats_table_symbol_cell"
                            cell_info = _row_overview_data.target
                            break;
                        case 1:
                            cell_info = name_identifier[_row_overview_data.target]
                            break;
                        case 2:
                            cell_info = _row_overview_data.value
                            break;
                        default:
                            cell_info = ""
                            break;
                    }
                }

                cell_element.appendChild(document.createTextNode(cell_info + ''));
            }
        }

        // Create table
        base_div.innerHTML = ""
        base_div.append(base_tbl)
    } catch (ex){
        console.log(ex.toString())
        console.log("An error occured creating Table")
    }
}

function display_coin_info(coin_data) {
    console.log(coin_data)
    this_degree = updateSubstat_cards(coin_data)

    if (coin_data == null) {
        document.getElementById("additional_coin_info_box_title").innerHTML = "OVERVIEW"
        overview_table()
        document.getElementById("coin_stats_table").className = "coin_stats_table disp"
    } else {
        document.getElementById("additional_coin_info_box_title").innerHTML = name_identifier[coin_data.name.toUpperCase()].toUpperCase()
        console.log(this_degree)
        if(this_degree == 0){
            document.getElementById("coin_stats_table").innerHTML = "No Associated Coins"
            document.getElementById("coin_stats_table").className = "coin_stats_table nei"
        } else {
            generate_coin_specific_table(coin_data)
            document.getElementById("coin_stats_table").className = "coin_stats_table disp"
        }
    }
}

display_coin_info(null);
