var api_get_silencer_by_id = app_api_data_v1_0_prefix + '/get_silencer_by_id/'


let signalInThisBioSample;
let signalInOtherBioSamples;

function initSignalInSpecificBioSamplesTables(tablesData) {
    var tableCommonColumns = [
        {
            'field': 'bio_sample_name',
            'title': 'Bio Sample Name',
        }, {
            'field': 'h3k27me3',
            'title': 'H3K27me3 Z-score',
        }, {
            'field': 'h3k9me1',
            'title': 'H3K9me1 Z-score',
        }, {
            'field': 'h3k9me2',
            'title': 'H3K9me2 Z-score',
        }, {
            'field': 'h3k9me3',
            'title': 'H3K9me3 Z-score',
        },
        // {
        //     'field': 'h3k79me3',
        //     'title': 'H3K79me3 Z-score'
        // }, {
        //     'field': 'h4k20me1',
        //     'title': 'H4K20me1 Z-score'
        // },
        {
            'field': 'recognition_factors',
            'title': 'Recognition Factors'
        }
    ];
    signalInThisBioSample = initBootstrapTable({
        dom: '#signalInThisBioSample',
        columns: tableCommonColumns,
        data: tablesData.signal_in_this_bio_sample,
    });
    signalInOtherBioSamples = initBootstrapTable({
        dom: '#signalInOtherBioSamples',
        columns: tableCommonColumns,
        data: tablesData.signal_in_other_bio_samples,
    });
}

let putativeTargetGenesTable;

function initPutativeTargetGenesTable(data) {
    putativeTargetGenesTable = initBootstrapTable({
        dom: '#putativeTargetGenesTable',
        columns: [
            {
                'field': 'strategies_algorithm',
                'title': 'Strategies/Algorithm',
            }, {
                'field': 'gene_name',
                'title': 'Gene Symbol',
            }, {
                'field': 'gene_ensembl_id',
                'title': 'Ensembl',
            }, {
                'field': 'genomic_loci',
                'title': 'Genomic Loci',
            }, {
                'field': 'distance_to_TSS',
                'title': 'Distance To TSS',
            }
        ],
        data: data
    });
}

var putativeTargetGenesNetwork

function initPutativeTargetGenesNetwork(networkData) {
    $("#putativeTargetGenesNetwork").width($("#silencerTab").outerWidth());
    putativeTargetGenesNetwork = echarts.init(document.getElementById('putativeTargetGenesNetwork'), null, {
        height: "500",
        width: 'auto',
    });
    var options = {
        title: {
            text: 'Putative Target Genes Network',
            // subtext: '',
            top: 'top',
            left: 'center'
        },
        tooltip: {},
        legend: [
            {
                // selectedMode: 'single',
                data: networkData.categories.map(function (item) {
                    return item.name;
                }),
                top: 'bottom'
            }
        ],
        series: [
            {
                name: 'Putative Target Genes Network',
                type: 'graph',
                layout: 'force',
                draggable: true,
                roam: true,
                legendHoverLink: true,
                hoverAnimation: true,
                nodeScaleRatio: 0.6,
                symbolSize: 20,
                data: networkData.nodes,
                links: networkData.links,
                categories: networkData.categories,
                label: {
                    show: true,
                    position: 'right',
                    formatter: '{b}'
                },
                labelLayout: {
                    show: true,
                    hideOverlap: true
                },
                force: {
                    repulsion: 500,
                    edgeLength: 100,
                    gravity: 0.1,
                    animationDuration: 0.2,
                    animationDurationUpdate: 0.2,
                    layoutAnimation: true
                },
                lineStyle: {
                    color: 'source',
                    curveness: 0.3
                },
            }
        ]
    };
    putativeTargetGenesNetwork.setOption(options);
}

function initPutativeTargetGenes(tableData, networkData) {
    initPutativeTargetGenesTable(tableData);
    initPutativeTargetGenesNetwork(networkData);
}

function toggleAssociatedGeneExpressionIcons() {
    const AssociatedGeneExpressionIcons = $(".AssociatedGeneExpressionCollapseButton");
    AssociatedGeneExpressionIcons.each(function (index, element) {
        let count = 0;
        $(element).on('click', function () {
            count++;
            if (count % 2 === 1) {
                $(this).children('i').removeClass('fa-plus-square').addClass('fa-minus-square');
            } else {
                $(this).children('i').removeClass('fa-minus-square').addClass('fa-plus-square');
            }
        });
    });
}

