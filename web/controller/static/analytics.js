$(function() {

    var renderers = $.extend(
        $.pivotUtilities.renderers,
        $.pivotUtilities.plotly_renderers);

    var utils = $.pivotUtilities;

    $.getJSON('analytics_profiles', function(profiles) {
        $("#pivot").pivotUI(
            profiles,
            {
                renderers: renderers,
                rows: ["country"],
                cols: ["age"],
                vals: ['height_cm'],
                rendererName: 'Bar chart'
            }
        );
    });
});