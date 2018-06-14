define([
    'underscore',
    'backbone',
    'common',
    'app/models/activity'
], function(_, Backbone, Common, Activity) {
    'use strict';

    var ActivityCollection = Backbone.Collection.extend({
        model: Activity,
        url: function () {
            return Common.getUrl({name: 'activities'});
        }
    });

    return ActivityCollection;
});
