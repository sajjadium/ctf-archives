//helper functions, it turned out chrome doesn't support Math.sgn() 
function signum(x) {
    return (x < 0) ? -1 : 1;
}
function absolute(x) {
    return (x < 0) ? -x : x;
}

function drawPath(svg, path, startX, startY, endX, endY, direction) {
    // get the path's stroke width (if one wanted to be  really precize, one could use half the stroke size)
    var stroke =  parseFloat(path.attr("stroke-width"));
    // check if the svg is big enough to draw the path, if not, set heigh/width
    if (svg.attr("height") <  endY)                 svg.attr("height", endY+20);
    if (svg.attr("width" ) < (startX + stroke) )    svg.attr("width", (startX + stroke));
    if (svg.attr("width" ) < (endX   + stroke) )    svg.attr("width", (endX   + stroke));
    
    var deltaX = (endX - startX) * 0.15;
    var deltaY = (endY - startY) * 0.15;
    // for further calculations which ever is the shortest distance
    var delta  =  deltaY < absolute(deltaX) ? deltaY : absolute(deltaX);

    // set sweep-flag (counter/clock-wise)
    // if start element is closer to the left edge,
    // draw the first arc counter-clockwise, and the second one clock-wise
    var arc1 = 0; var arc2 = 1;
    if (startX > endX) {
        arc1 = 1;
        arc2 = 0;
    }
    // draw tha pipe-like path
    // 1. move a bit down, 2. arch,  3. move a bit to the right, 4.arch, 5. move down to the end 
    // path.attr("d",  "M"  + startX + " " + startY +
    // " V" + (startY + delta) +
    // " A" + delta + " " +  delta + " 0 0 " + arc1 + " " + (startX + delta*signum(deltaX)) + " " + (startY + 2*delta) +
    // " H" + (endX - delta*signum(deltaX)) + 
    // " A" + delta + " " +  delta + " 0 0 " + arc2 + " " + endX + " " + (startY + 3*delta) +
    // " V" + endY +
    // " A" + delta + " " +  delta + " 0 0 " + arc1 + " " + (endX + delta*signum(deltaX)) + " " + (endY + 2*delta));

    //" A" + delta + " " +  delta + " 0 0 " + arc2 + " " + (endX + delta*signum(delta)) + " " + (endY + 2*delta)

    if( direction == "left")
    {
        path.attr("d",  "M"  + startX + " " + startY +
        " V" + (startY + delta) +
        " A" + delta + " " +  delta + " 0 0 " + arc1 + " " + (startX + delta*signum(deltaX)) + " " + (startY + 2*delta) +
        " H" + (endX - delta*signum(deltaX)) + 
        " A" + delta + " " +  delta + " 0 0 " + arc2 + " " + endX + " " + (startY + 3*delta) +
        " V" + (endY-delta*0.5) +
        " A" + delta + " " +  delta + " 0 0 " + arc1 + " " + (endX+delta*signum(deltaX)) + " " + (endY+5)
        );
    }
    else if( direction == "right")
    {
        console.log(startX+" " +startY+" " + endX + " " + endY + " " + deltaX + " ");
        path.attr("d",  "M"  + startX + " " + startY +
        " V" + (startY + delta) +
        " A" + delta + " " +  delta + " 0 0 " + arc1 + " " + (startX + delta*signum(deltaX)) + " " + (startY + 2*delta) +
        " H" + (endX - delta*signum(deltaX)) + 
        " A" + delta + " " +  delta + " 0 0 " + arc2 + " " + endX + " " + (startY + 3*delta) +
        " V" + (endY-delta*0.5) +
        " A" + delta + " " +  delta + " 0 0 " + arc1 + " " + (endX+delta*signum(deltaX)) + " " + (endY+5));
    }
    else
    {
        path.attr("d",  "M"  + startX + " " + startY +
        " V" + (startY + delta) +
        " A" + delta + " " +  delta + " 0 0 " + arc1 + " " + (startX + delta*signum(deltaX)) + " " + (startY + 2*delta) +
        " H" + (endX - delta*signum(deltaX)) + 
        " A" + delta + " " +  delta + " 0 0 " + arc2 + " " + endX + " " + (startY + 3*delta) +
        " V" + endY );
    }
}

function connectElements(svg, path, startElem, endElem, direction) {
    var svgContainer= $("#svgContainer");

    // if first element is lower than the second, swap!
    if(startElem.offset().top > endElem.offset().top){
        var temp = startElem;
        startElem = endElem;
        endElem = temp;
    }

    // get (top, left) corner coordinates of the svg container   
    var svgTop  = svgContainer.offset().top;
    var svgLeft = svgContainer.offset().left;

    // get (top, left) coordinates for the two elements
    var startCoord = startElem.offset();
    var endCoord   = endElem.offset();

    // calculate path's start (x,y)  coords
    // we want the x coordinate to visually result in the element's mid point
    var startX = startCoord.left + 0.5*startElem.outerWidth() - svgLeft;    // x = left offset + 0.5*width - svg's left offset
    var startY = startCoord.top  + startElem.outerHeight() - svgTop;        // y = top offset + height - svg's top offset

        // calculate path's end (x,y) coords
    
    if( direction == "left" )
    {
        var endX = endCoord.left - svgLeft - 18;
        var endY = endCoord.top  + 0.5*endElem.outerHeight() - svgTop;
    }
    else if( direction == "right")
    {
        var endX = endCoord.left + endElem.outerWidth() - svgLeft  + 18;
        var endY = endCoord.top  + 0.5*endElem.outerHeight() - svgTop;
    }
    else
    {
        var endX = endCoord.left + 0.5*endElem.outerWidth() - svgLeft;
        var endY = endCoord.top  - svgTop;
    }


    // call function for drawing the path
    drawPath(svg, path, startX, startY, endX, endY, direction);

}



function connectAll() {
    // connect all the paths you want!
    connectElements($("#svg1"), $("#path1"), $("#chal1"),   $("#chal2"), "top");
    connectElements($("#svg1"), $("#path2"), $("#chal1"),   $("#chal3"), "top");
    connectElements($("#svg1"), $("#path3"), $("#chal2"),   $("#chal4"), "top");
    connectElements($("#svg1"), $("#path4"), $("#chal3"),   $("#chal5"), "top");
    connectElements($("#svg1"), $("#path5"), $("#chal3"),   $("#chal6"), "top");
    connectElements($("#svg1"), $("#path6"), $("#chal4"),   $("#chal7"), "left");
    connectElements($("#svg1"), $("#path7"), $("#chal5"),   $("#chal7"), "top");
    connectElements($("#svg1"), $("#path8"), $("#chal6"),   $("#chal7"), "right");

}

$(document).ready(function() {
    // reset svg each time 
    $("#svg1").attr("height", "0");
    $("#svg1").attr("width", "0");
    connectAll();
});

$(window).resize(function () {
    // reset svg each time 
    $("#svg1").attr("height", "0");
    $("#svg1").attr("width", "0");
    connectAll();
});

$(".panel").click(function(){
    for( i = 0; i <= 100; i++ )
    {
        setTimeout(function() {
            //your code to be executed after 1 second
            $("#svg1").attr("height", "0");
            $("#svg1").attr("width", "0");
            connectAll();
          }, 50);
    }
});