var IGV = document.querySelector("#igv");
var igvOptions = {
    genome: "hg38",
    // locus: "chr8:127,736,588-127,739,371",
    locus: "chr9:70,805,699-72,141,763",
    // "fastaURL": "https://s3.amazonaws.com/igv.broadinstitute.org/genomes/seq/hg38/hg38.fa",
    // "indexURL": "https://s3.amazonaws.com/igv.broadinstitute.org/genomes/seq/hg38/hg38.fa.fai",
    // "cytobandURL": "https://s3.amazonaws.com/igv.broadinstitute.org/annotations/hg38/cytoBandIdeo.txt",
};

function initOptions() {
    var queryArgs = getQueryArgs();
    // console.log(queryArgs);
    if (queryArgs.genome) {
        igvOptions.genome = queryArgs.genome;
    }if (queryArgs.locus){
        igvOptions.locus = queryArgs.locus;
    }
    $.ajax({
        url: getIgvReference,
        type: 'get',
        // contentType: "application/json;charset=UTF-8",
        dataType: 'json',
        success: function (res) {
            igvOptions.reference = res.reference;
        },
        error: function (err) {
            console.log(err);
        }
    });
    $.ajax({
        url: getIgvTracks,
        type: 'get',
        // contentType: "application/json;charset=UTF-8",
        dataType: 'json',
        success: function (res) {
            igvOptions.tracks = res.tracks;
        }, error: function (err) {
            console.log(err);
        }
    })
}

function initIGV() {
    initOptions();
    if (igvOptions.tracks === undefined || igvOptions.reference === undefined) {
        igv.createBrowser(IGV, igvOptions)
            .then(function (browser) {
                // igv.browser = browser;
                console.log("Created IGV browser");
            })
    } else {

    }
}


$(function () {
    initIGV();
    endLoading();
});