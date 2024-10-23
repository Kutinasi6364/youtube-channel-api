document.addEventListener(
    "DOMContentLoaded", 
    function() {
        const sakuraContainer = document.querySelector('.sakura-background');

        // 桜の花びらを作成する関数
        function createSakura() {
            const sakura = document.createElement('div');
            sakura.classList.add('sakura');
            sakuraContainer.appendChild(sakura);

            // ランダムな横方向の位置に花びらを配置
            sakura.style.left = Math.random() * 100 + 'vw';

            // 花びらを一定時間後に削除する
            setTimeout(() => {
                sakura.remove();
            }, 50000); // 花びらが画面を落ちるまでの時間
        }

        // 花びらを定期的に生成
        setInterval(createSakura, 10000);
    }
);

