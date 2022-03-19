
var last_selected_element = null;

function update(selectedCoin) {
    try {
        if (selectedCoin != last_selected_element) {
            document.getElementById("coin_id_" + selectedCoin).className = "coin_selected";
            document.getElementById("coin_id_" + last_selected_element).className = "coin_label";
        }
    } catch {
        console.log("An Error Occured on Update")
    }

    last_selected_element = selectedCoin
    update_graph(selectedCoin)
    sentiment_heatmap(selectedCoin)
}

update("Bitcoin")