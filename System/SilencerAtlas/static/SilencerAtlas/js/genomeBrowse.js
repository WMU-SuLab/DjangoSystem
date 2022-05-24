function initGenomeBrowser() {
    var vm = Vue.createApp({
        compilerOptions: {
            delimiters: ['${', '}'],
            comments: true
        },
        data() {
            return {
                genomeTreeData: genomeTreeData,
                // 后端返回的格式不是el-tree需要的格式需要转换
                defaultProps: {
                    children: 'children',
                    label: 'label',
                    class:'tree-node',
                },
                IGVDom: null,
                igvOptions: {
                    genome: "hg38",
                    // locus: "chr8:127,736,588-127,739,371",
                    locus: "chr9:70,805,699-72,141,763",
                    "fastaURL": "https://s3.amazonaws.com/igv.broadinstitute.org/genomes/seq/hg38/hg38.fa",
                    "indexURL": "https://s3.amazonaws.com/igv.broadinstitute.org/genomes/seq/hg38/hg38.fa.fai",
                    // "cytobandURL": "https://s3.amazonaws.com/igv.broadinstitute.org/annotations/hg38/cytoBandIdeo.txt",
                    reference: {},
                    tracks: tracks
                },
            }
        },
        methods: {
            checkedNodesConfirm() {
                this.createIGV(this.$refs.genomeTree.getCheckedKeys());
            },
            initIGVOptions() {
                var that = this;
                var queryArgs = getQueryArgs();
                // console.log(queryArgs);
                if (queryArgs.genome) {
                    this.igvOptions.genome = queryArgs.genome;
                }
                if (queryArgs.locus) {
                    this.igvOptions.locus = queryArgs.locus;
                }
                $.ajax({
                    url: getIgvReference,
                    type: 'get',
                    // contentType: "application/json;charset=UTF-8",
                    dataType: 'json',
                    success: function (res) {
                        that.igvOptions.reference = res.reference;
                        that.generateIGV();
                    },
                    error: function (err) {
                        console.log(err);
                    }
                });
            },
            generateIGV() {
                this.IGVDom = document.querySelector("#igv");
                igv.removeAllBrowsers();
                if (this.igvOptions.tracks !== undefined && this.igvOptions.tracks.length !== 0 && this.igvOptions.reference !== undefined) {
                    igv.createBrowser(this.IGVDom, this.igvOptions)
                        .then(function (browser) {
                            // igv.browser = browser;
                            console.log("Created IGV browser");
                        })
                }
            },
            createIGV(checkedKeys) {
                var that = this;
                $.ajax({
                    url: getIgvTracks,
                    type: 'post',
                    data: JSON.stringify({'checkedKeys': checkedKeys}),
                    contentType: "application/json;charset=UTF-8",
                    dataType: 'json',
                    success: function (res) {
                        that.igvOptions.tracks = res.tracks;
                        that.generateIGV();
                    }, error: function (err) {
                        console.log(err);
                    }
                });
            }
        },
        mounted() {
            this.initIGVOptions();
        }
    });
    vm.use(ElementPlus);
    vm.mount("#genomeBrowser");
    return vm;
}

$(function () {
    initGenomeBrowser();
    endLoading();
});