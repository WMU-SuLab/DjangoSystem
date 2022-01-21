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
                allCount: allSilencersCount,
                chosenCount: 0,
                sourcesSilencersCount: sourcesSilencersCount,
                sourcesChosen: [],
                speciesSilencersCount: speciesSilencersCount,
                speciesChosen: [],
                bioSampleTypesSilencersCount: bioSampleTypesSilencersCount,
                bioSampleTypesChosen: [],
                tissueTypeSelect: null,
                tissueTypesSelectData: tissueTypesSelectData,
                tissueTypesChosen: [],
                bioSampleNameSelect: null,
                bioSampleNamesSelectData: bioSampleNamesSelectData,
                bioSamplesNamesChosen: [],
                samplesSilencersTable: null,
            }
        },
        computed: {
            bioSampleNameChosenSpan() {
                return this.chosenCount + ' / ' + this.allCount;
            },
            chosenData() {
                return {
                    'sourcesChosen': this.sourcesChosen || [],
                    'speciesChosen': this.speciesChosen || [],
                    'bioSampleTypesChosen': this.bioSampleTypesChosen || [],
                    'tissueTypesChosen': this.tissueTypesChosen || [],
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
            initTissueTypeSelect(selects) {
                const vueThis = this;
                vueThis.tissueTypeSelect = $("#tissueTypeSelect");
                vueThis.tissueTypeSelect.html('');
                vueThis.bioSampleNameSelect = vueThis.tissueTypeSelect.mySelect({
                    multi: true, //true为多选,false为单选
                    selects: selects,
                    onChange: function (res) { //选择框值变化返回结果
                        vueThis.tissueTypesChosen = vueThis.getSelectDataValue(res);
                        debounce(vueThis.onChosen(true), 500);
                        debounce(vueThis.initSamplesSilencersTable(), 500);
                    }
                });
            },
            initBioSampleNameSelect(selects) {
                const vueThis = this;
                vueThis.bioSampleNameSelect = $("#bioSampleNameSelect");
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
                        debounce(vueThis.initSamplesSilencersTable(), 500);
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
                debounce(this.onChosen(), 500);
                debounce(this.initSamplesSilencersTable(), 500);
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
                                vueThis.bioSampleNamesSelectData = result.data.bio_sample_names_select_data;
                                vueThis.initBioSampleNameSelect(result.data.bio_sample_names_select_data);
                            } else {
                                vueThis.allCount = result.data.all_silencers_count;
                                vueThis.sourcesSilencersCount = result.data.sources_chosen_silencers_count;
                                vueThis.speciesSilencersCount = result.data.species_chosen_silencers_count;
                                vueThis.bioSampleTypesSilencersCount = result.data.bio_sample_types_chosen_silencers_count;
                                vueThis.tissueTypesSelectData = result.data.tissue_types_select_data;
                                vueThis.initTissueTypeSelect(result.data.tissue_types_select_data);
                                vueThis.bioSampleNamesSelectData = result.data.bio_sample_names_select_data;
                                vueThis.initBioSampleNameSelect(result.data.bio_sample_names_select_data);
                            }

                        }
                    },
                    error: function (result, status) {
                        console.log(result);
                    }
                });
            },
            initSamplesSilencersTable() {
                this.samplesSilencersTable = initBootstrapTable({
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
                        {
                            'field': 'tissue_cell_type',
                            'title': 'Tissue/Cell line Type',
                        },
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
                });
            }
        },
        mounted() {
            this.initTissueTypeSelect(this.tissueTypesSelectData);
            this.initBioSampleNameSelect(this.bioSampleNamesSelectData);
            this.initSamplesSilencersTable();
            endLoading();
        }
    }).mount('#side');
});