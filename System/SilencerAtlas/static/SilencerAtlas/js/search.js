var page_silencer_details_by_id = app_page_prefix + '/silencer_details/';
var api_get_silencers = app_api_data_v1_0_prefix + '/get_silencers';
var api_get_tissue_types = app_api_data_v1_0_prefix + '/get_tissue_types';
var api_get_genes = app_api_data_v1_0_prefix + '/get_genes';
var api_get_snps = app_api_data_v1_0_prefix + '/get_snps';
var api_get_transcription_factors = app_api_data_v1_0_prefix + '/get_transcription_factors';


function initSelects() {
    // if (tissueTypesSelectData.length !== 0) {
    //     searchByRegionTissueTypesSearchSelect = new searchSelect('#searchByRegionFormTissueTypeSearchSelect', tissueTypesSelectData);
    //     searchByGeneTissueTypesSearchSelect = new searchSelect('#searchByGeneFormTissueTypeSearchSelect', tissueTypesSelectData);
    //     searchByTFTissueTypesSearchSelect = new searchSelect('#searchByTFFormTissueTypeSearchSelect', tissueTypesSelectData);
    //     searchBySNPTissueTypesSearchSelect = new searchSelect('#searchBySNPFormTissueTypeSearchSelect', tissueTypesSelectData);
    //     console.log('init tissue type');
    // }
    // if (genesSelectData.length !== 0) {
    //     // geneSearchSelect = new searchSelect('#searchByGeneFormGeneSearchSelect', genesSelectData);
    //     console.log('init genes');
    // }
    // if (transcriptionFactorsSelectData.length !== 0) {
    //     transcriptionFactorSearchSelect = new searchSelect('#searchByTFFormTranscriptionFactorSearchSelect', transcriptionFactorsSelectData);
    //     console.log('init transcription factors');
    // }
    // if (rsIdsSelectData.length !== 0) {
    //     rsIdSearchSelect = new searchSelect('#searchBySNPFormRsIdSearchSelect', rsIdsSelectData);
    //     console.log('init rsIds');
    // }
    searchByRegionTissueTypesSearchSelect = new searchSelect('searchByRegionFormTissueTypeSearchSelect', {
        mode: 'server',
        url: api_get_tissue_types,
        name: 'tissueType',
        placeholder:'tissue type',
        limit: 100,
        onDataChange: function (data) {
            regionTissueTypes = data.map((item) => {
                return item.value;
            });
        }
    });
    searchByGeneTissueTypesSearchSelect = new searchSelect('searchByGeneFormTissueTypeSearchSelect', {
        mode: 'server',
        url: api_get_tissue_types,
        name: 'tissueType',
        placeholder:'tissue type',
        limit: 100,
        onDataChange: function (data) {
            geneTissueTypes = data.map((item) => {
                return item.value;
            });
        }
    });
    searchBySNPTissueTypesSearchSelect = new searchSelect('searchBySNPFormTissueTypeSearchSelect', {
        mode: 'server',
        url: api_get_tissue_types,
        name: 'tissueType',
        placeholder:'tissue type',
        limit: 100,
        onDataChange: function (data) {
            SNPTissueTypes = data.map((item) => {
                return item.value;
            });
        }
    });
    searchByTFTissueTypesSearchSelect = new searchSelect('searchByTFFormTissueTypeSearchSelect', {
        mode: 'server',
        url: api_get_tissue_types,
        name: 'tissueType',
        placeholder:'tissue type',
        limit: 100,
        onDataChange: function (data) {
            TFTissueTypes = data.map((item) => {
                return item.value;
            });
        }
    });
    geneSearchSelect = new searchSelect('searchByGeneFormGeneSearchSelect', {
        mode: 'server',
        url: api_get_genes,
        name: 'gene',
        placeholder:'gene symbol',
        limit: 100,
        onDataChange: function (data) {
            genes = data.map((item) => {
                return item.value;
            });
        }
    });
    transcriptionFactorSearchSelect = new searchSelect('searchByTFFormTranscriptionFactorSearchSelect', {
        mode: 'server',
        url: api_get_transcription_factors,
        name: 'transcriptionFactor',
        placeholder:'transcription factor',
        limit: 100,
        onDataChange: function (data) {
            transcriptionFactors = data.map((item) => {
                return item.value;
            });
        }
    });
    rsIdSearchSelect = new searchSelect('searchBySNPFormRsIdSearchSelect', {
        mode: 'server',
        url: api_get_snps,
        name: 'rsId',
        placeholder:'rs_id',
        limit: 100,
        onDataChange: function (data) {
            rsIds = data.map((item) => {
                return item.value;
            });
        }
    });

    $(".form-select").addClass('fs-3');
    $(".form-control").addClass('fs-3');
    $(".formButtonGroup button").addClass('fs-3');
}

