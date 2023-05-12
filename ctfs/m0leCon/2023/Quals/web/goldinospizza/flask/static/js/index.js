/* global $ */

let keepalive = null;

function ready() {
    const ws = new WebSocket(`wss://${document.domain}:${location.port}/sock`);

    function sendMessage(sender, message) {
        ws.send(JSON.stringify(message));
    }

    function order(event) {
        let sender = $(event.currentTarget.closest(".product"));
        sendMessage(sender, {
            "request": "order",
            "orders": [{
                "product": parseInt(sender.attr("data-id"), 10),
                "quantity": parseInt(sender.find(":input[type=number]").val(), 10),
            }, ],
        });
    }
    $(".orderBtn").on("click", order);

    function cancel(event) {
        let sender = $(event.currentTarget.closest(".order"));
        sendMessage(sender, {
            "request": "cancel",
            "orders": [parseInt(sender.attr("data-id"), 10), ],
        });
    }

    function getBalance() {
        sendMessage(null, {
            "request": "balance",
        });
    }

    function getOrders() {
        sendMessage(null, {
            "request": "orders",
        });
    }

    ws.addEventListener("open", () => {
        getBalance();
        getOrders();
    });

    ws.addEventListener("close", event => {
        console.error(event.code, event.reason);
        setTimeout(ready, 500);
    });

    function orderTemplate(order) {
        let theme;
        switch (order.product.theme) {
            case 'golden':
                theme = "warning"
                break;
            case 'italian':
                theme = "success"
            case 'american':
                theme = "danger"
                break;
            default:
                theme = "primary";
        }
        return $("<div>").addClass(`order card text-bg-${theme} m-3`).attr("data-id", order.id).append(
            $("<div>").addClass("card-body").append(
                $("<div>").addClass("d-flex flex-row justify-content-around align-items-center align-content-center flex-wrap").append(
                    $("<h5>").addClass("card-title p-1").text(`${order.product.name}`),
                    $("<div>").addClass("card-text p-1").text(`${order.product_price.toFixed(2)}€`),
                    $("<div>").addClass("card-text p-1").text(`${order.product_quantity}#`),
                    $("<div>").addClass("card-text p-1").text(`tot: ${(order.product_price * order.product_quantity).toFixed(2)}€`),
                    $("<button>").addClass("cancelBtn btn btn-outline-light p-1").attr({
                        "type": "button",
                        "id": `order-button-${order.product_id}`
                    }).text("Cancel").on("click", cancel),
                ),
            ),
        );

    }

    ws.addEventListener(
        "message",
        event => {
            const message = JSON.parse(event.data);
            console.log(message);
            if (message.ok === true) {
                if ("balance" in message) {
                    $("#balance").text(`${message.balance.toFixed(2)}€`);
                }
                if ("orders" in message) {
                    $("#orders").empty();
                    message.orders.forEach((order) => {
                        $("#orders").append(orderTemplate(order));
                    })
                }
            } else {
                if ("error" in message) {
                    alert(message.error);
                    console.error(message.error);
                }
            }
        }
    );

    clearInterval(keepalive);
    keepalive = setInterval(getBalance, 25000);
}

$(document).ready(ready);
