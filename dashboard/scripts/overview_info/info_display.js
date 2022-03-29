var coin_map_to_slug = new Object()
top_100_coins.forEach(coin => coin_map_to_slug[coin.slug] = { "name": coin.name, "slug": coin.slug, "symbol": coin.symbol });


function display_coin_info(coin_data) {
    if (coin_data == null) {
        console.log("displaying an overview")
        document.getElementById("additional_coin_info_box_title").innerHTML = "OVERVIEW"
    } else {
        console.log("displaying info on a specific coin")
        document.getElementById("additional_coin_info_box_title").innerHTML = coin_data.name.toUpperCase()
    }
}

display_coin_info(null);
