/*
 */

function debounce(fn, wait, immediate) {
    let timer;
    return function () {
        if (timer) clearTimeout(timer);
        if (immediate) {
            // 如果已经执行过，不再执行
            let callNow = !timer;
            timer = setTimeout(() => {
                timer = null;
            }, wait);
            if (callNow) {
                fn.apply(this, arguments);
            }
        } else {
            timer = setTimeout(() => {
                fn.apply(this, arguments);
            }, wait);
        }
    };
}

class searchSelect {
    constructor(id, config) {
        this.id = id;
        this.dom = document.querySelector("#" + id);
        this.dom.removeAttribute("id");
        this.dom.setAttribute("class", "searchSelect_box");
        this.config = config;
        this.style = config.style || '';
        if (this.style) {
            this.dom.setAttribute("style", this.style);
        }
        this.class = config.class || '';
        if (this.class) {
            this.class.split(" ").forEach((className) => {
                this.dom.classList.add(className);
            })
        }
        if (config.name) {
            this.name = config.name;
        } else {
            console.error("name is required");
            return false;
        }
        this.mode = config.mode || "local";
        if (this.mode !== "server" && this.mode !== "local") {
            console.error("mode error");
            return false;
        }
        this.data = config.data || [];
        if (this.mode === "local" && this.data.length === 0) {
            console.error("data error");
            return false;
        }
        this.url = config.url || "";
        this.more = false;
        this.moreData = [];
        this.page = 1;
        if (this.mode === "server" && this.url === "") {
            console.error("url error");
            return false;
        }
        this.limit = config.limit || 20;
        this.init();
        this.onDataChange = config.onDataChange || function (value) {
            console.log(value);
        };
        this.nowSearchValue = "";
        return this.dom;
    }

    initInput() {
        let that = this;
        let input = document.createElement("input");
        input.setAttribute("id", this.id);
        input.setAttribute("type", "text");
        input.setAttribute("placeholder", this.config.placeholder || "");
        input.setAttribute("class", "searchInput form-control");
        input.setAttribute("name", that.name);
        input.setAttribute("spellcheck", "false");
        input.setAttribute("autocomplete", "off");
        input.setAttribute('data-ms-editor', 'true');
        input.addEventListener("focus", (e) => {
            if (that.isLoading) that.startLoading(); else that.showSelects();
        });
        input.addEventListener("blur", (e) => {
            if (!this.isLoading) {
                setTimeout(function () {
                    that.hideSelects();
                }, 100);
            }
        });
        let searchServerDebounce = debounce(this.searchServer, 500);
        let searchLocalDebounce = debounce(this.searchLocal, 500);
        input.addEventListener("input", (e) => {
            that.startLoading();
            that.buildSelects();
            const value = e.target.value;
            that.nowSearchValue = value;
            if (that.mode === "server") {
                searchServerDebounce(value, that);
            } else if (that.mode === "local") {
                searchLocalDebounce(value, that);
            }
        });
        that.input = input;
        that.dom.appendChild(input);
    }

    initLoading() {
        let loadingSelect = document.createElement("ul");
        loadingSelect.setAttribute("class", "drawer searchSelect");
        let loadingOption = document.createElement("li");
        loadingOption.setAttribute("class", "none");
        loadingOption.innerHTML = "searching....";
        loadingSelect.appendChild(loadingOption);
        loadingSelect.style.display = "none";
        this.isLoading = false;
        this.loadingSelect = loadingSelect;
        this.dom.appendChild(loadingSelect);
    }

    startLoading() {
        if (this.isLoading !== true) {
            this.loadingSelect.style.display = "block";
            this.selects.style.display = "none";
            this.isLoading = true;
        }
    }

    endLoading() {
        if (this.isLoading === true) {
            this.loadingSelect.style.display = "none";
            this.selects.style.display = "block";
            this.isLoading = false;
        }
    }

