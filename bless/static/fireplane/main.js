/**
 * Created with PyCharm.
 * User: kier
 * Date: 13-8-26
 * Time: 下午9:44
 * To change this template use File | Settings | File Templates.
 */
 //GameFunc.js 游戏的全局函数

Game.Func=(function(){
	var instance;
	function constructor() {
		return {
			adjustSizeForWindow:function () {
				//目标高宽比
				var targetRatio=cc.originalCanvasSize.height/cc.originalCanvasSize.width;
				//窗口高宽比
				var winRatio=window.innerHeight/window.innerWidth;

				//重新设置画布的大小，使画布高宽比与目标高宽比相同。
				//根据比例，设置高度或宽度与窗口大小一样
				if (winRatio<=targetRatio) {
					cc.canvas.height = window.innerHeight;
					cc.canvas.width=window.innerHeight/targetRatio;
				}else{
					cc.canvas.height = window.innerWidth*targetRatio;
					cc.canvas.width=window.innerWidth;
				}

				//缩放比例
				var xScale = cc.canvas.width / cc.originalCanvasSize.width;

				//设置垂直和水平居中
				var parentDiv = document.getElementById("Cocos2dGameContainer");
				if (parentDiv) {
					parentDiv.style.width = cc.canvas.width + "px";
					parentDiv.style.height = cc.canvas.height + "px";
					parentDiv.style.position = "absolute";
					parentDiv.style.top = "50%";
					parentDiv.style.left = "50%";
					parentDiv.style.marginLeft = (-cc.canvas.width / 2) + "px";
					parentDiv.style.marginTop = (-cc.canvas.height / 2) + "px";
				}

                if(cc.renderContextType == cc.CANVAS){
                    cc.log('canvas');
                    //重置坐标
				    cc.renderContext.translate(0, cc.canvas.height);

				    //内容缩放
				    cc.renderContext.scale(xScale, xScale);
                    cc.Director.getInstance().setContentScaleFactor(xScale);
                } else{
                    cc.log('webgl');
                }

			}
		}
	}

	return{
		getInstance:function () {
			if (!instance) {
				instance=constructor();
			};
			return instance;
		}
	}
})();

var cocos2dApp = cc.Application.extend({
    config:document['ccConfig'],
    ctor:function(scene){
        this._super();
        this.startScene = scene;
        cc.COCOS2D_DEBUG = this.config['COCOS2D_DEBUG'];
        cc.initDebugSetting();
        cc.setup(this.config['tag']);
        cc.AppController.shareAppController().didFinishLaunchingWithOptions();
        /*
        cc.Loader.getInstance().onloading = function(){

            cc.LoaderScene.getInstance().draw();
        };
        cc.Loader.getInstance().onload = function(){
            cc.AppController.shareAppController().didFinishLaunchingWithOptions();
        };
        */
    },
    applicationDidFinishLaunching:function(){
        var director = cc.Director.getInstance();
        cc.EGLView.getInstance().setDesignResolutionSize(320,480,cc.RESOLUTION_POLICY.SHOW_ALL);
        director.setDisplayStats(this.config['showFPS']);
        director.setAnimationInterval(1.0 / this.config['frameRate']);

        winSize = director.getWinSize();
        centerPos = cc.p(winSize.width / 2, winSize.height / 2);
        //director.runWithScene(new this.startScene());
        cc.LoaderScene.preload(g_resources, function(){
            director.replaceScene(new this.startScene());
        }, this);
        /*
        Game.Func.getInstance().adjustSizeForWindow();
        window.addEventListener("resize", function (event) {
            Game.Func.getInstance().adjustSizeForWindow();
        });
        */
        return true;
    }
})

var director;
var winSize;
var centerPos;
var myApp = new cocos2dApp(MainLayer.scene);
