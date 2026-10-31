import express from 'express';
import http from 'http';
import { WebSocketServer, WebSocket } from 'ws';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
const server = http.createServer(app);
const PORT = process.env.PORT || 3000;

app.use(express.json());

// Ensure data directory exists
const DATA_DIR = path.join(__dirname, 'data');
const SUBMISSIONS_FILE = path.join(DATA_DIR, 'student_results.json');

if (!fs.existsSync(DATA_DIR)) {
  fs.mkdirSync(DATA_DIR, { recursive: true });
}

// Seed default initial results if not present
function loadSubmissions(): any[] {
  try {
    if (fs.existsSync(SUBMISSIONS_FILE)) {
      const content = fs.readFileSync(SUBMISSIONS_FILE, 'utf-8');
      return JSON.parse(content);
    }
  } catch (err) {
    console.error('Error reading submissions:', err);
  }
  return [];
}

function saveSubmissions(data: any[]) {
  try {
    fs.writeFileSync(SUBMISSIONS_FILE, JSON.stringify(data, null, 2), 'utf-8');
  } catch (err) {
    console.error('Error saving submissions:', err);
  }
}

// REST API for Portal Guru & Dashboard
app.get('/api/health', (req, res) => {
  res.json({ status: 'ok', onlinePlayers: connectedPlayers.size });
});

app.get('/api/submissions', (req, res) => {
  const list = loadSubmissions();
  res.json({ ok: true, data: list });
});

app.post('/api/submissions', (req, res) => {
  const { studentName, studentId, mode, currentPos, quizScore, pahala, completed, details } = req.body;
  if (!studentName) {
    return res.status(400).json({ ok: false, error: 'Student name required' });
  }

  const list = loadSubmissions();
  const id = studentId || studentName.toLowerCase().replace(/[^a-z0-9]/g, '_');
  const now = new Date().toISOString();

  const existingIndex = list.findIndex(s => s.id === id || s.studentName.toLowerCase() === studentName.toLowerCase());
  const entry = {
    id,
    studentName,
    mode: mode || 'UMRAH',
    currentPos: currentPos || 1,
    quizScore: Number(quizScore) || 0,
    pahala: Number(pahala) || 0,
    completed: !!completed,
    details: details || [],
    lastUpdated: now,
  };

  if (existingIndex >= 0) {
    list[existingIndex] = { ...list[existingIndex], ...entry };
  } else {
    list.unshift(entry);
  }

  saveSubmissions(list);
  res.json({ ok: true, data: entry });
});

// Delete specific student result
app.delete('/api/submissions/:id', (req, res) => {
  const { id } = req.params;
  let list = loadSubmissions();
  list = list.filter(item => item.id !== id && item.studentName !== id);
  saveSubmissions(list);
  res.json({ ok: true, message: 'Deleted' });
});

// Clear all submissions
app.delete('/api/submissions', (req, res) => {
  saveSubmissions([]);
  res.json({ ok: true, message: 'All student submissions cleared' });
});

// ==========================================
// REAL-TIME MULTIPLAYER WEBSOCKET SERVER
// ==========================================
interface PlayerState {
  id: string;
  name: string;
  gender: string;
  mode: string;
  pos: number;
  x: number;
  y: number;
  z: number;
  rotationY: number;
  anim?: string;
  lastSeen: number;
}

const connectedPlayers = new Map<string, PlayerState>();
const socketToPlayerId = new Map<WebSocket, string>();

const wss = new WebSocketServer({ server, path: '/ws' });

function broadcast(msg: object, excludeWs?: WebSocket) {
  const raw = JSON.stringify(msg);
  wss.clients.forEach(client => {
    if (client.readyState === WebSocket.OPEN && client !== excludeWs) {
      try {
        client.send(raw);
      } catch (err) {}
    }
  });
}

