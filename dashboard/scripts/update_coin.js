
var last_selected_element = null;

const display_specific_coin = document.getElementById("coin_info_container")
const display_coins_overview = document.getElementById("overview_info_container")

function search_coin() {
    // Declare variables
    var input, filter, ul, li, a, i;
    input = document.getElementById("coinSearch");
    filter = input.value.toUpperCase();
    ul = document.getElementById("coin_select");
    li = ul.getElementsByTagName("li");

    // Loop through all list items, and hide those who don't match the search query
    for (i = 0; i < li.length; i++) {
        a = li[i].getElementsByTagName("a")[0];
        if (a.innerHTML.toUpperCase().indexOf(filter) > -1) {
            li[i].style.display = "";
        } else {
            li[i].style.display = "none";
        }
    }

}

function update(selectedCoin) {
    console.log(selectedCoin)
   
    try { document.getElementById("coin_id_" + selectedCoin).className = "coin_selected" } catch {}
    try { document.getElementById("coin_id_" + last_selected_element).className = "coin_label" } catch {}


    last_selected_element = selectedCoin
    if (selectedCoin == null) {
        display_specific_coin.style.display = "none";
        display_coins_overview.style.display = "grid";
    } else {
        console.log("displaying a specific coin")
        display_coins_overview.style.display = "none";
        display_specific_coin.style.display = "grid";
        update_graph(selectedCoin)
        sentiment_heatmap(selectedCoin)
    }


}

update(null)