var page_browse = app_page_prefix + '/browse';
var page_silencer_details_by_id = app_page_prefix + '/silencer_details/';
var api_get_samples_silencers = app_api_data_v1_0_prefix + '/get_sample_silencers';


$(function () {
    var vm = Vue.createApp({
        // 更改换分隔符，解决和模板语法的冲突
        // Vue3.1版本更换为了compilerOptions.delimiters
        compilerOptions: {
            delimiters: ['${', '}'],
            comments: true
        },
        data() {
            return {
                allSilencersCount: allSilencersCount,
                chosenCount: 0,
                sourcesSilencersCount: sourcesSilencersCount,
                sourcesChosen: [],
                speciesSilencersCount: speciesSilencersCount,
                speciesChosen: [],
                bioSampleTypesSilencersCount: bioSampleTypesSilencersCount,
                bioSampleTypesChosen: [],
                // tissueTypeSelect: null,
                // tissueTypesSelectData: tissueTypesSelectData,
                // tissueTypesChosen: [],
                bioSampleNameSelect: null,
                bioSampleNamesSelectData: bioSampleNamesSelectData,
                bioSamplesNamesChosen: [],
                samplesSilencersTable: null,
                searching: false,
            }
        },
        computed: {
            bioSampleNameChosenSpan() {
                return this.chosenCount + ' / ' + this.allSilencersCount;
            },
            chosenData() {
                return {
                    'sourcesChosen': this.sourcesChosen || [],
                    'speciesChosen': this.speciesChosen || [],
                    'bioSampleTypesChosen': this.bioSampleTypesChosen || [],
                    // 'tissueTypesChosen': this.tissueTypesChosen || [],
                    // 'csrfmiddlewaretoken':csrf_token,
                };
            },
        },
        watch: {},
        methods: {
            getSelectDataCount(list) {
                if (list) {
                    var count = 0;
                    list.forEach(function (item) {
                        count += Number(item.split(':')[1]);
                    });
                    return count;
                } else return 0;
            },
            getSelectDataValue(list) {
                return list.map(function (item) {
                    return item.split(':')[0];
                });
            },
            startSearching(){
                console.log('startSearching');
                this.searching = true;
                let elements=document.querySelectorAll('.list-group .list-group-item');
                elements.forEach(function(item){
                    item.classList.add('disabled');
                });
                this.bioSampleNameSelect.attr('disabled', true);
            },
            endSearching(){
                console.log('endSearching');
                this.searching = false;
                let elements=document.querySelectorAll('.list-group .list-group-item');
                elements.forEach(function(item){
                    item.classList.remove('disabled');
                });
                this.bioSampleNameSelect.attr('disabled', false);
            },
            // initTissueTypeSelect(selects) {
            //     const vueThis = this;
            //     vueThis.tissueTypeSelect = $("#tissueTypeSelect");
            //     vueThis.tissueTypeSelect.html('');
            //     vueThis.bioSampleNameSelect = vueThis.tissueTypeSelect.mySelect({
            //         multi: true, //true为多选,false为单选
            //         selects: selects,
            //         onChange: function (res) { //选择框值变化返回结果
            //             vueThis.tissueTypesChosen = vueThis.getSelectDataValue(res);
            //             debounce(vueThis.onChosen(true), 500);
            //             debounce(vueThis.initSamplesSilencersTable(), 500);
            //         }
            //     });
            // },
            initBioSampleNameSelect(selects) {
                const vueThis = this;
                vueThis.bioSampleNameSelect=$("#bioSampleNameSelect");
                vueThis.bioSampleNameSelect.html('');
                vueThis.bioSampleNameSelect.mySelect({
                    multi: true, //true为多选,false为单选
                    selects: selects,
                    onChange: function (res) {
                        //选择框值变化返回结果
                        console.log(res)
                        vueThis.chosenCount = vueThis.getSelectDataCount(res);
                        vueThis.bioSamplesNamesChosen = vueThis.getSelectDataValue(res);
                        // console.log(res);
                        if (!this.searching) {
                            vueThis.startSearching();
                            debounce(vueThis.initSamplesSilencersTable(true), 500);
                        }
                    }
                });
            },
            onChooseClick(event) {
                const el = $(event.target);
                if (el.hasClass('active')) {
                    el.removeClass('active');
                } else {
                    el.addClass('active');
                }
                if (!this.searching) {
                    this.startSearching();
                    debounce(this.onChosen(false), 500);
                    debounce(this.initSamplesSilencersTable(), 500);
                }
            },
            onChosen(notRefreshBioSampleType) {
                // 因为和JQuery一起用了，要保留一下this
                const vueThis = this;
                let sourcesChosen = $.map($("#source .active"), function (item) {
                    return $(item).attr('id');
                });
                let speciesChosen = $.map($('#species .active'), function (item) {
                    return $(item).attr('id');
                });
                let bioSampleTypesChosen = $.map($('#bioSampleType .active'), function (item) {
                    return $(item).attr('id');
                });
                vueThis.sourcesChosen = sourcesChosen;
                vueThis.speciesChosen = speciesChosen;
                vueThis.bioSampleTypesChosen = bioSampleTypesChosen;
                $.ajax({
                    url: page_browse,
                    type: 'POST',
                    data: JSON.stringify(vueThis.chosenData),
                    contentType: "application/json;charset=utf-8",
                    dataType: 'json',
                    success: function (result, status) {
                        if (result.success) {
                            if (notRefreshBioSampleType) {
                                vueThis.bioSampleNamesSelectData = result.data.bioSampleNamesSelectData;
                                vueThis.initBioSampleNameSelect(result.data.bioSampleNamesSelectData);
                            } else {
                                console.log(result.data);
                                vueThis.allSilencersCount = result.data.allSilencersCount;
                                vueThis.sourcesSilencersCount = result.data.sourcesSilencersCount;
                                vueThis.speciesSilencersCount = result.data.speciesSilencersCount;
                                vueThis.bioSampleTypesSilencersCount = result.data.bioSampleTypesSilencersCount;
                                // vueThis.tissueTypesSelectData = result.data.tissue_types_select_data;
                                // vueThis.initTissueTypeSelect(result.data.tissue_types_select_data);
                                vueThis.bioSampleNamesSelectData = result.data.bioSampleNamesSelectData;
                                vueThis.initBioSampleNameSelect(result.data.bioSampleNamesSelectData);
                            }
                        }
                    },
                    error: function (res, status) {
                        console.log(res);
                    },complete:function (res){
                        vueThis.endSearching();
                    }
                });
            },
            initSamplesSilencersTable(controlSearch=false) {
                let config={
                    dom: '#samplesSilencersTable',
                    columns: [
                        {
                            'field': 'silencer_id',
                            'title': 'Silencer ID',
                            formatter: function (value, row) {
                                return '<a href="' + page_silencer_details_by_id + row.id + '" target="_blank">' + value + '</a>';
                            },
                        },
                        {
                            'field': 'loci',
                            'title': 'Loci',
                        },
                        {
                            'field': 'species',
                            'title': 'Species'
                        },
                        {
                            'field': 'bio_sample_type',
                            'title': 'BioSample Type',
                        },
                        // {
                        //     'field': 'tissue_cell_type',
                        //     'title': 'Tissue/Cell line Type',
                        // },
                        {
                            'field': 'bio_sample_name',
                            'title': 'BioSample Name',
                        },
                        {
                            'field': 'recognition_factors',
                            'title': 'Recognition Factors',
                        }
                    ],
                    url: api_get_samples_silencers,
                    uploadData: Object.assign({'bioSamplesNamesChosen': this.bioSamplesNamesChosen || [],}, this.chosenData,),

                };
                if (controlSearch) config.completeCallBack= this.endSearching;
                this.samplesSilencersTable = initBootstrapTable(config);
            }
        },
        mounted() {
            // this.initTissueTypeSelect(this.tissueTypesSelectData);
            this.initBioSampleNameSelect(this.bioSampleNamesSelectData);
            this.initSamplesSilencersTable();
            endLoading();
        }
    }).mount('#side');
});