function initExamples() {
    $("#searchByRegionFormExample").on('click', function () {
        $("#searchByRegionFormSpeciesSelect option[selected='selected']").each(function () {
            $(this).removeAttr('selected');
        });
        $("#searchByRegionFormSpeciesSelect option:first").attr('selected', 'selected');
        $("#searchByRegionFormBioSampleTypeSelect option[selected='selected']").each(function () {
            $(this).removeAttr('selected');
        });
        $("#searchByRegionFormBioSampleTypeSelect option:first").attr('selected', 'selected');
        $("#searchByRegionFormTissueTypeSearchSelect").val(regionTissueTypes[0]);
        $("#searchByRegionFormRegionInput").val('chr1:5353130-5353206');
    });
    $("#searchByGeneFormExample").on('click', function () {
        $("#searchByGeneFormSpeciesSelect option[selected='selected']").each(function () {
            $(this).removeAttr('selected');
        });
        $("#searchByGeneFormSpeciesSelect option:first").attr('selected', 'selected');
        $("#searchByGeneFormBioSampleTypeSelect option[selected='selected']").each(function () {
            $(this).removeAttr('selected');
        });
        $("#searchByGeneFormBioSampleTypeSelect option:first").attr('selected', 'selected');
        $("#searchByGeneFormTissueTypeSearchSelect").val(geneTissueTypes[0]);
        $("#searchByGeneFormStrategySelect option[selected='selected']").each(function () {
            $(this).removeAttr('selected');
        });
        $("#searchByGeneFormStrategySelect option:first").attr('selected', 'selected');
        $("#searchByGeneFormGeneSymbolSearchSelect").val(genes[0]);
    });
    $("#searchByTFFormExample").on('click', function () {
        $("#searchByTFFormSpeciesSelect option[selected='selected']").each(function () {
            $(this).removeAttr('selected');
        });
        $("#searchByTFFormSpeciesSelect option:first").attr('selected', 'selected');
        $("#searchByTFFormBioSampleTypeSelect option[selected='selected']").each(function () {
            $(this).removeAttr('selected');
        });
        $("#searchByTFFormBioSampleTypeSelect option:first").attr('selected', 'selected');
        $("#searchByTFFormTissueTypeSearchSelect").val(TFTissueTypes[0]);
        $("#searchByTFFormTFSearchSelect").val(transcriptionFactors[0]);
    });
    $("#searchBySNPFormExample").on('click', function () {
        $("#searchBySNPFormSpeciesSelect option[selected='selected']").each(function () {
            $(this).removeAttr('selected');
        });
        $("#searchBySNPFormSpeciesSelect option:first").attr('selected', 'selected');
        $("#searchBySNPFormBioSampleTypeSelect option[selected='selected']").each(function () {
            $(this).removeAttr('selected');
        });
        $("#searchBySNPFormBioSampleTypeSelect option:first").attr('selected', 'selected');
        $("#searchBySNPFormTissueTypeSearchSelect").val(SNPTissueTypes[0]);
        $("#searchBySNPFormVariantSelect option[selected='selected']").each(function () {
            $(this).removeAttr('selected');
        });
        $("#searchBySNPFormVariantSelect option:first").attr('selected', 'selected');
        $("#searchBySNPFormSNPSearchSelect").val(rsIds[0]);
    });
}


$.validator.addMethod("validateRegion", function (value, element) {
    if (value) {
        const region_regex = /chr[0-9a-zA-Z]{1,3}:[0-9]*-[0-9]*/;
        return region_regex.test(value);
    } else {
        return null
    }
}, "Please input valid region!e.g. chr1:5353130-5353206!");

$.validator.addMethod('inTissueTypes', function (value, element) {
    if (value) {
        const tissueTypes = regionTissueTypes.concat(geneTissueTypes, TFTissueTypes, SNPTissueTypes);
        return tissueTypes.indexOf(value) !== -1;
    } else {
        return null
    }
}, 'Please input tissue type in within the limits!')

$.validator.addMethod('inGenes', function (value, element) {
    if (value) {
        return genes.indexOf(value) !== -1;
    } else {
        return null
    }
}, 'Please input tissue type in within the limits!')

$.validator.addMethod('inTranscriptionFactors', function (value, element) {
    if (value) {
        return transcriptionFactors.indexOf(value) !== -1;
    } else {
        return null
    }
}, 'Please input tissue type in within the limits!')

