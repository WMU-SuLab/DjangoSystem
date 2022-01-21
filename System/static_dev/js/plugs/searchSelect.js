/*
这是一个模糊搜索组件，功能应该算比较完善，提供了目前常用的api
使用方法 new searchSelect(dom名字,模糊搜索数据的数组,回调函数:选填，传入会在input事件触发时调用)
对原插件进行了一些改造，注意如果使用在其他项目中需要改回来
*/


class searchSelect {
    constructor(dom, list, fn) {
        this.list = []
        this.dom = $(dom)
        this.params = {}
        this.loading = false
        if (list instanceof Array) {
            this.list = list
        }
        let id=$(this.dom).attr('id')
        $(this.dom).removeAttr('id')
        $(this.dom).addClass('searchSelect_box')
        let name = $(this.dom).attr('name');
        let placeholder = $(this.dom).attr('placeholder')
        $(this.dom).append('<input id="'+id+'" placeholder="' + (placeholder || '') + '" type="text" name="' + (name || '') + '" class="searchSelect" autocomplete="off">')
        $(this.dom).append('<ul class="drawer"></ul>')
        this.getList()
        let that = this
        $(this.dom).children('.searchSelect').on('input', function () {
            let val = $(that.dom).children('.searchSelect').val().trim()
            $(that.dom).children('.searchSelect').val(val)
            if (!(val === $(that.dom).children('.drawer').find('.active').text())) {
                $(that.dom).children('.searchSelect').attr('data-id', '')
                $(that.dom).children('.drawer').find('.active').removeClass('active')
                that.params = {}
            }
            fn && fn($(this).val())
            $(that.dom).children('.drawer').stop(true, true).fadeIn()
            if (!that.loading) {
                that.getList(val)
            }
            // that.list.filter((item)=>item.value.inc)

        })
        $(this.dom).children('.searchSelect').on('focus', function () {
            $(that.dom).children('.drawer').stop(true, true).fadeIn()
        })
        $(this.dom).children('.searchSelect').on('blur', function () {
            setTimeout(() => {
                // 本来插件的意思当输入框不被聚焦的时候，输入框的值非列表中的值会直接被清除，这里不清除
                // if (!($(that.dom).children('.searchSelect').attr('data-id'))) {
                //     $(that.dom).children('.searchSelect').val('')
                // }
                $(that.dom).children('.drawer').stop(true, true).fadeOut()
            }, 100)
        })
    }

    // 模糊搜索方法
    getList(str) {
        // let list = arr || JSON.parse(JSON.stringify(this.list))
        if (this.list.length < 1) {
            $(this.dom).children('.drawer').html('<li class="none">暂无其他数据</li>')
            return this
        }
        let domList = str ? this.list.filter(item => item.value.includes(str)) : JSON.parse(JSON.stringify(this.list))
        if (domList.length < 1) {
            $(this.dom).children('.drawer').html('<li class="none">暂无其他数据</li>')
            return this
        }
        let listDom = ''
        $(this.dom).children('.drawer').html('')
        domList.forEach(item => {
            let isActive = $(this.dom).children('.searchSelect').attr('data-id') === item.id
            listDom += '<li class="item ' + (isActive ? 'active' : '') + ' " data-id="' + item.id + '">' + item.value + '</li>'
            if (isActive) {
                $(this.dom).children('.searchSelect').val(item.value)
            }
        })
        $(this.dom).children('.drawer').append(listDom)
        let dom = this.dom
        let that = this
        $(this.dom).children('.drawer').children('.item').on('click', function () {
            if ($(this).hasClass('active')) return
            $(dom).children('.searchSelect').attr('data-id', $(this).attr('data-id'))
            $(dom).children('.searchSelect').val($(this).text())
            // 因为加了验证插件，所以这里手动聚焦和取消聚焦一次，触发验证函数执行，一般可以删除这两行
            $(dom).children('.searchSelect').focus();
            $(dom).children('.searchSelect').blur();
            that.params.id = $(this).attr('data-id')
            that.params.value = $(this).text()
            $(this).addClass('active').siblings().removeClass('active')
            setTimeout(() => {
                $(dom).children('.drawer').stop(true, true).fadeOut()
                that.getList($(this).text())
            }, 300)
        })
        return this
    }

    // 更新数据 传入一个数组，更新下拉框内容
    update(list) {
        if (!(list instanceof Array)) {
            console.error('请传入一个数组！')
            return this
        }
        this.list = list
        this.getList($(this.dom).children('.searchSelect').val())
        this.loading = false
        return this
    }

    // 搜索方法 ，传入true会显示搜索中的loading，一般在input的钩子中触发ajax请求模糊搜索数据可用
    search(bol) {
        bol && $(this.dom).children('.drawer').html('<li class="none">正在搜索....</li>')
        bol && (this.loading = true)
        !bol && this.getList()
        !bol && (this.loading = false)
        return this
    }

    // 清空所有内容的方法
    empty() {
        $(this.dom).children('.drawer').html('<li class="none">暂无其他数据</li>')
        $(this.dom).children('.searchSelect').val('')
        return this
    }

    isFunction(fn) {
        return Object.prototype.toString.call(fn) === '[object Function]';
    }

//  disabled选项
    disabled(bol) {
        bol && $(this.dom).children('.searchSelect').prop('disabled', true)
        !bol && $(this.dom).children('.searchSelect').prop('disabled', false)
        return this
    }

    // 你也许需要强行赋值，用它
    assignment(obj) {
        if (obj instanceof Object && obj.id) {
            for (let i = 0; i < this.list.length; i++) {
                if (this.list[i].id === obj.id) {
                    $(this.dom).children('.drawer').html('<li class="item active" data-id="' + obj.id + '">' + obj.value + '</li>')
                    $(this.dom).children('.searchSelect').val(obj.value)
                    $(this.dom).children('.searchSelect').attr('data-id', obj).id
                    return this
                }
            }
            this.list.push(obj)
            $(this.dom).children('.drawer').html('<li class="item active" data-id="' + obj.id + '">' + obj.value + '</li>')
            $(this.dom).children('.searchSelect').val(obj.value)
            $(this.dom).children('.searchSelect').attr('data-id', obj.id)
        } else if (typeof obj === 'string' || typeof obj === 'number') {
            this.list.forEach(item => {
                if (item.id === obj) {
                    $(this.dom + ' .item[data-id="' + obj + '"]').addClass('active')
                    $(this.dom).children('.searchSelect').val($(this.dom + ' .item[data-id="' + obj + '"]').text())
                    $(this.dom).children('.searchSelect').attr('data-id', obj)
                }
            })
        }
        return this
    }
}