wss.on('connection', (ws) => {
  ws.on('message', (data) => {
    try {
      const msg = JSON.parse(data.toString());

      if (msg.type === 'join') {
        const id = msg.id || 'player_' + Math.random().toString(36).substring(2, 9);
        const player: PlayerState = {
          id,
          name: msg.name || 'Santri',
          gender: msg.gender || 'L',
          mode: msg.mode || 'UMRAH',
          pos: msg.pos || 1,
          x: typeof msg.x === 'number' ? msg.x : -60,
          y: typeof msg.y === 'number' ? msg.y : 0.5,
          z: typeof msg.z === 'number' ? msg.z : 50,
          rotationY: typeof msg.rotationY === 'number' ? msg.rotationY : 0,
          anim: 'idle',
          lastSeen: Date.now()
        };

        connectedPlayers.set(id, player);
        socketToPlayerId.set(ws, id);

        // Send self state and list of all currently active players
        ws.send(JSON.stringify({
          type: 'init',
          yourId: id,
          players: Array.from(connectedPlayers.values())
        }));

        // Broadcast to other players that new student joined
        broadcast({
          type: 'player:joined',
          player
        }, ws);
      }

      else if (msg.type === 'move') {
        const id = socketToPlayerId.get(ws) || msg.id;
        if (!id) return;
        const p = connectedPlayers.get(id);
        if (p) {
          p.x = msg.x;
          p.y = msg.y;
          p.z = msg.z;
          p.rotationY = msg.rotationY;
          p.anim = msg.anim || 'idle';
          if (msg.pos) p.pos = msg.pos;
          p.lastSeen = Date.now();

          broadcast({
            type: 'player:moved',
            id,
            x: p.x,
            y: p.y,
            z: p.z,
            rotationY: p.rotationY,
            anim: p.anim,
            pos: p.pos
          }, ws);
        }
      }

      else if (msg.type === 'update_profile') {
        const id = socketToPlayerId.get(ws) || msg.id;
        if (!id) return;
        const p = connectedPlayers.get(id);
        if (p) {
          if (msg.name) p.name = msg.name;
          if (msg.gender) p.gender = msg.gender;
          if (msg.pos) p.pos = msg.pos;
          if (msg.mode) p.mode = msg.mode;
          p.lastSeen = Date.now();

          broadcast({
            type: 'player:updated',
            player: p
          });
        }
      }

      else if (msg.type === 'throw_pebble') {
        const id = socketToPlayerId.get(ws) || msg.id;
        if (!id) return;
        broadcast({
          type: 'player:threw_pebble',
          id,
          pillarKey: msg.pillarKey || 'AQABAH'
        }, ws);
      }

      else if (msg.type === 'chat') {
        const id = socketToPlayerId.get(ws) || msg.id;
        broadcast({
          type: 'chat',
          id,
          name: msg.name || 'Santri',
          text: msg.text || '',
          x: msg.x,
          y: msg.y,
          z: msg.z
        }, ws);
      }

      else if (msg.type === 'ping') {
        const id = socketToPlayerId.get(ws);
        if (id && connectedPlayers.has(id)) {
          connectedPlayers.get(id)!.lastSeen = Date.now();
        }
        ws.send(JSON.stringify({ type: 'pong' }));
      }
    } catch (err) {
      console.error('WS Error:', err);
    }
  });

  ws.on('close', () => {
    const id = socketToPlayerId.get(ws);
    if (id) {
      connectedPlayers.delete(id);
      socketToPlayerId.delete(ws);
      broadcast({ type: 'player:left', id });
    }
  });
});

// Periodic cleanup of stale players (inactive > 45s)
setInterval(() => {
  const now = Date.now();
  for (const [id, player] of connectedPlayers.entries()) {
    if (now - player.lastSeen > 45000) {
      connectedPlayers.delete(id);
      broadcast({ type: 'player:left', id });
    }
  }
}, 10000);

// Setup Vite middleware in dev or static serving in prod
async function startServer() {
  if (process.env.NODE_ENV === 'production' && fs.existsSync(path.join(__dirname, 'dist'))) {
    app.use(express.static(path.join(__dirname, 'dist')));
    app.get('*', (req, res) => {
      res.sendFile(path.join(__dirname, 'dist', 'index.html'));
    });
  } else {
    const { createServer: createViteServer } = await import('vite');
    const vite = await createViteServer({
      server: { middlewareMode: true, hmr: false },
      appType: 'spa',
    });
    app.use(vite.middlewares);
  }

  server.listen(Number(PORT), '0.0.0.0', () => {
    console.log(`Server listening on http://0.0.0.0:${PORT}`);
  });
}

startServer();
