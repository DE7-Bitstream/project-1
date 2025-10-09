let chartInstance = null;
let currentYear = null;
let currentCategory = null;

// 페이지 로드 시 초기화
document.addEventListener('DOMContentLoaded', function() {
    // select 요소가 존재하는지 확인
    const yearSelect = document.getElementById('year-select');
    const categorySelect = document.getElementById('category-select');
    
    if (!yearSelect || !categorySelect) {
        console.error('Select elements not found');
        return;
    }
    
    currentYear = yearSelect.value;
    currentCategory = categorySelect.value;
    
    console.log('Initial year:', currentYear);
    console.log('Initial category:', currentCategory);
    
    updateTitle();
    loadChartData();
    
    // 이벤트 리스너 등록
    yearSelect.addEventListener('change', function() {
        currentYear = this.value;
        updateTitle();
        loadChartData();
    });
    
    categorySelect.addEventListener('change', function() {
        currentCategory = this.value;
        updateTitle();
        loadChartData();
    });
});

// 제목 업데이트
function updateTitle() {
    const chartTitle = document.getElementById('chart-title');
    chartTitle.textContent = `${currentYear}년 TOP5 ${currentCategory}`;
}

// 차트 데이터 로드
async function loadChartData() {
    console.log('Loading chart data for:', currentYear, currentCategory);
    
    try {
        const url = `/hitmakers/api/chart-data/?year=${currentYear}&category=${encodeURIComponent(currentCategory)}`;
        console.log('Fetching URL:', url);
        
        const response = await fetch(url);
        
        console.log('Response status:', response.status);
        
        if (!response.ok) {
            const errorText = await response.text();
            console.error('Error response:', errorText);
            throw new Error('데이터 로드 실패');
        }
        
        const data = await response.json();
        console.log('Received data:', data);
        
        if (data.length === 0) {
            alert('해당 연도/카테고리에 데이터가 없습니다.');
            return;
        }
        
        renderChart(data);
        clearSongTable();
        
    } catch (error) {
        console.error('Error in loadChartData:', error);
        alert('데이터를 불러오는데 실패했습니다: ' + error.message);
    }
}

// 차트 렌더링
function renderChart(data) {
    const ctx = document.getElementById('donut-chart').getContext('2d');
    
    // 기존 차트 제거
    if (chartInstance) {
        chartInstance.destroy();
    }
    
    const labels = data.map(item => item.label);
    const values = data.map(item => item.value);
    
    // 프로젝트 컬러 팔레트 (청록색 계열)
    const colors = [
        'rgba(23, 162, 184, 0.8)',   // 청록색
        'rgba(32, 201, 151, 0.8)',   // 민트색
        'rgba(52, 144, 220, 0.8)',   // 파란색
        'rgba(111, 66, 193, 0.8)',   // 보라색
        'rgba(155, 89, 182, 0.8)'    // 연보라색
    ];
    
    const borderColors = [
        'rgba(23, 162, 184, 1)',
        'rgba(32, 201, 151, 1)',
        'rgba(52, 144, 220, 1)',
        'rgba(111, 66, 193, 1)',
        'rgba(155, 89, 182, 1)'
    ];
    
    chartInstance = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                data: values,
                backgroundColor: colors,
                borderColor: borderColors,
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        padding: 15,
                        font: {
                            size: 12
                        }
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    padding: 12,
                    titleFont: {
                        size: 14
                    },
                    bodyFont: {
                        size: 13
                    },
                    callbacks: {
                        label: function(context) {
                            const value = context.parsed;
                            return `  ${value}곡`;
                        }
                    }
                }
            },
            onClick: (event, elements) => {
                if (elements.length > 0) {
                    const index = elements[0].index;
                    const label = labels[index];
                    loadTopSongs(label);
                }
            }
        }
    });
}

// 대표 곡 로드 (상위 차트 랭킹 곡)
async function loadTopSongs(label) {
    const wrapper = document.getElementById('song-table-wrapper');
    wrapper.innerHTML = '<p class="empty-message">로딩중...</p>';
    
    try {
        const response = await fetch(
            `/hitmakers/api/top-songs/?year=${currentYear}&category=${encodeURIComponent(currentCategory)}&label=${encodeURIComponent(label)}`
        );
        
        if (!response.ok) {
            throw new Error('곡 데이터 로드 실패');
        }
        
        const songs = await response.json();
        renderSongTable(songs, label);
        
    } catch (error) {
        console.error('Error:', error);
        wrapper.innerHTML = '<p class="empty-message">곡을 불러오는데 실패했습니다.</p>';
    }
}

// 테이블 렌더링
function renderSongTable(songs, label) {
    const wrapper = document.getElementById('song-table-wrapper');
    
    if (songs.length === 0) {
        wrapper.innerHTML = '<p class="empty-message">곡이 없습니다.</p>';
        return;
    }
    
    let html = `<div class="selected-label">${label}</div>`;
    
    html += `
        <table class="songs-table">
            <thead>
                <tr>
                    <th>순위</th>
                    <th>가수</th>
                    <th>노래제목</th>
                </tr>
            </thead>
            <tbody>
    `;
    
    songs.forEach(song => {
        html += `
            <tr>
                <td class="rank-cell">#${song.rank}</td>
                <td class="singer-cell">${song.singer}</td>
                <td class="title-cell">${song.title}</td>
            </tr>
        `;
    });
    
    html += `
            </tbody>
        </table>
    `;
    
    wrapper.innerHTML = html;
}

// 테이블 초기화
function clearSongTable() {
    document.getElementById('song-table-wrapper').innerHTML = 
        '<p class="empty-message">차트를 클릭하여 곡을 확인하세요</p>';
    
    const tableTitle = document.getElementById('table-title');
    tableTitle.textContent = '대표 곡';
}