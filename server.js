const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
const sqlite3 = require('sqlite3').verbose();
const path = require('path');
const multer = require('multer');
const fs = require('fs');

const app = express();
const PORT = process.env.PORT || 3000;

// 미들웨어 설정
app.use(cors());
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));
app.use(express.static('public'));
app.use('/uploads', express.static('uploads'));

// 업로드 디렉토리 생성
if (!fs.existsSync('uploads')) {
    fs.mkdirSync('uploads');
}
if (!fs.existsSync('uploads/songs')) {
    fs.mkdirSync('uploads/songs');
}
if (!fs.existsSync('uploads/lyrics')) {
    fs.mkdirSync('uploads/lyrics');
}

// 파일 업로드 설정
const storage = multer.diskStorage({
    destination: function (req, file, cb) {
        if (file.fieldname === 'song') {
            cb(null, 'uploads/songs/');
        } else if (file.fieldname === 'lyrics') {
            cb(null, 'uploads/lyrics/');
        }
    },
    filename: function (req, file, cb) {
        const uniqueSuffix = Date.now() + '-' + Math.round(Math.random() * 1E9);
        cb(null, uniqueSuffix + path.extname(file.originalname));
    }
});

const upload = multer({ storage: storage });

// 데이터베이스 초기화
const db = new sqlite3.Database('./karaoke.db');

// 테이블 생성
db.serialize(() => {
    // 노래 테이블
    db.run(`CREATE TABLE IF NOT EXISTS songs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        artist TEXT NOT NULL,
        genre TEXT,
        year INTEGER,
        song_file TEXT,
        lyrics_file TEXT,
        duration INTEGER,
        play_count INTEGER DEFAULT 0,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )`);

    // 예약 대기열 테이블
    db.run(`CREATE TABLE IF NOT EXISTS queue (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        song_id INTEGER,
        user_name TEXT NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        status TEXT DEFAULT 'waiting',
        FOREIGN KEY (song_id) REFERENCES songs (id)
    )`);

    // 인기 차트 뷰
    db.run(`CREATE VIEW IF NOT EXISTS popular_songs AS
        SELECT id, title, artist, play_count
        FROM songs
        ORDER BY play_count DESC
        LIMIT 100`);
});

// API 라우트

// 모든 노래 조회
app.get('/api/songs', (req, res) => {
    const { search, genre, artist } = req.query;
    let query = 'SELECT * FROM songs WHERE 1=1';
    const params = [];

    if (search) {
        query += ' AND (title LIKE ? OR artist LIKE ?)';
        params.push(`%${search}%`, `%${search}%`);
    }
    if (genre) {
        query += ' AND genre = ?';
        params.push(genre);
    }
    if (artist) {
        query += ' AND artist LIKE ?';
        params.push(`%${artist}%`);
    }

    query += ' ORDER BY title ASC';

    db.all(query, params, (err, rows) => {
        if (err) {
            res.status(500).json({ error: err.message });
            return;
        }
        res.json(rows);
    });
});

// 특정 노래 조회
app.get('/api/songs/:id', (req, res) => {
    const { id } = req.params;
    db.get('SELECT * FROM songs WHERE id = ?', [id], (err, row) => {
        if (err) {
            res.status(500).json({ error: err.message });
            return;
        }
        if (!row) {
            res.status(404).json({ error: '노래를 찾을 수 없습니다.' });
            return;
        }
        res.json(row);
    });
});

// 노래 추가
app.post('/api/songs', upload.fields([
    { name: 'song', maxCount: 1 },
    { name: 'lyrics', maxCount: 1 }
]), (req, res) => {
    const { title, artist, genre, year, duration } = req.body;
    const songFile = req.files['song'] ? req.files['song'][0].filename : null;
    const lyricsFile = req.files['lyrics'] ? req.files['lyrics'][0].filename : null;

    db.run(
        `INSERT INTO songs (title, artist, genre, year, song_file, lyrics_file, duration)
         VALUES (?, ?, ?, ?, ?, ?, ?)`,
        [title, artist, genre, year, songFile, lyricsFile, duration],
        function(err) {
            if (err) {
                res.status(500).json({ error: err.message });
                return;
            }
            res.json({ id: this.lastID, message: '노래가 추가되었습니다.' });
        }
    );
});

// 인기 차트 조회
app.get('/api/popular', (req, res) => {
    db.all('SELECT * FROM popular_songs', (err, rows) => {
        if (err) {
            res.status(500).json({ error: err.message });
            return;
        }
        res.json(rows);
    });
});

// 예약 대기열 조회
app.get('/api/queue', (req, res) => {
    db.all(
        `SELECT q.*, s.title, s.artist 
         FROM queue q 
         JOIN songs s ON q.song_id = s.id 
         WHERE q.status = 'waiting'
         ORDER BY q.created_at ASC`,
        (err, rows) => {
            if (err) {
                res.status(500).json({ error: err.message });
                return;
            }
            res.json(rows);
        }
    );
});

// 예약 추가
app.post('/api/queue', (req, res) => {
    const { song_id, user_name } = req.body;
    
    db.run(
        'INSERT INTO queue (song_id, user_name) VALUES (?, ?)',
        [song_id, user_name],
        function(err) {
            if (err) {
                res.status(500).json({ error: err.message });
                return;
            }
            res.json({ id: this.lastID, message: '예약되었습니다.' });
        }
    );
});

// 예약 삭제
app.delete('/api/queue/:id', (req, res) => {
    const { id } = req.params;
    
    db.run('DELETE FROM queue WHERE id = ?', [id], function(err) {
        if (err) {
            res.status(500).json({ error: err.message });
            return;
        }
        res.json({ message: '예약이 취소되었습니다.' });
    });
});

// 현재 재생 중인 노래 설정
app.post('/api/play/:id', (req, res) => {
    const { id } = req.params;
    
    // 재생 횟수 증가
    db.run(
        'UPDATE songs SET play_count = play_count + 1 WHERE id = ?',
        [id],
        (err) => {
            if (err) {
                res.status(500).json({ error: err.message });
                return;
            }
            
            // 대기열에서 상태 업데이트
            db.run(
                'UPDATE queue SET status = "playing" WHERE song_id = ? AND status = "waiting" LIMIT 1',
                [id],
                function(err) {
                    if (err) {
                        res.status(500).json({ error: err.message });
                        return;
                    }
                    res.json({ message: '재생이 시작되었습니다.' });
                }
            );
        }
    );
});

// 서버 시작
app.listen(PORT, () => {
    console.log(`노래방 서버가 포트 ${PORT}에서 실행 중입니다.`);
});