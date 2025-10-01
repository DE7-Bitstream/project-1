// 입력 검증
document.getElementById('filterForm').addEventListener('submit', function(e){
    ////////////////////
    const MAX_MONTHS = 12;
    const MAX_RANK = 30;
    ////////////////////

    const startYear = parseInt(document.getElementById('start_year').value);
    const startMonth = parseInt(document.getElementById('start_month').value);
    const endYear = parseInt(document.getElementById('end_year').value);
    const endMonth = parseInt(document.getElementById('end_month').value);
    const maxRank = parseInt(document.getElementById('max_rank').value);


    if ((startYear > endYear) || (startYear === endYear && startMonth > endMonth)) {
        alert("시작 연도/월이 끝 연도/월보다 늦습니다.");
        e.preventDefault();
        return;
    }

    const monthsDiff = (endYear - startYear) * 12 + (endMonth - startMonth + 1);
    if (monthsDiff > MAX_MONTHS) {
        alert(`최대 ${MAX_MONTHS}개월까지 조회 가능합니다.`);
        e.preventDefault();
        return;
    }

    if (maxRank > MAX_RANK) {
        alert(`최대 순위는 ${MAX_RANK}까지만 조회 가능합니다.`);
        e.preventDefault();
        return;
    }
});

///////////////////////
//// 차트 관련 함수   ////
///////////////////////
// 모든 주차 라벨 추출 및 정렬 ()
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
            artist: data.artist,
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

// 차트 높이 동적 설정
function setDynamicChartHeight(canvasId, totalRanks) {
    const baseHeight = 400; // 기본 높이
    const extraHeightPerRank = 25; // rank 1개당 추가 높이
    const canvas = document.getElementById(canvasId);
    canvas.style.height = (baseHeight + extraHeightPerRank * totalRanks) + "px";
}

// 차트 렌더링
function renderWeeklyChart(songData, canvasId) {
    const xLabels = extractAndSortLabels(songData);
    const totalSongs = Object.keys(songData).length;

    const maxRank = Math.max(...Object.values(songData).flatMap(d => d.y));
    setDynamicChartHeight(canvasId, maxRank);

    const colors = generateDistinctColors(totalSongs);
    const datasets = createDatasets(songData, xLabels, colors).map(ds => ({
        ...ds,
        hoverBorderWidth: 4,  // 마우스 오버 시 선 굵기
        hoverRadius: 7,         // 마우스 오버 시 점 크기
    }));

    const ctx = document.getElementById(canvasId).getContext('2d');

    const chart = new Chart(ctx, {
        type: 'line',
        data: { labels: xLabels, datasets },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: { reverse: true, title: { display: true, text: '순위' }, ticks: { stepSize: 1 } },
                x: { title: { display: true, text: '주차' } }
            },
            plugins: {
                title: { display: true, text: '주간 차트 순위 변화 *melon 차트 기준' },
                legend: {
                    position: 'top',
                    labels: {
                        generateLabels: function(chart) {
                            const datasets = chart.data.datasets;
                            return datasets.map((dataset, i) => {
                                const meta = chart.getDatasetMeta(i);
                                const hidden = meta.hidden; // 현재 숨김 여부
                                return {
                                    text: dataset.label,
                                    fillStyle: dataset.borderColor,
                                    strokeStyle: dataset.borderColor,
                                    lineWidth: dataset.borderWidth,
                                    hidden: false,
                                    fontColor: hidden ? 'darkgray' : '#000', // 숨김이면 글자색 회색
                                    datasetIndex: i,
                                };
                            });
                        }
                    },

                    onClick: (e, legendItem, legend) => {
                        const index = legendItem.datasetIndex;
                        const meta = legend.chart.getDatasetMeta(index);
                        meta.hidden = !meta.hidden; // meta.hidden 기준으로 토글
                        legend.chart.update();
                    },
                    onHover: (event, legendItem, legend) => {
                        // 범례에 마우스를 올릴 때
                        const datasetIndex = legendItem.datasetIndex;
                        const dataset = legend.chart.data.datasets[datasetIndex];

                        // 꺾은선과 점의 스타일 변경
                        dataset.borderWidth = 4; 
                        dataset.pointRadius = 7; 
                        legend.chart.update();
                    },
                    onLeave: (event, legendItem, legend) => {
                        // 범례에서 마우스를 뗄 때
                        const datasetIndex = legendItem.datasetIndex;
                        const dataset = legend.chart.data.datasets[datasetIndex];

                        // 꺾은선과 점의 스타일 원래대로 복원
                        dataset.borderWidth = 2;
                        dataset.pointRadius = 5;
                        legend.chart.update();
                    },
                },
                tooltip: {
                    mode: 'nearest',
                    intersect: true,
                    callbacks: {
                        label: context => `${context.dataset.label} - ${context.dataset.artist} | 순위: ${context.raw ?? '순위 없음'}`
                    }
                }
            },
            interaction: { mode: 'dataset', intersect: true },
        }
    });

    // 포인트 클릭 -> 사라지기
    ctx.canvas.addEventListener('click', (event) => {
        const points = chart.getElementsAtEventForMode(event, 'nearest', { intersect: true }, true);
        if (points.length) {
            const datasetIndex = points[0].datasetIndex;
            const meta = chart.getDatasetMeta(datasetIndex);
            meta.hidden = !meta.hidden; // meta.hidden 기준으로 토글
            chart.update();
        }
    });

    // 전체 토글 버튼
    const toggleBtn = document.getElementById('toggleAllBtn');
    toggleBtn.addEventListener('click', () => {
        // 하나라도 숨겨져 있으면 전체 표시, 아니면 전체 숨김
        const anyHidden = chart.data.datasets.some((dataset, idx) => chart.getDatasetMeta(idx).hidden);
        chart.data.datasets.forEach((dataset, idx) => {
            const meta = chart.getDatasetMeta(idx);
            meta.hidden = !anyHidden; // meta.hidden 기준
        });
        chart.update();
    });
}

const songData = JSON.parse(document.getElementById("song-data").textContent);
renderWeeklyChart(songData, 'weeklyChart');