const AssociatedGeneExpression = {
    template:
        `<div class="d-flex flex-column">
    <div class="py-3">
        <div class="py-4">
            <button class="btn btn-outline-secondary AssociatedGeneExpressionCollapseButton" type="button" data-bs-toggle="collapse"
                    :data-bs-target="'#bulk_collapse_'+geneName">
                    <i class="far fa-plus-square"></i>
                Bulk tissue gene expression for {{ geneName }}
            </button>
        </div>
        <div class="collapse" :id="'bulk_collapse_'+geneName">
            <div class="card card-body">
                <div class="d-flex flex-column">
                    <h5>Data Source: GTEx Analysis Release V8 (dbGaP Accession phs000424.v8.p2)</h5>
                    <h5>Data processing and normalization</h5>
                </div>
                <div class="d-flex justify-content-between border-bottom border-top border-secondary">
                    <div class="d-flex flex-row align-items-center py-3">
                        <span class="me-2 fs-5">SCALE</span>
                        <div class="btn-group" role="group">
                            <input type="radio" class="btn-check" :name="'scale_'+geneName" :id="'linear_'+geneName"
                                   autocomplete="off" checked>
                            <label class="btn btn-outline-secondary" :for="'linear_'+geneName" @click="changeToLinear()">Linear</label>
                            <input type="radio" class="btn-check" :name="'scale_'+geneName" :id="'lasso_'+geneName"
                                   autocomplete="off">
                            <label class="btn btn-outline-secondary" :for="'lasso_'+geneName" @click="changeToLasso()">Lasso</label>
                        </div>
                    </div>
                    <div class="d-flex flex-row align-items-center py-3">
                        <span class="me-2 fs-5">Tissue Sort</span>
                        <div class="btn-group" role="group">
                            <input type="radio" class="btn-check" :name="'tissueSort_'+geneName" :id="'tissue_sort_asc_'+geneName"
                                   autocomplete="off">
                            <label class="btn btn-outline-secondary" :for="'tissue_sort_asc_'+geneName" @click="tissueSortAsc()">ASC</label>

                            <input type="radio" class="btn-check" :name="'tissueSort_'+geneName"  :id="'tissue_sort_desc_'+geneName"
                                   autocomplete="off">
                            <label class="btn btn-outline-secondary" :for="'tissue_sort_desc_'+geneName" @click="tissueSortDesc()">DESC</label>
                        </div>
                    </div>
                    <div class="d-flex flex-row align-items-center py-3">
                        <span class="me-2 fs-5">Median Sort</span>
                        <div class="btn-group" role="group">
                            <input type="radio" class="btn-check" :name="'medianSort_'+geneName" :id="'median_sort_asc_'+geneName"
                                   autocomplete="off">
                            <label class="btn btn-outline-secondary" :for="'median_sort_asc_'+geneName" @click="medianSortAsc()">ASC</label>

                            <input type="radio" class="btn-check" :name="'medianSort_'+geneName" :id="'median_sort_desc_'+geneName"
                                   autocomplete="off">
                            <label class="btn btn-outline-secondary" :for="'median_sort_desc_'+geneName" @click="medianSortDesc()">DESC</label>
                        </div>
                    </div>
                </div>
                <div :id="'bulk_gene_expression_'+geneName" class="echarts"></div>
            </div>
        </div>
    </div>
    <!--<div class="py-3">
        <div class="py-4">
            <button class="btn btn-outline-secondary AssociatedGeneExpressionCollapseButton" type="button" data-bs-toggle="collapse"
                    :data-bs-target="'#single_collapse_'+geneName">
                <i class="far fa-plus-square"></i> 
                Single tissue gene expression for {{ geneName }}
            </button>
        </div>
        <div class="collapse" :id="'single_collapse_'+geneName">
            <div class="card card-body d-flex flex-column">
                <div class="d-flex flex-column">
                    <h5>Data Source: Single cell snRNA-seq pilot</h5>
                </div>
                <div class="d-flex justify-content-between">
                    <div class="btn-group" role="group" aria-label="Basic radio toggle button group">
                    </div>
                </div>
                <div :id="'single_gene_expression_'+geneName" class="echarts"></div>
            </div>
        </div>
    </div>-->
</div>`,
    props: {
        'geneName': {
            type: String,
            default: ''
        },
        'bulkData': {
            type: Object,
            default: {
                'source': [],
                'names': []
            }
        },
        /*'singleData': {
            type: Object,
            default: {
                'source': [],
                'names': []
            }
        }*/
    },
    data() {
        return {
            bulkChart: null,
            bulkDataMethod: 'linear',
            // singleChart: null,

        }
    },
    computed: {
        bulkChartOptions() {
            const bulkData = this.bulkData;
            return {
                title: [
                    {
                        text: 'Bulk tissue gene expression for ' + this.geneName,
                        left: 'center'
                    },
                ],
                dataset: [
                    {
                        source: this.bulkData.source
                    }, {
                        transform: {
                            type: 'boxplot',
                            config: {
                                itemNameFormatter: function (params) {
                                    return bulkData.names[params.value]
                                }
                            }
                        }
                    },
                    {
                        fromDatasetIndex: 1,
                        fromTransformResult: 1
                    }
                ], tooltip: {
                    trigger: 'item',
                    axisPointer: {
                        type: 'shadow'
                    }
                },
                grid: {
                    left: '5%',
                    right: '5%',
                    bottom: '35%'
                },
                xAxis: {
                    type: 'category',
                    boundaryGap: true,
                    nameGap: 30,
                    splitArea: {
                        show: false
                    },
                    splitLine: {
                        show: false
                    },
                    axisLabel: {
                        interval: 0,
                        rotate: 300
                    },
                },
                yAxis: {
                    type: 'value',
                    splitArea: {
                        show: true
                    }
                },
                series: [
                    {
                        name: 'boxplot',
                        type: 'boxplot',
                        datasetIndex: 1
                    },
                    {
                        name: 'outlier',
                        type: 'scatter',
                        datasetIndex: 2
                    }
                ]
            }
        },
        /*singleChartOptions() {
            const singleData = this.singleData;
            return {
                title: [
                    {
                        text: 'Bulk tissue gene expression for ' + this.geneName,
                        left: 'center'
                    },
                ],
                dataset: [
                    {
                        source: singleData.source
                    }, {
                        transform: {
                            type: 'boxplot',
                            config: {
                                itemNameFormatter: function (index) {
                                    return singleData.names[index]
                                }
                            }
                        }
                    },
                    {
                        fromDatasetIndex: 1,
                        fromTransformResult: 1
                    }
                ], tooltip: {
                    trigger: 'item',
                    axisPointer: {
                        type: 'shadow'
                    }
                },
                grid: {
                    left: '10%',
                    right: '10%',
                    bottom: '15%'
                },
                xAxis: {
                    type: 'category',
                    boundaryGap: true,
                    nameGap: 30,
                    splitArea: {
                        show: false
                    },
                    splitLine: {
                        show: false
                    }
                },
                yAxis: {
                    type: 'value',
                    splitArea: {
                        show: true
                    }
                },
                series: [
                    {
                        name: 'boxplot',
                        type: 'boxplot',
                        datasetIndex: 1
                    },
                    {
                        name: 'outlier',
                        type: 'scatter',
                        datasetIndex: 2
                    }
                ]
            }
        }*/
    },
    methods: {
        changeToLasso() {
            if (this.bulkDataMethod !== 'lasso') {
                this.bulkDataMethod = 'lasso';
                var newSource = [];
                this.bulkData.source = this.bulkData.source.map(function (arr) {
                    var newArr = [];
                    arr.forEach(function (item) {
                        if (item <= 0.0001) newArr.push(item);
                        else newArr.push(Math.log2(item));
                    })
                    newSource.push(newArr);
                    return newArr;
                });
                this.bulkData.source = newSource;
                this.bulkChart.clear();
                this.bulkChart.setOption(this.bulkChartOptions);
            }
        },
        changeToLinear() {
            if (this.bulkDataMethod !== 'linear') {
                this.bulkDataMethod = 'linear';
                var newSource = []
                this.bulkData.source = this.bulkData.source.map(function (arr) {
                    var newArr = [];
                    arr.forEach(function (item) {
                        newArr.push(Math.pow(2, item));
                    });
                    newSource.push(newArr);
                    return newArr;
                });
                this.bulkData.source = newSource;
                this.bulkChart.clear();
                this.bulkChart.setOption(this.bulkChartOptions);
            }
        },
        tissueSortAsc() {
            arraySortedIndex(this.bulkData.names, 'asc');
            var namesIndex = this.bulkData.names.sortedIndex;
            var newSource = [];
            namesIndex.forEach((item) => {
                newSource.push(this.bulkData.source[item])
            })
            this.bulkData.source = newSource;
            this.bulkChart.setOption(this.bulkChartOptions);
        },
        tissueSortDesc() {
            arraySortedIndex(this.bulkData.names, 'desc');
            var namesIndex = this.bulkData.names.sortedIndex;
            var newSource = [];
            namesIndex.forEach((item) => {
                newSource.push(this.bulkData.source[item])
            })
            this.bulkData.source = newSource;
            this.bulkChart.setOption(this.bulkChartOptions);
        },
        medianSortAsc() {
            var averageSource = arrayAverageSort(this.bulkData.source, 'asc');
            var sourceIndex = averageSource.sortedIndex;
            var newSource = [];
            var newNames = [];
            sourceIndex.forEach((item) => {
                newSource.push(this.bulkData.source[item]);
                newNames.push(this.bulkData.names[item]);
            })
            this.bulkData.names = newNames;
            this.bulkData.source = newSource;
            this.bulkChart.setOption(this.bulkChartOptions);
        },
        medianSortDesc() {
            var averageSource = arrayAverageSort(this.bulkData.source, 'desc');
            var sourceIndex = averageSource.sortedIndex;
            var newSource = [];
            var newNames = [];
            sourceIndex.forEach((item) => {
                newSource.push(this.bulkData.source[item]);
                newNames.push(this.bulkData.names[item]);
            })
            this.bulkData.names = newNames;
            this.bulkData.source = newSource;
            this.bulkChart.setOption(this.bulkChartOptions);
        },
        initEcharts() {
            this.bulkChart = echarts.init(document.getElementById('bulk_gene_expression_' + this.geneName), null, {
                height: "500",
            });
            this.bulkChart.setOption(this.bulkChartOptions);
            // this.singleChart = echarts.init(document.getElementById('single_gene_expression_' + this.geneName), null, {
            //     height: "500",
            // });
            // this.singleChart.setOption(this.singleChartOptions);
            // toggleAssociatedGeneExpressionIcons();
        }
    },
    created() {
    },
    mounted() {
        var eChartsWidth = $("#SignalInSpecificBioSamples").outerWidth();
        $('#bulk_gene_expression_' + this.geneName).width(eChartsWidth);
        // $('#single_gene_expression_' + this.geneName).width(eChartsWidth);
        this.initEcharts();
    }
};

