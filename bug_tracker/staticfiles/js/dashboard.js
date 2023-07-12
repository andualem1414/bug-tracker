$(function () {
    // =====================================
    // Profit
    // =====================================

    const renderChartStatus = (data, limit) => {
        const cxt = document.querySelector("#chart");

        new ApexCharts(cxt, {
            series: [
                {
                    name: "Ticket Count",
                    data: data,
                },
            ],

            chart: {
                type: "bar",
                height: 345,
                offsetX: -15,
                toolbar: { show: true },
                foreColor: "#adb0bb",
                fontFamily: "inherit",
                sparkline: { enabled: false },
            },

            colors: ["#5D87FF", "#49BEFF"],

            plotOptions: {
                bar: {
                    horizontal: false,
                    columnWidth: "35%",
                    borderRadius: [6],
                    borderRadiusApplication: "end",
                    borderRadiusWhenStacked: "all",
                },
            },
            markers: { size: 0 },

            dataLabels: {
                enabled: false,
            },

            legend: {
                show: false,
            },

            grid: {
                borderColor: "rgba(0,0,0,0.1)",
                strokeDashArray: 3,
                xaxis: {
                    lines: {
                        show: false,
                    },
                },
            },

            xaxis: {
                type: "category",
                categories: [
                    "new",
                    "open",
                    "inprogress",
                    "resolved",
                    "Information required",
                ],
                labels: {
                    style: {
                        cssClass: "grey--text lighten-2--text fill-color",
                    },
                },
            },

            yaxis: {
                show: true,
                min: 0,
                max: limit,
                tickAmount: 4,
                labels: {
                    style: {
                        cssClass: "grey--text lighten-2--text fill-color",
                    },
                },
            },
            stroke: {
                show: true,
                width: 3,
                lineCap: "butt",
                colors: ["transparent"],
            },

            tooltip: { theme: "light" },

            responsive: [
                {
                    breakpoint: 600,
                    options: {
                        plotOptions: {
                            bar: {
                                borderRadius: 3,
                            },
                        },
                    },
                },
            ],
        }).render();
    };

    // =====================================
    // Breakup
    // =====================================

    const renderChartType = (labels, data) => {
        const ctx = document.querySelector("#breakup");

        new ApexCharts(ctx, {
            color: "#adb5bd",
            series: data,
            labels: labels,
            chart: {
                width: 180,
                type: "donut",
                fontFamily: "Plus Jakarta Sans', sans-serif",
                foreColor: "#adb0bb",
            },
            plotOptions: {
                pie: {
                    startAngle: 0,
                    endAngle: 360,
                    donut: {
                        size: "75%",
                    },
                },
            },
            stroke: {
                show: false,
            },

            dataLabels: {
                enabled: false,
            },

            legend: {
                show: false,
            },
            colors: ["#FA896B", "#539BFF", "#FFAE1F", "#13DEB9"],

            responsive: [
                {
                    breakpoint: 991,
                    options: {
                        chart: {
                            width: 150,
                        },
                    },
                },
            ],
            tooltip: {
                theme: "dark",
            },
        }).render();
    };

    // =====================================
    // Earning
    // =====================================

    const renderChartPriority = (data) => {
        const cxt = document.querySelector("#earning");

        new ApexCharts(cxt, {
            series: [
                {
                    data: data,
                },
            ],
            chart: {
                type: "bar",
                height: 130,
                toolbar: {
                    show: false,
                },
            },
            plotOptions: {
                bar: {
                    borderRadius: 4,
                    horizontal: true,
                },
            },
            dataLabels: {
                enabled: false,
            },

            xaxis: {
                categories: ["None", "Low", "Medium", "High"],
            },

            colors: ["#FA896B", "#539BFF", "#FFAE1F", "#13DEB9"],
        }).render();
    };

    const getChartData = () => {
        fetch("/ticket_count/")
            .then((res) => res.json())
            .then((result) => {
                console.log(result);

                type_labels = Object.keys(result.tickets_type_count);
                type_data = Object.values(result.tickets_type_count);

                status_data = Object.values(result.tickets_status_count);
                limit = result.limit;

                priority_labels = Object.keys(result.tickets_priority_count);
                priority_data = Object.values(result.tickets_priority_count);

                renderChartType(type_labels, type_data);
                renderChartStatus(status_data, limit);
                renderChartPriority(priority_data);
            });
    };

    getChartData();
});
