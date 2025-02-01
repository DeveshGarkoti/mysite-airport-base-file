document.addEventListener("DOMContentLoaded", function () {
    var toc = document.querySelector("#toc ul");  // The TOC container (ul)
    var headings = document.querySelectorAll("h2, h3");  // All h2 and h3 headings in the content
    var currentList = toc;  // Keep track of the current list (ul)

    // Dynamically build the TOC
    headings.forEach(function (heading, index) {
        // Generate a unique ID if not already present
        if (!heading.id) {
            heading.id = "heading-" + index;
        }

        // Create a list item for each heading
        var tocItem = document.createElement("li");
        var link = document.createElement("a");
        link.href = "#" + heading.id;
        link.textContent = heading.textContent;
        tocItem.appendChild(link);

        // Add h3 as nested under h2
        if (heading.tagName === "H2") {
            toc.appendChild(tocItem);
            currentList = document.createElement("ul");
            tocItem.appendChild(currentList);
        } else {
            currentList.appendChild(tocItem);
        }
    });

    // Smooth scroll and adjust position to center section
    document.querySelectorAll('#toc a').forEach(function(link) {
        link.addEventListener('click', function(event) {
            event.preventDefault();  // Prevent default scroll behavior
            
            var targetId = this.getAttribute('href').substring(1);
            var targetElement = document.getElementById(targetId);
            
            if (targetElement) {
                var targetPosition = targetElement.getBoundingClientRect().top + window.pageYOffset;
                var middleOfViewport = window.innerHeight / 4.5;
                var offset = targetPosition - middleOfViewport + (targetElement.offsetHeight / 2);
                
                window.scrollTo({
                    top: offset,
                    behavior: 'smooth'
                });
            }
        });
    });
});
