// 전역 변수
let currentFilter = 'all';
let selectedSongId = null;

// DOM 요소
const searchInput = document.getElementById('searchInput');
const searchBtn = document.getElementById('searchBtn');
const songsList = document.getElementById('songsList');
const popularList = document.getElementById('popularList');
const queueList = document.getElementById('queueList');
const nowPlayingInfo = document.getElementById('nowPlayingInfo');

// 모달 요소
const reserveModal = document.getElementById('reserveModal');
const adminModal = document.getElementById('adminModal');
const adminBtn = document.getElementById('adminBtn');
const addSongForm = document.getElementById('addSongForm');

// 초기화
document.addEventListener('DOMContentLoaded', () => {
    loadSongs();
    loadPopularSongs();
    loadQueue();
    setupEventListeners();
});

// 이벤트 리스너 설정
function setupEventListeners() {
    // 검색
    searchBtn.addEventListener('click', performSearch);
    searchInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') performSearch();
    });

    // 필터 버튼
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
            e.target.classList.add('active');
            currentFilter = e.target.dataset.filter;
            loadSongs();
        });
    });

    // 탭 버튼
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const tabName = e.target.dataset.tab;
            switchTab(tabName);
        });
    });

    // 모달 관련
    adminBtn.addEventListener('click', () => {
        adminModal.style.display = 'block';
    });

    document.querySelectorAll('.close').forEach(closeBtn => {
        closeBtn.addEventListener('click', (e) => {
            e.target.closest('.modal').style.display = 'none';
        });
    });

    window.addEventListener('click', (e) => {
        if (e.target.classList.contains('modal')) {
            e.target.style.display = 'none';
        }
    });

    // 예약 확인
    document.getElementById('confirmReserve').addEventListener('click', makeReservation);

    // 노래 추가 폼
    addSongForm.addEventListener('submit', addNewSong);
}

// 탭 전환
function switchTab(tabName) {
    // 탭 버튼 활성화
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
        if (btn.dataset.tab === tabName) {
            btn.classList.add('active');
        }
    });

    // 탭 콘텐츠 표시
    document.querySelectorAll('.tab-pane').forEach(pane => {
        pane.classList.remove('active');
    });
    document.getElementById(`${tabName}-tab`).classList.add('active');

    // 데이터 새로고침
    if (tabName === 'popular') {
        loadPopularSongs();
    } else if (tabName === 'queue') {
        loadQueue();
    }
}

// 노래 목록 로드
async function loadSongs() {
    try {
        let url = '/api/songs';
        if (currentFilter !== 'all') {
            url += `?genre=${currentFilter}`;
        }
        
        const response = await fetch(url);
        const songs = await response.json();
        
        displaySongs(songs);
    } catch (error) {
        console.error('노래 목록 로드 실패:', error);
    }
}

// 노래 표시
function displaySongs(songs) {
    if (songs.length === 0) {
        songsList.innerHTML = '<p style="text-align: center; color: #999;">노래가 없습니다.</p>';
        return;
    }

    songsList.innerHTML = songs.map(song => `
        <div class="song-card" onclick="showReserveModal(${song.id}, '${song.title}', '${song.artist}')">
            <h3>${song.title}</h3>
            <p class="artist">${song.artist}</p>
            ${song.genre ? `<span class="genre">${getGenreLabel(song.genre)}</span>` : ''}
        </div>
    `).join('');
}

// 장르 라벨 변환
function getGenreLabel(genre) {
    const labels = {
        'ballad': '발라드',
        'dance': '댄스',
        'rock': '록',
        'trot': '트로트',
        'pop': '팝송'
    };
    return labels[genre] || genre;
}

// 검색 수행
async function performSearch() {
    const searchTerm = searchInput.value.trim();
    if (!searchTerm) {
        loadSongs();
        return;
    }

    try {
        const response = await fetch(`/api/songs?search=${encodeURIComponent(searchTerm)}`);
        const songs = await response.json();
        displaySongs(songs);
    } catch (error) {
        console.error('검색 실패:', error);
    }
}

