/**
 * Created with PyCharm.
 * User: kier
 * Date: 13-8-26
 * Time: 下午9:03
 * To change this template use File | Settings | File Templates.
 */
var audioEngine = cc.AudioEngine.getInstance();
var g_gameStatus = {normal:0, pause:1, gameover:2};
var g_sharedGameLayer;
var MainLayer = cc.Layer.extend({
    _backSky:null,
    _backSkyHeight:0,
    _backSkyRe:null,
    _monstersDestroyed:0,
    _monsters:[],
    _projectiles:[],
    score: 0,
    miss_monsters: 0,
    miss_bullets:0,
    status: g_gameStatus.normal,
    overmenu: null,
    ctor:function(){
        this._super();
        cc.associateWithNative(this, cc.Layer);
        cc.SpriteFrameCache.getInstance().addSpriteFrames(s_use_plist);
        Game.CONTAINER.EXPLOSIONS = [];

    },
    /*
    init:function () {
        if (this._super()) {
            //cc.SpriteFrameCache.getInstance().addSpriteFrames(s_use_plist);

        }
    },
    */
    onEnter:function(){
        this._super();
        if('touches' in sys.capabilities){
            this.setTouchEnabled(true);
        }
        if('mouse' in sys.capabilities){
            this.setMouseEnabled(true);
        }
        var texTransparent = cc.TextureCache.getInstance().addImage(s_use);
        this._texTransparentBatch = cc.SpriteBatchNode.createWithTexture(texTransparent);
        this.addChild(this._texTransparentBatch);
        //var player = cc.Sprite.create(s_player);
        var player = cc.Sprite.createWithSpriteFrameName('11.png');
        //player.setTag(3000);
        //player.setPosition(player.getContentSize().width / 2, winSize.height / 2);
        player.setPosition(winSize.width / 2, player.getContentSize().height / 2);
        //this.addChild(player);
        this._texTransparentBatch.addChild(player, 3000, 1000);
        // score
        this.lbScore = cc.LabelTTF.create('Score: 0', "Arial", 15);
        this.lbScore.setAnchorPoint(cc.p(1, 0));
        this.addChild(this.lbScore, 1000);
        this.lbScore.setPosition(winSize.width-5, 30);
        this.lbmonsters = cc.LabelTTF.create("miss enemy: 0", "Arial", 15);
        this.lbmonsters.setAnchorPoint(cc.p(1, 0));
        this.addChild(this.lbmonsters, 1000);
        this.lbmonsters.setPosition(winSize.width-5, 15);
        this.lbbullets = cc.LabelTTF.create("miss hit: 0", "Arial", 15);
        this.lbbullets.setAnchorPoint(cc.p(1, 0));
        this.addChild(this.lbbullets, 1000);
        this.lbbullets.setPosition(winSize.width-5, 0);

        //pause btn
        var pauseItem=cc.MenuItemFont.create('帮助', this.pauseGame, this);
        pauseItem.setFontSize(20);
        this.pausemenu = cc.Menu.create(pauseItem);
        this.pausemenu.setPosition(25,20);
        this.addChild(this.pausemenu);
        //menu
        this.addMenu();
        // explosion batch node
        cc.SpriteFrameCache.getInstance().addSpriteFrames(s_explosion_plist);
        var explosionTexture = cc.TextureCache.getInstance().addImage(s_explosion);
        this._explosions = cc.SpriteBatchNode.createWithTexture(explosionTexture);
        this._explosions.setBlendFunc(gl.SRC_ALPHA, gl.ONE);
        this.addChild(this._explosions);
        Explosion.sharedExplosion();
        this.schedule(this.gameLogic,3);
        this.scheduleUpdate();
        audioEngine.playMusic(s_bgMusic, true);
        g_sharedGameLayer = this;
        BackSky.preSet();
        Explosion.preSet();
        this.initBackground();
        this.pauseGame();
    },
    initBackground:function () {
        this._backSky = BackSky.getOrCreate();
        this._backSkyHeight = this._backSky.getContentSize().height;

        //this.movingBackground();
        //this.schedule(this.movingBackground, 3);

        //this.moveTileMap();
        //this.schedule(this.moveTileMap, 5);
    },
    addMenu:function(){
        this.menulayer=cc.LayerColor.create(cc.c4(10,30,20,150),winSize.width / 2, winSize.height / 2);
        this.menulayer.setPosition(cc.p(winSize.width / 4, winSize.height / 4));
        //this.menulayer.setAnchorPoint(cc.p(0.5, 0.5));
        //startmenu
        /*
        var startLabel = cc.LabelBMFont.create("start", s_arial14_fnt);
        var startItem = cc.MenuItemLabel.create(startLabel);
        this.startmenu = cc.Menu.create(startItem);
        this.menulayer.addChild(this.startmenu);
        this.startmenu.setVisible(false);
        */
        //pause and help menu
        this.pauselayer=cc.LayerColor.create(cc.c4(10,30,20,150),winSize.width / 2, winSize.height / 2);
        this.pauselayer.setPosition(cc.p(winSize.width / 4, winSize.height / 4));
        //var resumeItem = cc.MenuItemLabel.create(resumeLabel);
        var helpstr = '触摸屏幕发射子弹\n下列情况游戏结束:\n1.漏过3个敌机\n2.子弹打空10次';
        var helpLabel = cc.LabelTTF.create(helpstr, "Arial", 18);
        //var helpItem=cc.MenuItemLabel.create(helpLabel, null, this);
        var resumeItem=cc.MenuItemFont.create('回到游戏', this.resumeGame, this);
        resumeItem.setFontSize(15);
        helpLabel.setPosition(cc.p(winSize.width / 4, winSize.height/ 3));
        resumeItem.setPosition(cc.p(winSize.width / 4, winSize.height / 12));
        this.resumemenu = cc.Menu.create(resumeItem);
        this.resumemenu.setPosition(cc.PointZero);
        this.pauselayer.addChild(helpLabel);
        this.pauselayer.addChild(this.resumemenu);
        //this.resumemenu.setVisible(false);
        this.menulayer.setVisible(false);
        this.pauselayer.setVisible(false);
        this.addChild(this.pauselayer);
        this.addChild(this.menulayer);
    },
    startGame:function(){
        //cc.log('start game');
        audioEngine.playEffect(s_selectEffect);
        this.reset();
        this.status = g_gameStatus.normal;
        this.menulayer.setVisible(false);
        //this.overmenu.setVisible(false);
        if(this.overmenu){
            this.overmenu.removeFromParent();
            this.overmenu = null;
        }
        if(this.scoreLabel){
            this.scoreLabel.removeFromParent();
            this.scoreLabel = null;
        }
        if(this.weixinLabel){
            this.weixinLabel.removeFromParent();
            this.weixinLabel = null;
        }
        //this.startmenu.setVisible(false);

    },
    pauseGame:function(){
        //cc.log('pause game');
        audioEngine.playEffect(s_selectEffect);
        if(this.status == g_gameStatus.pause){
            return;
        }
        this.status = g_gameStatus.pause;
        this.pauselayer.setVisible(true);
        cc.Director.getInstance().pause();
        //this.resumemenu.setVisible(true);
    },
    resumeGame:function(){
        audioEngine.playEffect(s_selectEffect);
        this.status = g_gameStatus.normal;
        this.pauselayer.setVisible(false);
        cc.Director.getInstance().resume();
        //this.resumemenu.setVisible(false);
    },
    reset:function(){
        for(var i=0; i< this._monsters.length; i++){
            node = this._monsters[i];
            node.removeFromParent();
        }
        this._monsters = [];
        for(var i=0; i< this._projectiles.length; i++){
            node = this._projectiles[i];
            node.removeFromParent();
        }
        this._projectiles = [];
        this.miss_bullets = 0;
        this.miss_monsters = 0;
        this.score = 0;
        if('touches' in sys.capabilities){
            this.setTouchEnabled(true);
        }
        if('mouse' in sys.capabilities){
            this.setMouseEnabled(true);
        }
    },
    addMonster:function(){
        var monster = cc.Sprite.createWithSpriteFrameName('12.png');
        var minY = monster.getContentSize().height / 2 + 80;
        var maxY = winSize.height - monster.getContentSize().height / 2;
        var rangeY = maxY - minY;
        var actualY = (Math.random() * rangeY) + minY;

        monster.setPosition(winSize.width + monster.getContentSize().width / 2, actualY);
        this.addChild(monster);

        var minDuration = 2.0;
        var maxDuration = 4.0;
        var rangeDuration = maxDuration - minDuration;
        var actualDuration = (Math.random() % rangeDuration) + minDuration;

        var actionMove = cc.MoveTo.create(actualDuration, cc.p(-monster.getContentSize().width / 2, actualY));
        var actionMoveDone = cc.CallFunc.create(function(node){
            cc.ArrayRemoveObject(this._monsters, node);
            this.miss_monsters += 1;
            node.removeFromParent();

        }, this)
        monster.runAction(cc.Sequence.create(cc.Sequence.create(actionMove, actionMoveDone)));

        monster.setTag(1);
        this._monsters.push(monster);
    },
    gameLogic:function(dt){
        this.addMonster();
    },
    locationTapped:function(location){
        var projectile = cc.Sprite.createWithSpriteFrameName('bullet.png');
        //projectile.setPosition(20, winSize.height/2);
        projectile.setPosition(winSize.width / 2, 20);
        var offset = cc.pSub(location, projectile.getPosition());
        if(offset.y <= 0) return;
        this.addChild(projectile);

        //var realX = winSize.width + (projectile.getContentSize().width / 2);
        //var ratio = offset.y / offset.x;
        //var realY = (realX * ratio) + projectile.getPosition().y;
        var realY = winSize.height + (projectile.getContentSize().height / 2);
        var ratio = offset.x / offset.y;
        var realX = (realY * ratio) + projectile.getPosition().x;
        var realDest = cc.p(realX, realY);

        var offset = cc.pSub(realDest, projectile.getPosition());
        var length = cc.pLength(offset);
        var velocity = 480.0;
        var realMoveDuration = length / velocity;

        projectile.runAction(cc.Sequence.create(
            cc.MoveTo.create(realMoveDuration, realDest),
            cc.CallFunc.create(function(node){
                cc.ArrayRemoveObject(this._projectiles, node);
                this.miss_bullets += 1;
                node.removeFromParent();
            }, this)
        ));

        projectile.setTag(2);
        this._projectiles.push(projectile);
        audioEngine.playEffect(s_shootEffect);
    },

    onMouseUp:function(event){
        if(this.status != g_gameStatus.normal){
            return;
        }
        var location = event.getLocation();
        v = cc.EGLView.getInstance()
        location = cc.p((location.x - v._viewPortRect.x) / v._scaleX, (location.y - v._viewPortRect.y) / v._scaleY)
        //cc.log(location);
        this.locationTapped(location);
    },

    onTouchesEnded:function(touches, event){
        if(this.status != g_gameStatus.normal){
            return;
        }
        if(touches.length <= 0)
            return;
        var touch = touches[0];
        var location = touch.getLocation();
        this.locationTapped(location);
    },
    update:function(dt){
        if(this.status != g_gameStatus.normal){
            return;
        }
        for(var i=0; i<this._projectiles.length; i++){
            var projectile = this._projectiles[i];
            for(var j=0; j<this._monsters.length; j++){
                var monster = this._monsters[j];
                var projectileRect = projectile.getBoundingBox();
                var monsterRect = monster.getBoundingBox();
                if(cc.rectIntersectsRect(projectileRect, monsterRect)){
                    //cc.log('collision!');
                    this.score += 10;
                    cc.ArrayRemoveObject(this._projectiles, projectile);
                    projectile.removeFromParent();
                    var a = Explosion.getOrCreateExplosion();
                    a.setPosition(monster.getPosition());
                    cc.ArrayRemoveObject(this._monsters, monster);
                    monster.removeFromParent();
                    this._monstersDestroyed++;
                    /*
                    if(this._monstersDestroyed >= 2){
                        var scene = GameOver.scene(true);
                        cc.Director.getInstance().replaceScene(scene);
                    }
                    */
                }
            }
        }
        this.updateUI();
    },
    updateUI:function(){


        this.lbScore.setString("Score: " + this.score);
        this.lbmonsters.setString("miss enemy: " + this.miss_monsters);
        this.lbbullets.setString("miss hit: " + this.miss_bullets);
        if(this.miss_bullets >= 10 || this.miss_monsters >= 3){
            this.overGame();
            //var scene = GameOver.scene(false);
            //cc.Director.getInstance().replaceScene(scene);
            //cc.Director.getInstance().replaceScene(cc.TransitionFade.create(1.2, scene));
        }
    },
    overGame:function(){
        this.status = g_gameStatus.gameover;
        this.menulayer.setVisible(true);
        //game over menu

        //var scoreLabel = cc.LabelBMFont.create(this.score.toString(), s_arial14_fnt);
        //var scoreItem=cc.MenuItemLabel.create(scoreLabel);
        var scorestr = this.score.toString();
        this.scoreLabel = cc.LabelTTF.create(scorestr, "Arial", 30);
        var weixinstr = '欢迎关注微信号:\n qinglvmiyu';
        this.weixinLabel = cc.LabelTTF.create(weixinstr, "Arial", 18);
        //var yixinstr = '欢迎关注易信号:情侣蜜语';
        //scoreItem.setScale(3);
        //var restartLabel = cc.LabelBMFont.create('restart', s_arial14_fnt);
        //var restartItem = cc.MenuItemLabel.create(restartLabel, this.startGame, this);
        var restartItem=cc.MenuItemFont.create('restart', this.startGame, this);
        restartItem.setFontSize(15);
        this.scoreLabel.setPosition(cc.p(winSize.width / 4, winSize.height/ 3));
        this.weixinLabel.setPosition(cc.p(winSize.width / 4, winSize.height / 5));
        restartItem.setPosition(cc.p(winSize.width / 4, winSize.height / 12));
        this.overmenu=cc.Menu.create(restartItem);
        this.menulayer.addChild(this.scoreLabel);
        this.menulayer.addChild(this.weixinLabel);
        this.menulayer.addChild(this.overmenu);
        this.overmenu.setPosition(cc.PointZero);
        this.overmenu.setVisible(true);
        if('touches' in sys.capabilities){
            this.setTouchEnabled(false);
        }
        if('mouse' in sys.capabilities){
            this.setMouseEnabled(false);
        }
    }
});

MainLayer.create = function(){
    var sg = new MainLayer();
    if (sg && sg.init(cc.c4b(255, 255, 255, 150))){
        return sg;
    }
    return null;
};

MainLayer.scene = function(){
    var scene = cc.Scene.create();
    var layer = MainLayer.create();
    scene.addChild(layer);
    return scene;
}
MainLayer.prototype.addExplosions = function (explosion) {
    this._explosions.addChild(explosion);
};