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
        this.page = 1;
        if (this.mode === "server" && this.url === "") {
            console.error("url error");
            return false;
        }
        this.limit = config.limit || 20;
        this.init();
        this.onDataChange = config.onDataChange || function (value) {
            console.log(value)
        };
        return this.dom;
    }

    loading() {
        if (this.isLoading === true) return false;
        else {
            this.dom.lastChild.innerHTML = '<li class="none">searching....</li>';
            this.isLoading = true;
        }
    }

    searchLocal(value, that) {
        let options = that.config.data || [];
        that.data = options.filter((item) => {
            if (item.text.toLocaleLowerCase().includes(value) || item.value.toLocaleLowerCase().includes(value)) return item;
        });
        that.initSelects();
        that.isLoading = false;
    }

    searchServer(value, that, first=false, type = 'init') {
        let url = that.url;
        let data = {
            searchText: value,
            limit: that.limit || 20,
        };
        if (type) that.page+=1;
        data.page=that.page;
        fetch(url, {
            method: "POST",
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data),
        }).then((res) => {
            return res.json();
        }).then((res) => {
            if (type === 'init') {
                that.data = res.data.selects;
                that.page=1;
            } else if (type === 'add') {
                that.data = that.data.concat(res.data.selects);
            }
            that.more = res.data.more;
            that.onDataChange(that.data);
            that.initSelects();
            that.isLoading = false;
            if (first) that.hideSelects();
        });
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
            that.showSelects();
        });
        input.addEventListener("blur", (e) => {
            setTimeout(function () {
                that.hideSelects();
            }, 100);
        });
        let searchServerDebounce = debounce(this.searchServer, 500);
        let searchLocalDebounce = debounce(this.searchLocal, 500);
        input.addEventListener("input", (e) => {
            that.loading();
            let value = e.target.value;
            if (that.mode === "server") {
                searchServerDebounce(value, that);
            } else if (that.mode === "local") {
                searchLocalDebounce(value, that);
            }
        });
        that.input = input;
        that.dom.appendChild(input);
    }

    initSelects() {
        let that = this;
        if (that.selects) that.selects.remove();
        let selects = document.createElement("ul");
        selects.setAttribute("class", "drawer searchSelect");
        selects.style.display = "block";
        that.selects = selects;
        that.dom.appendChild(that.selects);
        const options = that.data || [];
        if (options.length === 0) {
            let none = document.createElement("li");
            none.setAttribute("class", "none");
            none.innerHTML = "no result";
            that.selects.appendChild(none);
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
            if (that.more) {
                let option = document.createElement("li");
                option.setAttribute("class", "item");
                option.innerHTML = that.limit*that.page + ' results, click to show more';
                option.addEventListener('click', (e) => {
                    that.searchServer(that.input.value, that, false, 'add');
                })
                that.selects.appendChild(option);
            }
        }
    }

    hideSelects() {
        this.selects.style.display = "none";
    }

    showSelects() {
        this.selects.style.display = "block";
    }

    init() {
        this.initInput();
        if (this.mode === 'server') {
            this.searchServer('', this, true);
        }
        this.initSelects();
        this.hideSelects();
    }
}