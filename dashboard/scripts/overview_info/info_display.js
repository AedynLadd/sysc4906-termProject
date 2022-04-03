var coin_map_to_slug = new Object()
var name_identifier = new Object()
top_100_coins.forEach(coin => coin_map_to_slug[coin.slug] = { "name": coin.name, "slug": coin.slug, "symbol": coin.symbol });
top_100_coins.forEach(coin => name_identifier[coin.symbol] = coin.name)

// calculate averages and top 10 connected coins
console.log(network_data)

rolling_average = {"avg": {"b": 0, "nb": 0, "d": 0}, "count": 0}

network_data["nodes"].forEach((node)=>{
    rolling_average.avg.b = (rolling_average.avg.b*rolling_average.count + node.data.betweeness)/(rolling_average.count+1)
    rolling_average.avg.nb = (rolling_average.avg.nb*rolling_average.count + node.data.normalized_betweeness)/(rolling_average.count+1)
    rolling_average.avg.d = (rolling_average.avg.d*rolling_average.count + node.data.degree)/(rolling_average.count+1)

    rolling_average.count += 1;
})

console.log(rolling_average)


function updateSubstat_cards(coin_data){
    if(coin_data == null){
        document.getElementById("coin_degree_title").innerHTML = "Degree"
        document.getElementById("coin_degree_subtitle").innerHTML = rolling_average.avg.d.toFixed(4)

        document.getElementById("coin_norm_betweeness_title").innerHTML = "Norm. Betweeness"
        document.getElementById("coin_norm_betweeness_subtitle").innerHTML = rolling_average.avg.nb.toFixed(4)

        document.getElementById("coin_betweeness_title").innerHTML = "Betweeness"
        document.getElementById("coin_betweeness_subtitle").innerHTML = rolling_average.avg.b.toFixed(4)
    } else {
        document.getElementById("coin_degree_title").innerHTML = "Degree"
        document.getElementById("coin_degree_subtitle").innerHTML = coin_data.data.degree.toFixed(4)

        document.getElementById("coin_norm_betweeness_title").innerHTML = "Norm. Betweeness"
        document.getElementById("coin_norm_betweeness_subtitle").innerHTML = coin_data.data.normalized_betweeness.toFixed(4)

        document.getElementById("coin_betweeness_title").innerHTML = "Betweeness"
        document.getElementById("coin_betweeness_subtitle").innerHTML = coin_data.data.betweeness.toFixed(4)
    }
}

function display_coin_info(coin_data) {
    console.log(coin_data)
    updateSubstat_cards(coin_data)

    if (coin_data == null) {
        document.getElementById("additional_coin_info_box_title").innerHTML = "OVERVIEW"
    } else {
        document.getElementById("additional_coin_info_box_title").innerHTML = name_identifier[coin_data.name.toUpperCase()].toUpperCase()
    }
}

display_coin_info(null);
