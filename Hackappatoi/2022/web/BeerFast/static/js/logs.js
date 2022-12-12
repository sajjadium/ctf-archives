let applylog = () => {
    var log = document.getElementById("log");
    document.location.href = "/logs?type=" + log.value;
}