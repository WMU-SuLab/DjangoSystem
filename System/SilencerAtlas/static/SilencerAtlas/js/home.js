function quickSearch() {
    var searchText = $("#homeQuickSearchText").val();
    console.log(searchText);
    if (searchText !== '') {
        window.location.href = search_page_prefix + '?searchText=' + searchText;
    }
}

function initQuickSearch() {
    $("#homeQuickSearch").children().addClass('fs-3');
    // $("#homeQuickSearchSelect li").on('click', function () {
    //     var selectText = $(this).text();
    //     console.log(selectText);
    //     $("#homeQuickSearchSelected").text(selectText);
    // });
    $("#quickSearch").on('click', function () {
        quickSearch();
    });
    $("#homeQuickSearchText").on('keypress', function (e) {
        if (e.keyCode === 13) {
            quickSearch();
        }
    });
}

var TFChIPSeqStatisticsTable;

function initTFChIPSeqStatisticsTable() {
    TFChIPSeqStatisticsTable = echarts.init(document.getElementById('TFChIPSeqStatisticsTable'));
    TFChIPSeqStatisticsTable.showLoading();
    // 指定图表的配置项和数据
    var options = {
        title: {
            text: 'TF ChIP-seq Statistics in 5 DataBases',
            // subtext: ''
            top: 'top',
            left: 'center'
        },
        legend: {
            show: true,
            bottom: 0,
        },
        dataset: {
            source: [
                ['Data Source', 'Samples', 'TFs'],
                ['ENCODE', 674, 178],
                ['RoadMap', 438, 168],
                ['Cistrome', 2405, 333],
                ['CMP-Atlas', 1433, 271],
                ['GTRD', 98, 87]
            ]
        },
        xAxis: {type: 'category'},
        yAxis: {
            type: 'value',
            name: 'count',
        },
        // Declare several bar series, each will be mapped
        // to a column of dataset.source by default.
        series: [
            {
                type: 'bar',
                label: {
                    show: true,
                    rotate: 90,
                    // distance: 5,
                    formatter: '{@[1]}',
                    fontSize: 8,
                },
                emphasis: {
                    focus: 'series'
                },
            },
            {
                type: 'bar',
                label: {
                    show: true,
                    rotate: 90,
                    // distance: 5,
                    formatter: '{@[2]}',
                    fontSize: 8,
                },
                emphasis: {
                    focus: 'series'
                },
            }
        ]
    };

    TFChIPSeqStatisticsTable.hideLoading();
    // 使用刚指定的配置项和数据显示图表
    TFChIPSeqStatisticsTable.setOption(options);
}

$(function () {
    initQuickSearch();
    endLoading();
    // 由于echarts被隐藏后显示有问题，所以放到后面执行
    initTFChIPSeqStatisticsTable();
});