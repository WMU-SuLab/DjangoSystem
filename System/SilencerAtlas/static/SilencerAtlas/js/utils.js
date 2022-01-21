function debounce(func, wait, immediate) {
    let time
    let debounced = function () {
        let context = this
        if (time) clearTimeout(time)

        if (immediate) {
            let callNow = !time
            if (callNow) func.apply(context, arguments)
            time = setTimeout(
                () => {
                    time = null
                } //见注解
                , wait)
        } else {
            time = setTimeout(
                () => {
                    func.apply(context, arguments)
                }
                , wait)
        }
    }

    debounced.cancel = function () {
        clearTimeout(time)
        time = null
    }

    return debounced
}

// js对象转URL查询参数
function objTransUrlParams(obj) {
    const params = [];
    Object.keys(obj).forEach((key) => {
        let value = obj[key]
        // 如果值为undefined我们将其置空
        if (typeof value === 'undefined') {
            value = ''
        }
        // 对于需要编码的文本（比如说中文）我们要进行编码
        params.push([key, encodeURIComponent(value)].join('='))
    })
    return params.join('&')
}


// // 实现PHP的sprintf函数
// function str_repeat(i, m) {
//     for (var o = []; m > 0; o[--m] = i) ;
//     return o.join('');
// }
//
// function sprintf() {
//     var i = 0, a, f = arguments[i++], o = [], m, p, c, x, s = '';
//     while (f) {
//         if (m = /^[^\x25]+/.exec(f)) {
//             o.push(m[0]);
//         } else if (m = /^\x25{2}/.exec(f)) {
//             o.push('%');
//         } else if (m = /^\x25(?:(\d+)\$)?(\+)?(0|'[^$])?(-)?(\d+)?(?:\.(\d+))?([b-fosuxX])/.exec(f)) {
//             if (((a = arguments[m[1] || i++]) == null) || (a == undefined)) {
//                 throw('Too few arguments.');
//             }
//             if (/[^s]/.test(m[7]) && (typeof (a) != 'number')) {
//                 throw('Expecting number but found ' + typeof (a));
//             }
//             switch (m[7]) {
//                 case 'b':
//                     a = a.toString(2);
//                     break;
//                 case 'c':
//                     a = String.fromCharCode(a);
//                     break;
//                 case 'd':
//                     a = parseInt(a);
//                     break;
//                 case 'e':
//                     a = m[6] ? a.toExponential(m[6]) : a.toExponential();
//                     break;
//                 case 'f':
//                     a = m[6] ? parseFloat(a).toFixed(m[6]) : parseFloat(a);
//                     break;
//                 case 'o':
//                     a = a.toString(8);
//                     break;
//                 case 's':
//                     a = ((a = String(a)) && m[6] ? a.substring(0, m[6]) : a);
//                     break;
//                 case 'u':
//                     a = Math.abs(a);
//                     break;
//                 case 'x':
//                     a = a.toString(16);
//                     break;
//                 case 'X':
//                     a = a.toString(16).toUpperCase();
//                     break;
//             }
//             a = (/[def]/.test(m[7]) && m[2] && a >= 0 ? '+' + a : a);
//             c = m[3] ? m[3] == '0' ? '0' : m[3].charAt(1) : ' ';
//             x = m[5] - String(a).length - s.length;
//             p = m[5] ? str_repeat(c, x) : '';
//             o.push(s + (m[4] ? a + p : p + a));
//         } else {
//             throw('Huh ?!');
//         }
//         f = f.substring(m[0].length);
//     }
//     return o.join('');
// }


// 优化jQuery的序列化函数
$.fn.serializeObject = function () {
    var o = {};
    var a = this.serializeArray();
    $.each(a, function () {
        if (o[this.name]) {
            if (!o[this.name].push) {
                o[this.name] = [o[this.name]];
            }
            o[this.name].push(this.value || '');
        } else {
            o[this.name] = this.value || '';
        }
    });
    return o;
};


// 数组转置
function array_transform(arr) {
    let arr1 = [];
    let arr2 = [];
    const arr_col = arr[0].length;
    const arr_row = arr.length;
    for (let i = 0; i < arr_col; i++) {
        for (let j = 0; j < arr_row; j++) {
            if (arr[j].length != arr_col) {
                return {
                    code: false,
                    msg: "column not same"
                };
            } else {
                arr1.push(arr[j][i]);
            }
        }
        arr2.push(arr1);
        arr1 = [];
    }
    return {
        code: true,
        msg: arr2
    };
}

// 给数组中的每个字典合并另一个字典
function arrayObjAddProps(arrayObj, props) {
    return arrayObj.map(item => {
        for (let key in props) {
            item[key] = props[key];
        }
        return item
    });
}

// 字典是否为空
function isEmptyObject(obj) {
    for (const key in obj) {
        return false;
    }
    return true;
}

// 数组合并去重
function mergeArray(arr1, arr2) {
    let _arr = [];
    for (let i = 0; i < arr1.length; i++) {
        _arr.push(arr1[i]);
    }
    for (let i = 0; i < arr2.length; i++) {
        let flag = true;
        for (let j = 0; j < arr1.length; j++) {
            if (arr2[i] === arr1[j]) {
                flag = false;
                break;
            }
        }
        if (flag) {
            _arr.push(arr2[i]);
        }
    }
    return _arr;
}

// 求和
function sum(arr) {
    return arr.reduce((pre, cur) => {
        return pre + cur;
    });
}

// 平均值
function average(arr) {
    return this.sum(arr) / arr.length;
}

// 数组排序返回索引
function arraySortedIndex(array, method) {
    for (let i = 0; i < array.length; i++) {
        array[i] = [array[i], i];
    }
    if (method === 'asc') {
        array.sort(function (left, right) {
            return left[0] < right[0] ? -1 : 1;
        });
    } else if (method === 'desc') {
        array.sort(function (left, right) {
            return left[0] > right[0] ? -1 : 1;
        });
    }
    array.sortedIndex = [];
    for (let j = 0; j < array.length; j++) {
        array.sortedIndex.push(array[j][1]);
        array[j] = array[j][0];
    }
    return array;
}

// 二维数组平均值排序
function arrayAverageSort(twoDimensionArr, method) {
    var arrayAverage = [];
    twoDimensionArr.forEach((item) => {
        arrayAverage.push(average(item));
    });
    return arraySortedIndex(arrayAverage, method);
}

function getQueryArgs() {
    var qs = (location.search.length > 0 ? location.search.substr(1) : ''),
        //保存每一项
        args = {},
        //得到每一项
        items = qs.length ? qs.split('&') : [],
        item = null,
        name = null,
        value = null,
        len = items.length;

    for (var i = 0; i < len; i++) {
        item = items[i].split('=')
        name = decodeURIComponent(item[0])
        value = decodeURIComponent(item[1])
        if (name.length) {
            args[name] = value;
        }
    }
    return args;
}

function startLoading() {
    var loadingEl = document.querySelector('#loading');
    var mainContentEl = document.querySelector('#mainContent')
    loadingEl.style.display = 'block';
    mainContentEl.style.display = 'none';
}

function endLoading() {
    var loadingEl = document.querySelector('#loading');
    var mainContentEl = document.querySelector('#mainContent')
    loadingEl.style.display = 'none';
    mainContentEl.style.display = 'block';
}