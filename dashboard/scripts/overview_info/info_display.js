var coin_map_to_slug = new Object()
var name_identifier = new Object()
top_100_coins.forEach(coin => coin_map_to_slug[coin.slug] = { "name": coin.name, "slug": coin.slug, "symbol": coin.symbol });
top_100_coins.forEach(coin => name_identifier[coin.symbol] = coin.name)

function display_coin_info(coin_data) {
    if (coin_data == null) {
        document.getElementById("additional_coin_info_box_title").innerHTML = "OVERVIEW"
    } else {
        document.getElementById("additional_coin_info_box_title").innerHTML = name_identifier[coin_data.name.toUpperCase()].toUpperCase()
    }
}

display_coin_info(null);
