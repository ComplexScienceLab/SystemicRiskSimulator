import igraph as ig
import json

# 创建一个igraph图
g = ig.Graph.Tree(10, 2)

# 为节点和边设置属性和标签
g.vs["label"] = [str(i) for i in range(len(g.vs))]
g.es["weight"] = [i for i in range(len(g.es))]
g.es["label"] = ["edge " + str(i) for i in range(len(g.es))]

# 将igraph图转换为JSON格式
json_data = {"nodes": [], "links": []}
for i, v in enumerate(g.vs):
    json_data["nodes"].append({"id": i, "label": v["label"]})
for e in g.es:
    json_data["links"].append({"source": e.source, "target": e.target, "weight": e["weight"], "label": e["label"]})
json_data = json.dumps(json_data)

# 使用D3.js绘制可视化图表
from IPython.core.display import HTML
HTML('''
<style>
.link {
  stroke: #ccc;
}

.node text {
  pointer-events: none;
  font: 10px sans-serif;
}

.node circle {
  stroke: #fff;
  stroke-width: 1.5px;
}
</style>
<div id="chart"></div>
<script src="https://d3js.org/d3.v6.min.js"></script>
<script>
var width = 500,
    height = 500;

var data = %s;

var nodes = data.nodes,
    links = data.links;

var simulation = d3.forceSimulation(nodes)
    .force("link", d3.forceLink(links).id(d => d.id).distance(50))
    .force("charge", d3.forceManyBody().strength(-100))
    .force("center", d3.forceCenter(width / 2, height / 2));

var svg = d3.select("#chart").append("svg")
    .attr("width", width)
    .attr("height", height);

var link = svg.selectAll(".link")
    .data(links)
    .enter().append("line")
    .attr("class", "link")
    .attr("stroke-width", d => d.weight);

var node = svg.selectAll(".node")
    .data(nodes)
    .enter().append("g")
    .attr("class", "node")
    .call(d3.drag()
        .on("start", dragstarted)
        .on("drag", dragged)
        .on("end", dragended));

node.append("circle")
    .attr("r", 10)
    .attr("fill", "#ccc");

node.append("text")
    .attr("dx", 12)
    .attr("dy", ".35em")
    .text(d => d.label);

link.append("text")
    .attr("class", "edge-label")
    .attr("dx", 12)
    .attr("dy", ".35em")
    .text(d => d.label);

simulation.on("tick", () => {
link.attr("x1", d => d.source.x)
.attr("y1", d => d.source.y)
.attr("x2", d => d.target.x)
.attr("y2", d => d.target.y);

node.attr("transform", d => translate(${d.x},${d.y}));
});

function dragstarted(event) {
if (!event.active) simulation.alphaTarget(0.3).restart();
event.subject.fx = event.subject.x;
event.subject.fy = event.subject.y;
}

function dragged(event) {
event.subject.fx = event.x;
event.subject.fy = event.y;
}

function dragended(event) {
if (!event.active) simulation.alphaTarget(0);
event.subject.fx = null;
event.subject.fy = null;
}
</script>
''' % json_data)


# 在这个示例中，我们首先创建了一个简单的树形图。然后，我们为节点和边设置了标签和属性。接下来，我们将igraph图转换为JSON格式，并使用D3.js库的力导向布局算法和节点和边的属性来绘制可视化图表。在这个例子中，我们使用了一个力导向图布局算法，因此节点和边会根据它们之间的连接关系进行布局，同时在节点和边上绘制标签。最后，我们使用IPython的`HTML`函数将可视化图表嵌入到notebook中进行显示。



