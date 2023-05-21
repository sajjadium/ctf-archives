function checkType(param)
{
    return typeof param === "string";
}

function visit_url(url)
{
    return true;
}

module.exports = {
    checkType,
    visit_url
}