$.validator.addMethod('inRsIds', function (value, element) {
    if (value) {
        return rsIds.indexOf(value) !== -1;
    } else {
        return null
    }
}, 'Please input tissue type in within the limits!')

function initForms() {
    $("#searchByRegionForm").validate({
        rules: {
            region: {
                required: true,
                normalizer: function (value) {
                    return $.trim(value);
                },
                validateRegion: true
            },
            tissueType: {
                required: true,
                normalizer: function (value) {
                    return $.trim(value);
                },
                inTissueTypes: true,
            }
        },
        submitHandler: function (form, event) {
            formData = $(form).serializeObject();
            // getSilencers(formData);
            initTable()
            // $(form).submit()
        }
    });
    $("#searchByGeneForm").validate({
        rules: {
            tissueType: {
                required: true,
                normalizer: function (value) {
                    return $.trim(value);
                },
                inTissueTypes: true,
            },
            gene: {
                required: true,
                normalizer: function (value) {
                    return $.trim(value);
                },
                inGenes: true,
            }
        },
        submitHandler: function (form, event) {
            formData = $(form).serializeObject();
            // getSilencers(formData);
            initTable()
            // $(form).submit()
        }
    });
    $("#searchByTFForm").validate({
        rules: {
            tissueType: {
                required: true,
                normalizer: function (value) {
                    return $.trim(value);
                },
                inTissueTypes: true,
            },
            transcriptionFactor: {
                required: true,
                normalizer: function (value) {
                    return $.trim(value);
                },
                inTranscriptionFactors: true,
            }
        },
        submitHandler: function (form, event) {
            formData = $(form).serializeObject();
            // getSilencers(formData);
            initTable()
            // $(form).submit()
        }
    });
    $("#searchBySNPForm").validate({
        rules: {
            tissueType: {
                required: true,
                normalizer: function (value) {
                    return $.trim(value);
                },
                inTissueTypes: true,
            },
            rsId: {
                required: true,
                normalizer: function (value) {
                    return $.trim(value);
                },
                inRsIds: true,
            }
        },
        submitHandler: function (form, event) {
            formData = $(form).serializeObject();
            // getSilencers(formData);
            initTable()
            // $(form).submit()
        }
    });
}

// 客户端方式提交表单
// function getSilencers(formData) {
//     $.ajax({
//         url: api_get_silencers,
//         type: 'post',
//         contentType: "application/json;charset=UTF-8",
//         data: JSON.stringify(formData),
//         dataType: 'json',
//         success: function (res, status) {
//             if (res.code === 1) {
//                 tableData = res.data;
//                 silencerTable.bootstrapTable('load',tableData);
//             }
//         },
//         error: function (e) {
//             console.log(e.status);
//             console.log(e.responseText);
//         }
//     })
// }

function initTable() {
    silencerTable = initBootstrapTable({
        dom: '#silencerTable',
        columns: [
            {
                'field': 'silencer_id',
                'title': 'Silencer ID',
                formatter: function (value, row) {
                    return '<a href="' + page_silencer_details_by_id + row.id + '" target="_blank">' + value + '</a>';
                },
            },
            {
                'field': 'chromosome',
                'title': 'Chr',
            },
            {
                'field': 'start',
                'title': 'Start',
            },
            {
                'field': 'end',
                'title': 'End',
            },
            {
                'field': 'recognition_factors',
                'title': 'Recognition Factors',
            },
            {
                'field': 'eQTLs_count',
                'title': 'eQTL(count)',
            },
            {
                'field': 'risk_snps_count',
                'title': 'Risk SNPs(count)',
            },
            {
                'field': 'TFBs_count',
                'title': 'TFBs(count)',
            },
            {
                'field': 'Cas9s_count',
                'title': 'CRISPR/Cas9 target site(count)',
            },
        ],
        url: api_get_silencers,
        // 添加默认给silencer_id排序
        sortPriority: [
            {"sortName": "silencer_id", "sortOrder": "desc"},
        ],
        uploadData: formData,
    })
}

function initSearchTextResult() {
    var queryArgs = getQueryArgs();
    if (!isEmptyObject(queryArgs)) {
        var searchText = queryArgs.searchText;
        if (searchText.includes(':') && searchText.includes('-')) {
            formData = {'region': searchText};
        } else if (searchText.includes('_')) {
            $("#searchBySNP-tab").click();
            formData = {'rsId': searchText};
        } else {
            $("#searchByGene-tab").click();
            formData = {'gene': searchText};
        }
    }
    initTable();
}

$(function () {
    initSelects();
    initExamples();
    initForms();
    initSearchTextResult();
    endLoading();
});