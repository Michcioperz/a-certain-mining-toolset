sc = $("table.result").parent("div").find("p").text();
$("table.result tbody tr").each(function(index) {
    a = $(this);
    $.get("http://127.0.0.1:5000/data/orly", {
        "orly": JSON.stringify({
            "school": sc,
            "class": a.find("td:eq(0)").text(),
            "min": a.find("td:eq(1)").text(),
            "max": a.find("td:eq(2)").text(),
            "avg": a.find("td:eq(3)").text(),
            "contest": a.find("td:eq(4)").text(),
            "prime": a.find("td:eq(5)").text(),
            "f": a.find("td:eq(6)").text(),
            "m": a.find("td:eq(7)").text()
        })
    });
});
