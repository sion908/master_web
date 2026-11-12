(function () {
    function boot() {
        var nav = document.querySelector("nav.ablock-ui");
        if (!nav) {
            return;
        }

        var headings = Array.prototype.slice.call(document.querySelectorAll(".body h2"));
        var links = [];

        headings.forEach(function (heading) {
            var section = heading.closest("section");
            var id = section && section.id ? section.id : heading.id;
            if (!id) {
                return;
            }

            var labelNode = heading.cloneNode(true);
            labelNode.querySelectorAll(".headerlink").forEach(function (node) {
                node.remove();
            });

            var link = document.createElement("a");
            link.href = "#" + id;
            link.textContent = labelNode.textContent.replace(/\s+/g, " ").trim();
            nav.appendChild(link);
            links.push({ link: link, section: section || heading });
        });

        if (!("IntersectionObserver" in window)) {
            return;
        }
        var observer = new IntersectionObserver(
            function (entries) {
                entries.forEach(function (entry) {
                    if (!entry.isIntersecting) {
                        return;
                    }
                    links.forEach(function (item) {
                        item.link.classList.remove("is-active");
                    });
                    var current = links.find(function (item) {
                        return item.section === entry.target;
                    });
                    if (current) {
                        current.link.classList.add("is-active");
                    }
                });
            },
            { rootMargin: "-30% 0px -60% 0px" }
        );
        links.forEach(function (item) {
            observer.observe(item.section);
        });
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", boot);
    } else {
        boot();
    }
})();
