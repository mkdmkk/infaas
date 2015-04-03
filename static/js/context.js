(function ($) {
    function ContextVisualizer($chart) {
        // Resize the chart to fit its parent
        $chart.attr('width', $chart.parent().width()-2);
        $chart.attr('height', $chart.parent().height()-2);

        // Get 2d chart
        var chart = new Chart($chart.get(0).getContext("2d"));
        var lineChart;

        // Public attributes and methods
        var self = {
            plot: function (data) {
                options = {
                    scaleShowGridLines: true,
                    scaleGridLineColor: "rgba(0,0,0,.05)",
                    scaleGridLineWidth: 1,
                    bezierCurve: false,
                    pointDot: false,
                    pointDotStrokeWidth: 1,
                    pointHitDetectionRadius: 20,
                    datasetStroke: true,
                    datasetStrokeWidth: 2,
                    datasetFill: false,
                    legendTemplate: "<ul class=\"<%=name.toLowerCase()%>-legend\"><% for (var i=0; i<datasets.length; i++){%><li><span style=\"background-color:<%=datasets[i].lineColor%>\"></span><%if(datasets[i].label){%><%=datasets[i].label%><%}%></li><%}%></ul>",
                    animation: false
                };
                lineChart = chart.Line(data, options);
            }
        };
        return self;
    }

    var contextVisualizer = new ContextVisualizer($("#chart-curr-context"));

    $("#bt-query").click(function() {
        $.get("http://localhost:8000/api/context", packContextQuery(), function(res) {
            //contextVisualizer.plot(data);
            alert(res);
        });
    });

    function packContextQuery() {
        var contextQuery = {};
//        contextQuery["source"] = $("#in-source").val();
//        contextQuery["type"] = $("#in-type").val();
        contextQuery["time"] = {"$gte":$("#in-from").val(),"$lte":$("#in-to").val()}
        return {"query":JSON.stringify(contextQuery),"limit":$("#in-maxctxnum").val()};
    }

    function decodeContext() {

    }
})(jQuery);