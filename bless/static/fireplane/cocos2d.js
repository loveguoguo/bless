/**
 * Created with PyCharm.
 * User: kier
 * Date: 13-8-26
 * Time: 下午9:16
 * To change this template use File | Settings | File Templates.
 */
var Game=Game||{};
(function(){
    var d = document;
    var c = {
        menuType: 'canvas',
        COCOS2D_DEBUG:2,
        box2d:false,
        chipmunk:false,
        //showFPS:true,
        frameRate:60,
        loadExtension:true,
        renderMode:1,       //Choose of RenderMode: 0(default), 1(Canvas only), 2(WebGL only)
        tag:'gameCanvas',
        //engineDir:'../cocos2d-html5/cocos2d/',
        SingleEngineFile:'fireplane_advanced.js',
        appFiles:[
            'src/resource.js',
            'src/MainLayer.js',
            'src/GameOver.js',
            'src/background.js',
            'src/explosion.js',
            'src/GameConfig.js'
        ]
    };
    window.addEventListener('DOMContentLoaded', function(){
        var s = d.createElement('script');
        if(c.SingleEngineFile && !c.engineDir){
            s.src = c.SingleEngineFile;
        }
        else if(c.engineDir && !c.SingleEngineFile){
            s.src = c.engineDir + 'platform/jsloader.js';
        }
        else{
            alert('you must specify either the single engine file or engine directory in "cocos2d.js"');
        }

        document.ccConfig = c;
        s.id = 'cocos2d-html5';
        d.body.appendChild(s);
    });
})();
