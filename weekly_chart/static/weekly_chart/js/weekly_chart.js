// 모든 주차 라벨 추출 및 정렬
function extractAndSortLabels(songData) {
    const allLabelsSet = new Set();
    Object.values(songData).forEach(song => song.x.forEach(label => allLabelsSet.add(label)));

    return Array.from(allLabelsSet).sort((a, b) => {
        const [am, aw] = a.match(/\d+/g).map(Number);
        const [bm, bw] = b.match(/\d+/g).map(Number);
        return am !== bm ? am - bm : aw - bw;
    });
}

// 서로 다른 색 생성 (HSL)
function generateDistinctColors(n) {
    const colors = [];
    const saturation = 70;
    const lightness = 50;

    for (let i = 0; i < n; i++) {
        const hue = Math.round((360 / n) * i);
        colors.push(`hsl(${hue}, ${saturation}%, ${lightness}%)`);
    }
    return colors;
}

// 곡별 dataset 변환
function createDatasets(songData, xLabels, colors) {
    return Object.entries(songData).map(([song, data], idx) => {
        const songMap = Object.fromEntries(data.x.map((label, i) => [label, data.y[i]]));
        const alignedData = xLabels.map(label => songMap[label] ?? null);

        return {
            label: song,
            data: alignedData,
            borderColor: colors[idx],
            backgroundColor: colors[idx],
            borderWidth: 2,
            pointRadius: 4,
            pointHoverRadius: 6,
            spanGaps: false
        };
    });
}

// 차트 그리기
function renderWeeklyChart(songData, canvasId) {
    const xLabels = extractAndSortLabels(songData);
    const totalSongs = Object.keys(songData).length;
    const colors = generateDistinctColors(totalSongs);
    const datasets = createDatasets(songData, xLabels, colors);

    const ctx = document.getElementById(canvasId).getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: { labels: xLabels, datasets },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    reverse: true,
                    title: { display: true, text: '순위' },
                    ticks: { stepSize: 1 }
                },
                x: { title: { display: true, text: '주차' } }
            },
            plugins: {
                title: { display: true, text: '주간 차트 순위 변화' },
                legend: { position: 'top' },
                tooltip: {
                    callbacks: {
                        label: context => `${context.dataset.label} | 순위: ${context.raw ?? '순위 없음'}`
                    }
                }
            }
        }
    });
}

// 실행
const songData = JSON.parse(document.getElementById("song-data").textContent);
renderWeeklyChart(songData, 'weeklyChart');