    searchLocal(value, that) {
        let options = that.config.data || [];
        that.data = options.filter((item) => {
            if (item.text.toLocaleLowerCase().includes(value) || item.value.toLocaleLowerCase().includes(value)) return item;
        });
        that.initSelects();
        that.endLoading();
    }

    searchServer(value, that, type = 'init') {
        let url = that.url;
        if (type === 'add') that.page += 1; else if (type === 'init') that.page = 1;
        let data = {
            searchText: value,
            limit: that.limit || 20,
            page: that.page,
        };
        fetch(url, {
            method: "POST",
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data),
        }).then((res) => {
            return res.json();
        }).then((res) => {
            if (that.nowSearchValue !== value) return;
            if (type === 'init') {
                that.data = res.data.selects
                that.more = res.data.more;
                that.appendOptions(that.data);
                that.removeSearchingOption();
            } else if (type === 'add') {
                that.data = that.data.concat(res.data.selects);
                that.moreData = res.data.selects;
                that.more = res.data.more;
                that.addSelects();
            }
            that.onDataChange(that.data);
            that.endLoading();
        });
    }

    appendSearchingOption() {
        let searchingOption = document.createElement("li");
        searchingOption.setAttribute("class", "none");
        searchingOption.innerHTML = "searching....";
        this.selects.appendChild(searchingOption);
        this.searchingOption = searchingOption;
    }

    removeSearchingOption() {
        this.searchingOption.remove();
    }

    appendNoneOption() {
        let that = this;
        let none = document.createElement("li");
        none.setAttribute("class", "none");
        none.innerHTML = "no result";
        that.selects.appendChild(none);
    }

    appendMoreOption() {
        let that = this;
        if (that.more) {
            let moreOption = document.createElement("li");
            moreOption.setAttribute("class", "item");
            moreOption.innerHTML = that.limit * that.page + ' results, loading more';
            that.moreOption = moreOption;
            that.selects.appendChild(moreOption);
        }
    }

    appendOptions(options) {
        let that = this;
        if (options.length === 0 && that.page === 1) {
            that.appendNoneOption();
        } else {
            options.forEach((item) => {
                let option = document.createElement("li");
                option.setAttribute("class", "item");
                option.setAttribute("value", item.value);
                option.setAttribute("text", item.text);
                option.innerHTML = item.text;
                option.addEventListener('click', (e) => {
                    that.input.value = e.target.getAttribute("value");
                    that.input.dispatchEvent(new Event('blur'));
                    that.hideSelects();
                });
                that.selects.appendChild(option);
            });
            that.appendMoreOption();
        }
    }

    buildSelects() {
        let that = this;
        if (that.selects) that.selects.remove();
        let selects = document.createElement("ul");
        selects.setAttribute("class", "drawer searchSelect");
        selects.style.display = "none";
        selects.addEventListener('scroll', function () {
            const viewHeight = selects.clientHeight;
            const contentHeight = selects.scrollHeight;//内容高度
            const scrollTop = selects.scrollTop;
            if (scrollTop + viewHeight - contentHeight < 2) { //到达底部100px时,加载新内容
                if (!that.isLoading && that.more) {
                    that.isLoading = true;
                    that.searchServer(that.input.value, that, 'add');
                }
            }
        });
        that.selects = selects;
        that.dom.appendChild(that.selects);
    }

    initSelects() {
        let that = this;
        that.buildSelects();
        that.hideSelects();
    }

    addSelects() {
        let that = this;
        const options = that.moreData;
        that.showSelects();
        that.moreOption.remove();
        that.appendOptions(options);
    }

    hideSelects() {
        this.selects.style.display = "none";
    }

    showSelects() {
        this.selects.style.display = "block";
    }

    init() {
        this.initInput();
        this.initLoading();
        if (this.mode === 'server') {
            this.initSelects();
            this.appendSearchingOption();
            this.searchServer('', this, 'init');
        } else if (this.mode === 'local') {
            this.initSelects();
            this.hideSelects();
        }
    }
}