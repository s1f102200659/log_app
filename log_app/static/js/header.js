fetch('/header/url/')
    .then(response => response.text())
    .then(data => {
        // ヘッダーの内容を更新
        document.querySelector('header').innerHTML = data;

        // 時刻を表示する要素を追加
        updateTime(); // ページ読み込み時に初期時刻を表示
        setInterval(updateTime, 1000); // 1秒ごとに時刻を更新
    })
    .catch(error => console.log('Error fetching header:', error));

function updateTime() {
    // 現在時刻を取得して表示
    const currentTimeElement = document.getElementById('current-time');
    const now = new Date();

    // 年、月、日、時、分、秒を取得
    const year = now.getFullYear();
    const month = String(now.getMonth() + 1).padStart(2, '0'); // 月は0から始まるので+1
    const day = String(now.getDate()).padStart(2, '0');
    const hours = String(now.getHours()).padStart(2, '0');
    const minutes = String(now.getMinutes()).padStart(2, '0');
    const seconds = String(now.getSeconds()).padStart(2, '0');

    // フォーマットした日付と時刻を表示
    const timeString = `${year}/${month}/${day} ${hours}:${minutes}:${seconds}`;

    if (currentTimeElement) {
        currentTimeElement.textContent = timeString;
    }
}


