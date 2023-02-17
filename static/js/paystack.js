function beforeRequestPayment() {
    const loaderContainer = document.getElementById("loader-container")
    const orderContainer = document.getElementById("order-container")
    orderContainer.classList.add("d-none")
    loaderContainer.classList.remove("d-none")
}

function afterRequestPayment(status) {
    const loaderContainer = document.getElementById("alert")
    const orderContainer = document.getElementById("alert")
    orderContainer.classList.remove("d-none")
    loaderContainer.classList.add("d-none")
}

function getReceipt(response) {
    // todo: add befored send 
    const orderNumber = response.reference
    const method = 'POST'
    const requestUrl = '/orders/make-payment/'
    const responseType = "json"
    const data = JSON.stringify({ order_number: orderNumber })
    const xhr = new XMLHttpRequest()
    const csrftoken = getCookie("csrftoken")
    xhr.open(method, requestUrl)
    xhr.responseType = responseType
    xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest")
    xhr.setRequestHeader("HTTP_X_REQUESTED_WITH", "XMLHttpRequest")
    xhr.setRequestHeader("Content-Type", "application/json")
    xhr.setRequestHeader("X-CSRFToken", csrftoken)
    xhr.onload = function () {
        const response = xhr.response
        console.log(response)
        if (xhr.status === 200) {
            window.open(`/orders/receipt/${orderNumber}`, '_self')
            afterRequestPayment()
        }
    }
    xhr.send(data)
}

function payWithPaystack(response) {
    const email = response.serializer.email
    const amount = parseInt(response.serializer.order_total)
    console.log(amount)
    const ref = response.serializer.order_number
    const public_key = response.public_key
    let handler = PaystackPop.setup({
        key: public_key,
        email: email,
        amount: amount * 100,
        ref: ref,
        onClose: function () {
            alert('Window closed.');
        },
        callback: function (response) {
            console.log(response)
            beforeRequestPayment()
            let message = 'Payment complete! Reference: ' + response.reference;
            alert(message);
            getReceipt(response)
        }
    });

    handler.openIframe();
}

function paymentRequest(order_id) {
    // todo: add befored send 
    const orderId = order_id
    const method = 'POST'
    const requestUrl = '/orders/detail/'
    const responseType = "json"
    const data = JSON.stringify({ order_id: orderId })
    const xhr = new XMLHttpRequest()
    const csrftoken = getCookie("csrftoken")
    xhr.open(method, requestUrl)
    xhr.responseType = responseType
    xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest")
    xhr.setRequestHeader("HTTP_X_REQUESTED_WITH", "XMLHttpRequest")
    xhr.setRequestHeader("Content-Type", "application/json")
    xhr.setRequestHeader("X-CSRFToken", csrftoken)
    xhr.onload = function () {
        const response = xhr.response
        console.log(response)
        if (xhr.status === 200) {
            payWithPaystack(response)
        }
    }
    xhr.send(data)
}