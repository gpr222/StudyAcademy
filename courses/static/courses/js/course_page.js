let player;
document.onreadystatechange = () => {
    if (document.readyState == 'interactive') {
        player = document.getElementById('player');
        video_list = document.getElementById('video_list');
        maintainRatio();
    }
}
maintainRatio = () => {
    let w = player.clientWidth;
    let h = (w * 9) / 16;
    player.height = h;
    video_list.style.maxHeight = h + 'px';
}
window.onresize = maintainRatio;