function initAssociatedGeneExpression(genes) {
    var associatedGeneExpressionEl = $("#AssociatedGeneExpression");
    associatedGeneExpressionEl.append(
        "<div v-for='item in genes'>" +
        "<associated-gene-expression " +
        ":gene-name='item.gene_name' " +
        ":bulk-data='item.bulk_data' " +
        // ":single-data='item.single_data'" +
        ">" +
        "</associated-gene-expression>" +
        "</div>")
    Vue.createApp({
        components: {
            AssociatedGeneExpression
        },
        data() {
            return {
                genes: genes
            }
        },
    }).mount('#AssociatedGeneExpression');
}

function getSilencer() {
    var pathname = window.location.pathname;
    var pathSplit = pathname.split('/');
    var silencerID = pathSplit[pathSplit.length - 1];
    $.ajax({
        url: api_get_silencer_by_id + silencerID,
        type: 'GET',
        dataType: 'json',
        success: function (res, status) {
            // console.log(res);
            endLoading();
            initSignalInSpecificBioSamplesTables(res.data.signal_in_specific_bio_samples_tables_data);
            initPutativeTargetGenes(res.data.putative_target_genes.table_data, res.data.putative_target_genes.network_data);
            initAssociatedGeneExpression(res.data.associated_gene_expressions);
        }, error: function (error) {
            console.log(error);
            endLoading();
        },
    });
}

$(function () {
    getSilencer();
});