// 인기 차트 로드
async function loadPopularSongs() {
    try {
        const response = await fetch('/api/popular');
        const songs = await response.json();
        
        if (songs.length === 0) {
            popularList.innerHTML = '<p style="text-align: center; color: #999;">아직 재생된 노래가 없습니다.</p>';
            return;
        }

        popularList.innerHTML = songs.map((song, index) => `
            <div class="popular-item" onclick="showReserveModal(${song.id}, '${song.title}', '${song.artist}')">
                <span class="rank">${index + 1}</span>
                <div class="popular-info">
                    <h4>${song.title}</h4>
                    <p>${song.artist}</p>
                    <span class="play-count">재생 ${song.play_count}회</span>
                </div>
            </div>
        `).join('');
    } catch (error) {
        console.error('인기 차트 로드 실패:', error);
    }
}

// 예약 대기열 로드
async function loadQueue() {
    try {
        const response = await fetch('/api/queue');
        const queue = await response.json();
        
        if (queue.length === 0) {
            queueList.innerHTML = '<p style="text-align: center; color: #999;">예약된 노래가 없습니다.</p>';
            return;
        }

        queueList.innerHTML = queue.map((item, index) => `
            <div class="queue-item">
                <div class="queue-info">
                    <h4>${index + 1}. ${item.title}</h4>
                    <p>${item.artist}</p>
                    <span class="user">예약자: ${item.user_name}</span>
                </div>
                <button class="cancel-btn" onclick="cancelReservation(${item.id})">
                    <i class="fas fa-times"></i> 취소
                </button>
            </div>
        `).join('');

        // 첫 번째 노래를 현재 재생 중으로 표시
        if (queue.length > 0) {
            updateNowPlaying(queue[0]);
        }
    } catch (error) {
        console.error('예약 대기열 로드 실패:', error);
    }
}

// 현재 재생 중 업데이트
function updateNowPlaying(song) {
    if (song) {
        nowPlayingInfo.innerHTML = `
            <h4>${song.title}</h4>
            <p>${song.artist}</p>
            <p style="color: #666; font-size: 0.9rem;">예약자: ${song.user_name}</p>
        `;
    } else {
        nowPlayingInfo.innerHTML = '<p>재생 중인 노래가 없습니다</p>';
    }
}

// 예약 모달 표시
function showReserveModal(songId, title, artist) {
    selectedSongId = songId;
    document.getElementById('selectedSongInfo').innerHTML = `
        <h3>${title}</h3>
        <p>${artist}</p>
    `;
    document.getElementById('userName').value = '';
    reserveModal.style.display = 'block';
}

// 예약하기
async function makeReservation() {
    const userName = document.getElementById('userName').value.trim();
    
    if (!userName) {
        alert('이름을 입력해주세요.');
        return;
    }

    try {
        const response = await fetch('/api/queue', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                song_id: selectedSongId,
                user_name: userName
            })
        });

        if (response.ok) {
            alert('예약되었습니다!');
            reserveModal.style.display = 'none';
            loadQueue();
            switchTab('queue');
        } else {
            alert('예약에 실패했습니다.');
        }
    } catch (error) {
        console.error('예약 실패:', error);
        alert('예약에 실패했습니다.');
    }
}

// 예약 취소
async function cancelReservation(queueId) {
    if (!confirm('예약을 취소하시겠습니까?')) {
        return;
    }

    try {
        const response = await fetch(`/api/queue/${queueId}`, {
            method: 'DELETE'
        });

        if (response.ok) {
            loadQueue();
        } else {
            alert('취소에 실패했습니다.');
        }
    } catch (error) {
        console.error('예약 취소 실패:', error);
        alert('취소에 실패했습니다.');
    }
}

// 새 노래 추가
async function addNewSong(e) {
    e.preventDefault();
    
    const formData = new FormData(addSongForm);
    
    try {
        const response = await fetch('/api/songs', {
            method: 'POST',
            body: formData
        });

        if (response.ok) {
            alert('노래가 추가되었습니다!');
            adminModal.style.display = 'none';
            addSongForm.reset();
            loadSongs();
        } else {
            alert('노래 추가에 실패했습니다.');
        }
    } catch (error) {
        console.error('노래 추가 실패:', error);
        alert('노래 추가에 실패했습니다.');
    }
}

// 재생 시작 (실제 구현 시 오디오 플레이어와 연동)
async function startPlaying(songId) {
    try {
        const response = await fetch(`/api/play/${songId}`, {
            method: 'POST'
        });

        if (response.ok) {
            console.log('재생 시작');
            loadQueue();
        }
    } catch (error) {
        console.error('재생 시작 실패:', error);
    }
}