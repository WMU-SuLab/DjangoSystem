// 可以直接调用bootstrap-table的工具函数实现PHP的sprintf函数
var sprintf = $.fn.bootstrapTable.utils.sprintf;

function initBootstrapTable({dom, columns, url = undefined,uploadData,sortPriority=[], data = undefined}) {
    var config = {
        classes: "table table-bordered table-hover table-striped",
        // 是否分页
        pagination: true,
        // server:服务器端分页|client：前端分页
        // 是否显示行间隔色
        striped: true,
        // 初始化加载第一页
        pageNumber: 1,
        // 单页记录数
        pageSize: 10,
        // 可选择单页记录数
        pageList: ['1', '5', '10', '20', '50', '100', 'all'],
        // 当前页信息
        formatShowingRows: function (pageFrom, pageTo, totalRows) {
            return sprintf('Showing %s to %s of %s rows', pageFrom, pageTo, totalRows)
        },
        // 这个选项会在没数据的时候不显示分页的一些内容，最好设置为false关了
        smartDisplay: false,
        // 添加指定页码跳转
        showJumpTo: true,
        showJumpToByPages: 1,
        // 添加搜索功能
        search: true,
        searchOnEnterKey: true,
        searchHighlight: true,
        // 添加高级搜索功能
        advancedSearch: true,
        idForm: 'silencerAdvancedForm',
        idTable: 'silencerAdvancedTable',
        formatAdvancedCloseButton: function () {
            return 'Confirm';
        },
        // 刷新按钮
        showRefresh: true,
        // 显示下拉框勾选要显示的列
        showColumns: true,
        // 显示文本形式的列
        showToggle: true,
        // 添加选择框
        clickToSelect: true,
        // 添加选择复制功能
        showCopyRows: true,
        // 添加全屏功能
        showFullscreen: true,
        // 添加混合排序功能
        showMultiSort: true,
        // 手动设置优先级
        // sortPriority: [
        //     {"sortName": "","sortOrder":"desc"},
        // ],
        sortPriority:sortPriority,
        // 添加打印功能
        showPrint: true,
        // 添加导出数据功能
        showExport: true,
        exportDataType: 'selected',
        exportTypes: ['json', 'xml', 'csv', 'txt', 'sql', 'excel', 'pdf'],
        exportOptions: {
            fileName: function () {
                return 'tableExport';
            }
        },
        // 设置查询
        // 设置为undefined参数名称为pageNumber，pageSize，searchText，sortName，sortOrder
        // 设置为limit参数名称为limit, offset, search, sort, order
        queryParamsType: '',
        queryParams: function (params) {
            // console.log(params);
            //这里的键的名字和控制器的变量名必须一直，这边改动，控制器也需要改成一样的
            const temp = Object.assign({
                pageSize: params.pageSize,//页面大小
                currentPage: params.pageNumber,//页码
                searchText: params.searchText,//搜索内容
                filters: params.filter,//按条件搜索
                orderName: params.sortName,//需要排序的列
                sortOrder: params.sortOrder,//升序或降序
                multiSort: params.multiSort,//混合排序
            }, uploadData);
            return JSON.stringify(temp);
        },
        responseHandler: function (res) {
            return res.data;
        },
        onLoadSuccess: function (res) {  //加载成功时执行
            // console.log(res);
        },
        onLoadError: function (e) {  //加载失败时执行
            console.log(e);
        },
        // 列属性
        columns: [{
            field: 'state',
            checkbox: true,
        }].concat(arrayObjAddProps(columns, {
            'align': 'center',
            'valign': 'middle',
            'sortable': true,
            searchHighlightFormatter: function (value, searchText) {
                if ($(value).is('a')) {
                    value = $(value);
                    value.html(value.text().replace(new RegExp('(' + searchText + ')', 'gim'), '<span style="background-color: greenyellow;border: 1px solid red;border-radius:90px;padding:4px">$1</span>'));
                    return value[0].outerHTML;
                } else {
                    return value.toString().replace(new RegExp('(' + searchText + ')', 'gim'), '<span style="background-color: greenyellow;border: 1px solid red;border-radius:90px;padding:4px">$1</span>')
                }
            },
        })),
    }
    if (url !== undefined) {
        config.url = url;
        config.method = "POST";
        config.sidePagination = 'server';

    } else if (data !== undefined) {
        config.sidePagination = 'client';
        // 客户端模式的时候指定数据
        config.data = data;
    }
    return $(dom).bootstrapTable('destroy').bootstrapTable(config);
}