const orderitemslist = []
function addItem(itemID) {
    console.log(itemID)
    orderitemslist.push(itemID)
    console.log(orderitemslist)
    return orderitemslist;
}  

function sendlist() {
    console.log(orderitemslist)
    const request = new XMLHttpRequest()
    request.open("POST", `/cart/${(orderitemslist)}`)
    request.send()
}

function delay(URL) {
    setTimeout( function() { window.location = URL }, 500 );
}