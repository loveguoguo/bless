/**
 * Created with PyCharm.
 * User: kier
 * Date: 13-8-26
 * Time: 下午9:00
 * To change this template use File | Settings | File Templates.
 */
var dirArt = "art/";
var dirSounds = 'sounds/';

var s_use_plist = dirArt + 'use.plist';
var s_use = dirArt + 'use.png';

var s_explosion = dirArt + "explosion.png";
var s_explosion_plist = dirArt + "explosion.plist";

var s_bgMusic = dirSounds + 'background-music.mp3';
var s_bgMusicOgg = dirSounds + 'background-music.ogg';
var s_bgMusicWav = dirSounds + 'background-music.wav';

var s_shootEffect = dirSounds + "shoot.mp3";
var s_shootEffectOgg = dirSounds + "shoot.ogg";
var s_shootEffectWav = dirSounds + "shoot.wav";

var s_selectEffect = dirSounds + "select.mp3";
var s_selectEffectOgg = dirSounds + "select.ogg";
var s_selectEffectWav = dirSounds + 'select.wav';

var s_explosionEffect = dirSounds + 'explosion.mp3';
var s_explosionEffectOgg = dirSounds + 'explosion.ogg';
var s_explosionEffectWav = dirSounds + 'explosion.wav';


var g_resources = [
    {src:s_use},
    {src:s_use_plist},
    {src:s_explosion},
    {src:s_explosion_plist},
    {src:s_bgMusic},
    {src:s_bgMusicOgg},
    {src:s_bgMusicWav},
    {src:s_shootEffect},
    {src:s_shootEffectOgg},
    {src:s_shootEffectWav},
    {src:s_selectEffect},
    {src:s_selectEffectOgg},
    {src:s_selectEffectWav},
    {src:s_explosionEffect},
    {src:s_explosionEffectOgg},
    {src:s_explosionEffectWav}
    // FNT
]

/*
var g_resources =[
    {type:"image", src:s_player},
    {type:"image", src:s_monster},
    {type:"image", src:s_projectile},

    {type:'sound', src:s_bgMusic},
    {type:'sound', src:s_bgMusicOgg},
    {type:'sound', src:s_bgMusicWav},

    {type:'sound', src:s_shootEffect},
    {type:'sound', src:s_shootEffectOgg},
    {type:'sound', src:s_shootEffectWav}
];
*/
