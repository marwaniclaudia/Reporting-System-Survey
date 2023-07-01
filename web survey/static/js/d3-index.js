// First define your cloud data, using `text` and `size` properties:
var skillsToDraw = []
getvalue = document.getElementsByClassName('valueName')
getsize = document.getElementsByClassName('valueSize')
for(var s=0; s<getvalue.length;s++){
    skillsToDraw.push({
        text:getvalue[s].innerHTML, size:getsize[s].innerHTML
    })
}
// Next you need to use the layout script to calculate the placement, rotation and size of each word:

var width = 500;
var height = 500;
var fill = d3.scale.category20();

d3.layout.cloud()
    .size([width, height])
    .words(skillsToDraw)
    .rotate(function() {
        return ~~(Math.random() * 2) * 90;
    })
    .font("Impact")
    .fontSize(function(d) {
        return d.size;
    })
    .on("end", drawSkillCloud)
    .start();

// Finally implement `drawSkillCloud`, which performs the D3 drawing:

// apply D3.js drawing API
function drawSkillCloud(words) {
    d3.select("#cloud").append("svg")
        .attr("width", width)
        .attr("height", height)
        .append("g")
        .attr("transform", "translate(" + ~~(width / 2) + "," + ~~(height / 2) + ")")
        .selectAll("text")
        .data(words)
        .enter().append("text")
        .style("font-size", function(d) {
            return d.size + "px";
        })
        .style("-webkit-touch-callout", "none")
        .style("-webkit-user-select", "none")
        .style("-khtml-user-select", "none")
        .style("-moz-user-select", "none")
        .style("-ms-user-select", "none")
        .style("user-select", "none")
        .style("cursor", "default")
        .style("font-family", "Impact")
        .style("fill", function(d, i) {
            return fill(i);
        })
        .attr("text-anchor", "middle")
        .attr("transform", function(d) {
            return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
        })
        .text(function(d) {
            return d.text;
        });
}

// set the viewbox to content bounding box (zooming in on the content, effectively trimming whitespace)

var svg = document.getElementsByTagName("svg")[0];
var bbox = svg.getBBox();
var viewBox = [bbox.x, bbox.y, bbox.width, bbox.height].join(" ");
svg.setAttribute("viewBox", viewBox);