/*
插件的原option替换为selects，不然和根属性options太相似
本插件根据项目需要进行了改造，增加了计数的功能，即count部分
如果需要用在其他地方，需要重新改回来动
*/

const searchMultipleSelect = function (ele, options) {
    this.ele = ele;
    this.defaults = {
        multi: false
    };
    this.options = $.extend({}, this.defaults, options);
    this.result = [];
};
searchMultipleSelect.prototype = {
    init: function () {//初始化函数
        this.pubFunction();
        this.initOption();
        this.closeSelectEvent();
        this.addEvent();
    },
    closeSelectEvent: function () {
        const that = this;
        this.ele.find(".inputWrap").on("click", function (event) {
            event.stopPropagation();
            if ($(event.target).is(that.ele.find('.inputWrap>input'))){
                that.ele.find(".inputWrap>i").removeClass("fa-angle-down").addClass("fa-angle-up");
                that.ele.find(".mySelect-option").animate({height: "400px", opacity: "1"}, "fast", "swing")
            }else {
                if (that.ele.find(".inputWrap>i").hasClass("fa-angle-down")) {
                    that.ele.find(".inputWrap>i").removeClass("fa-angle-down").addClass("fa-angle-up");
                    that.ele.find(".mySelect-option").animate({height: "400px", opacity: "1"}, "fast", "swing")
                } else {
                    that.ele.find(".inputWrap>i").removeClass("fa-angle-up").addClass("fa-angle-down");
                    that.ele.find(".mySelect-option").animate({height: "0", opacity: "0"}, "fast", "swing")
                }
            }
        });
        $("html").on("click", function () {
            that.ele.find(".inputWrap>i").removeClass("fa-angle-up").addClass("fa-angle-down");
            that.ele.find(".mySelect-option").animate({height: "0", opacity: "0"}, "fast", "swing")
        })
    },
    pubFunction: function () {
        Array.prototype.contains = function (obj) {
            let i = this.length;
            while (i--) {
                if (this[i] === obj) {
                    return i;  // 返回的这个 i 就是元素的索引下标，
                }
            }
            return false;
        }
    },
    initOption: function () {
        const that = this;
        //初始化输入框和option
        this.ele.append('<div class="inputWrap"><ul></ul><input style="border: 0;min-height: 40px;padding-left: 10px;width: calc( 100% - 30px)" placeholder="search"><i class="fa fa-angle-down"></i></div>');
        this.ele.append('<div class="mySelect-option"></div>');
        const selects=this.options.selects;
        for (let i = 0; i < selects.length; i++) {
            this.ele.find(".mySelect-option").append(
                '<div class="justify-content-between" style="display: flex;" data-value="' + selects[i].value+':'+selects[i].count + '">' +
                '<span>' + selects[i].label + '</span>' +
                // '<i class="fas fa-check"></i>' +
                '<span class="badge bg-secondary rounded-pill">'+selects[i].count+'</span>'+
                '</div>')
        }

        this.ele.find('.inputWrap').find('input').on('input', function (event) {
            const divElements = that.ele.find(".mySelect-option").children('div');
            const inputValue = event.target.value.toLowerCase();
            for (let el of divElements) {
                el.hidden=true;
                const selectText = $($(el).children('span')[0]).text().toLowerCase();
                if (inputValue===''){
                    el.removeAttribute("hidden");
                } else if (selectText.indexOf(inputValue) !== -1) {
                    el.removeAttribute("hidden");
                }
            }
        })
    },
    addEvent: function () {
        const that = this;
        this.ele.find(".mySelect-option").find("div").on("click", function (event) {
            event.stopPropagation();
            if (that.options.multi) {
                if ($(this).hasClass("selected")) {
                    $(this).removeClass("selected");
                    that.result.splice(that.result.contains($(this).attr("data-value")), 1)
                } else {
                    $(this).addClass("selected");
                    that.result.push($(this).attr("data-value"))
                }
                that.refreshInput();
            } else {
                if ($(this).hasClass("selected")) {
                    $(this).removeClass("selected");
                    that.result = '';
                } else {
                    that.ele.find(".mySelect-option").find("div").removeClass("selected");
                    $(this).addClass("selected");
                    that.result = $(this).attr("data-value");
                    that.ele.find(".inputWrap>i").removeClass("fa-angle-up").addClass("fa-angle-down");
                    that.ele.find(".mySelect-option").animate({height: "0", opacity: "0"}, "fast", "swing")
                }
                that.refreshInput($(this).find("span").text());
            }
            that.options.onChange(that.result)
        });

    },
    inputResultRemoveEvent: function () {
        const that = this;
        this.ele.find(".inputWrap ul li i").on("click", function (event) {
            event.stopPropagation();
            that.result.splice(that.result.contains($(this).attr("data-value")), 1);
            that.refreshInput();
            that.removeOptionStyle($(this).attr("data-value"));
            that.options.onChange(that.result);

        })
    },
    removeOptionStyle: function (val) {
        this.ele.find(".mySelect-option").find("div").each(function () {
            if ($(this).attr("data-value") === val) {
                $(this).removeClass("selected")
            }
        })
    },
    refreshInput: function (label) {
        this.ele.find(".inputWrap ul").empty();
        if (this.options.multi) {
            for (let i = 0; i < this.options.selects.length; i++) {
                for (let j = 0; j < this.result.length; j++) {
                    if (this.result[j] === this.options.selects[i].value) {
                        this.ele.find(".inputWrap ul").append('<li><span>' + this.options.selects[i].label + '</span>&nbsp;&nbsp;<i data-value="' + this.options.selects[i].value + '" class="fas fa-times"></i></li>')
                    }
                }
            }
        } else {
            if (this.result === '') {
                this.ele.find(".inputWrap ul").empty()
            } else {
                this.ele.find(".inputWrap ul").append('<li><span>' + label + '</span>&nbsp;&nbsp;</li>')
            }

        }
        this.inputResultRemoveEvent();
    },
    setResult: function (res) {
        this.result = res;
        if (this.options.multi) {
            if (res instanceof Array) {
                this.refreshInput();
                this.ele.find(".mySelect-option").find("div").each(function () {
                    for (let i = 0; i < res.length; i++) {
                        if ($(this).attr("data-value") === res[i]) {
                            $(this).addClass("selected")
                        }
                    }

                })
            } else {
                alert("参数必须是数组")
            }

        } else {
            for (let i = 0; i < this.options.selects.length; i++) {
                if (this.options.selects[i].value === res) {
                    this.refreshInput(this.options.selects[i].label)
                }
            }
            this.ele.find(".mySelect-option").find("div").each(function () {
                if ($(this).attr("data-value") === res) {
                    $(this).addClass("selected")
                }
            })
        }

    },
    getResult: function () {
        return this.result;
    }
};
$.fn.mySelect = function (options) {
    const select = new searchMultipleSelect(this, options);
    select.init();
    return select;
};