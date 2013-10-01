/**
 * Created with PyCharm.
 * User: kier
 * Date: 13-9-11
 * Time: 下午10:03
 * To change this template use File | Settings | File Templates.
 */
var BackSky = cc.Sprite.extend({
    active:true,
    ctor:function () {
        this._super();
        //var pFrame = cc.SpriteFrameCache.getInstance().getSpriteFrame("11.png");
        this.initWithSpriteFrameName('bg01.jpg');
        this.setAnchorPoint(cc.p(0, 0));
    },
    destroy:function () {
        this.setVisible(false);
        this.active = false;
    }
});

BackSky.create = function () {
    var background = new BackSky();
    g_sharedGameLayer.addChild(background, -10);
    //MW.CONTAINER.BACKSKYS.push(background);
    return background;
};

BackSky.getOrCreate = function () {
    var selChild = null;
    /*
    for (var j = 0; j < MW.CONTAINER.BACKSKYS.length; j++) {
        selChild = MW.CONTAINER.BACKSKYS[j];
        if (selChild.active == false) {
            selChild.setVisible(true);
            selChild.active = true;
            return selChild;
        }
    }
    */
    selChild = BackSky.create();
    return selChild;
};


BackSky.preSet = function () {
    var background = null;
    background = BackSky.create();
    background.setVisible(false);
    background.active = false;
    /*
    for (var i = 0; i < 2; i++) {
        background = BackSky.create();
        background.setVisible(false);
        background.active = false;
    }
    */
};