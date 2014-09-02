/**
 * Created by merlex on 02.09.14.
 */

var App = {
    baseUrl: '/',
    url: {
        save: '/save/',
        create: '/create/',
        load: '/json/'
    },
    currentModel:null,
    template:"<table>" +
        "<tr>" +
        "<th>id</th>" +
        "{{each(i, field) model.fields}}" +
            "<th>${field.title}</th>" +
        "{{/each}}" +
        "</tr>" +
        "{{each(key, object) objects}}" +
            "<tr>" +
            "<td><a href='#'>${object.id}</a></td>" +
            "{{each(i, field) model.fields}}" +
                "<td><a href='#' class='editable' data-name='${field.id}' data-type='"+
                "{{if field.type == 'date'}}"+
                    "date" +
                "{{else}}"+
                    "text" +
                "{{/if}}"+
                "' data-pk='${object.id}' data-url='/save/${model_name}/' data-title='Enter data'>${object[field.id]}</a></td>" +
            "{{/each}}" +
            "</tr>" +
        "{{/each}}" +
        "</table>",
    fillTable: function (model) {
        $.get(App.url.load+model,{}, function(result){
            $('#table-data').html($.tmpl( "modelTemplate", result ));
            $('.editable').editable();
            $('#content #create-model').show();
            App.currentModel = result.model_name;
        });
    },
    createModel: function (model) {
        $.post(App.url.create+model+'/',{},function(result){
            App.fillTable(model);
        });
    },
    init: function (baseUrl){
        App.baseUrl = baseUrl;

        $.template( "modelTemplate", App.template);

        /**
         * Edit event
         */
        $('#mainmenu ul li a').on('click', function(e){
            e.preventDefault();
            App.fillTable($(this).data('key'));
            return false;
        });
        /**
         *Create event
         */
        $('#content #create-model').on('click', function(e){
            e.preventDefault();
            App.createModel(App.currentModel);
            return false;
        });
    }
};
$(function(){
    var csrftoken = $.cookie('csrftoken');
    /**
     *
     * @param method
     * @returns {boolean}
     */
    function csrfSafeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    /**
     *
     */
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
    App.init(baseUrl);
});
