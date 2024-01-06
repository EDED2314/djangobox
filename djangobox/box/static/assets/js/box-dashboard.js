document.onmousemove = handleMouseMove
document.onclick = function (event) {
    closeMenu()
}

function popitup(url) {
    newwindow = window.open(url, 'name', 'height=200,width=150');
    if (!newindow) {
        alert('We have detected that you are using popup blocking software...');
    }
    if (window.focus) { newwindow.focus() }
    return false;
}

function addBoxInLocation(id) {
    console.log('addBoxInLocation clicked')
}


function addItemInBox(id) {
    console.log('addItemInBox clicked')
}


function addBoxInBox(id) {
    console.log('addBoxInBox clicked')
}

function removeBoxfromPos(id) {
    console.log('removeBoxfromBox clicked')
}

function removePortionfromBox(id) {
    console.log('removePortionfromBox clicked')
}

function closeMenu() {
    var men = document.getElementById('rmenu')
    if (men === null) {
    } else {
        men.remove()
    }
}

function displayContextMenu(event, id, type, url) {
    event.preventDefault()
    closeMenu()
    console.log('displayContextMenu clicked')
    console.log(id, type, url)

    var rmenu = document.createElement('menu')
    rmenu.setAttribute('id', 'rmenu')
    rmenu.setAttribute('style', 'display:none;z-index:100;')

    if (type == 'Location') {
        let men1 = document.createElement('menu')
        men1.setAttribute('onclick', "addBoxInLocation('" + id + "')")
        men1.innerText += 'Add box into current location'
        rmenu.append(men1)
    } else if (type == 'Box') {
        let men1 = document.createElement('menu')
        men1.setAttribute('onclick', "addItemInBox()")
        men1.innerText += 'Add item portion into box'
        rmenu.append(men1)
        let men2 = document.createElement('menu')
        men2.setAttribute('onclick', "addBoxInBox()")
        men2.innerText += 'Add box into box'
        rmenu.append(men2)
        let men3 = document.createElement('menu')
        men3.setAttribute('onclick', "removeBoxfromPos()")
        men3.innerText += 'Remove box from current position in tree'
        rmenu.append(men3)
    } else if (type == 'Portion') {
        let men1 = document.createElement('menu')
        men1.setAttribute('onclick', 'removePortionfromBox()')
        men1.innerText += 'Remove item portion from current box'
        rmenu.append(men1)
    }

    locator = document.getElementById('menu-storage-locator')
    const location = document.getElementById('menustorage')
    location.insertBefore(rmenu, locator.nextSibling)

    rmenu.style.display = 'block'
    rmenu.style.left = document.getElementById('cords').getAttribute('x') - 10 + 'px'
    rmenu.style.top = document.getElementById('cords').getAttribute('y') - 10 + 'px'
}

function handleMouseMove(event) {
    let x = event.clientX
    let y = event.clientY
    let cords = document.getElementById('cords')
    cords.setAttribute('x', x)
    cords.setAttribute('y', y)
}

function renderTree(treeData) {
    light_color = localStorage.getItem('light_color')
    var root = d3.hierarchy(treeData)
    root.sort(function (a, b) {
        return a.data.type.toLowerCase().localeCompare(b.data.type.toLowerCase())
    })
    padding = 3
    var width = 500

    const dx = 100
    const dy = width / (root.height + padding)
    height = dy * root.height

    var levelWidth = [1]
    var childCount = function (level, n) {
        if (n.children && n.children.length > 0) {
            if (levelWidth.length <= level + 1) levelWidth.push(0)

            levelWidth[level + 1] += n.children.length
            n.children.forEach(function (d) {
                childCount(level + 1, d)
            })
        }
    }
    childCount(0, root)
    var newHeight = d3.max(levelWidth) * 50

    var svg = d3.select('#tree-container').append('svg').append('g').attr('id', 'tree-svg')

    var tree = d3.tree().size([newHeight, width])
    var treeData = tree(root)

    var stroke = '#2181ff'
    var strokeWidth = 1.5
    var strokeOpacity = 0.4

    const nodes = treeData.descendants()
    nodes.forEach(function (d) {
        d.y = d.depth * 180
    })

    const link = svg
        .append('g')
        .attr('fill', 'none')
        .attr('stroke', stroke)
        .attr('stroke-opacity', strokeOpacity)
        .attr('stroke-width', strokeWidth)
        .selectAll()
        .data(root.links())
        .join('path')
        .attr(
            'd',
            d3
                .linkHorizontal()
                .x((d) => d.y)
                .y((d) => d.x)
        )

    const node = svg
        .append('g')
        .attr('stroke-linejoin', 'round')
        .attr('stroke-width', 3)
        .selectAll()
        .data(root.descendants())
        .join('g')
        .attr('transform', (d) => `translate(${d.y},${d.x})`)

    node
        .append('circle')
        .attr('fill', (d) => (d.children ? '#555' : '#999'))
        .attr('r', 2.5)

    node
        .append('a')
        .attr('href', (d) => d.data.url)
        .attr('oncontextmenu', (d) => "displayContextMenu(event,'" + d.data.id.toString() + "','" + d.data.type.toString() + "','" + d.data.url + "')")
        .attr('class', 'tree-node-label')
        .append('text')
        .attr('dy', '0.31em')
        .attr('x', (d) => (d.children ? -6 : 6))
        .attr('text-anchor', (d) => (d.children ? 'end' : 'start'))
        .text((d) => d.data.type + ': ' + d.data.name)
        .clone(true)
        .lower()
        .attr('stroke', light_color == 'true' ? null : stroke)

    var treeSvg = document.getElementById('tree-svg')
    console.log()
    var bbox = treeSvg.getBBox()

    d3.select('#tree-container')
        .select('svg')
        .attr('width', bbox.width + 50)
        .attr('height', bbox.height + 100)
        .select('g')
        .attr('transform', 'translate(' + 300 + ',' + 0 + ')')
}

fetch('func/get_tree_data/')
    .then((response) => response.json())
    .then((data) => {
        var selectedIndex = 0
        var selectNode = document.getElementById('selectNode')
        for (var i = 0; i < data.length; i++) {
            var o = document.createElement('option')
            o.value = i
            o.text = 'Location: ' + data[i].name
            selectNode.appendChild(o)
        }

        selectNode.onchange = function () {
            selectedIndex = selectNode.selectedIndex
            const element = document.getElementById('tree-container')
            element.remove()
            var newContainer = document.createElement('div')
            newContainer.setAttribute('id', 'tree-container')
            locator = document.getElementById('tree-container-locator')
            const treeDiv = document.getElementById('tree-div')
            treeDiv.insertBefore(newContainer, locator.nextSibling)

            renderTree(data[selectedIndex])
        }

        renderTree(data[selectedIndex]) // Assuming data[0] is the root node of the tree
    })