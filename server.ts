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
  roomId: string;
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
const socketToRoomId = new Map<WebSocket, string>();

const wss = new WebSocketServer({ server, path: '/ws' });

function getRoomPlayers(roomId: string): PlayerState[] {
  const normRoom = (roomId || 'SDN-TUMBRASANOM').trim().toUpperCase();
  return Array.from(connectedPlayers.values()).filter(p => (p.roomId || 'SDN-TUMBRASANOM') === normRoom);
}

function broadcast(msg: object, excludeWs?: WebSocket, targetRoomId?: string) {
  const raw = JSON.stringify(msg);
  const normTargetRoom = targetRoomId ? targetRoomId.trim().toUpperCase() : null;

  wss.clients.forEach(client => {
    if (client.readyState === WebSocket.OPEN && client !== excludeWs) {
      if (normTargetRoom) {
        const clientRoom = (socketToRoomId.get(client) || 'SDN-TUMBRASANOM').trim().toUpperCase();
        if (clientRoom !== normTargetRoom) return;
      }
      try {
        client.send(raw);
      } catch (err) {}
    }
  });
}

function pruneInactivePlayers(maxAgeMs = 35000) {
  const now = Date.now();
  for (const [id, player] of connectedPlayers.entries()) {
    if (now - player.lastSeen > maxAgeMs) {
      connectedPlayers.delete(id);
      const room = player.roomId || 'SDN-TUMBRASANOM';
      const remainingCount = getRoomPlayers(room).length;
      broadcast({ type: 'player:left', id, roomId: room, onlineCount: remainingCount }, undefined, room);
    }
  }
}

wss.on('connection', (ws) => {
  ws.on('message', (data) => {
    try {
      const msg = JSON.parse(data.toString());

      if (msg.type === 'join') {
        const id = msg.id || 'player_' + Math.random().toString(36).substring(2, 9);
        const roomId = (msg.roomId || 'SDN-TUMBRASANOM').trim().toUpperCase();
        const rotY = typeof msg.rotationY === 'number' ? msg.rotationY : (typeof msg.rotY === 'number' ? msg.rotY : 0);

        // Prune any stale players before adding
        pruneInactivePlayers(30000);

        const player: PlayerState = {
          id,
          roomId,
          name: msg.name || 'Santri',
          gender: msg.gender || 'L',
          mode: msg.mode || 'UMRAH',
          pos: msg.pos || 1,
          x: typeof msg.x === 'number' ? msg.x : -60,
          y: typeof msg.y === 'number' ? msg.y : 0.5,
          z: typeof msg.z === 'number' ? msg.z : 50,
          rotationY: rotY,
          anim: 'idle',
          lastSeen: Date.now()
        };

        connectedPlayers.set(id, player);
        socketToPlayerId.set(ws, id);
        socketToRoomId.set(ws, roomId);

        const roomPlayers = getRoomPlayers(roomId);

        // Send self state and list of all currently active players in this specific room
        ws.send(JSON.stringify({
          type: 'init',
          yourId: id,
          roomId,
          onlineCount: roomPlayers.length,
          players: roomPlayers
        }));

        // Broadcast to other players in the same room that new student joined
        broadcast({
          type: 'player:joined',
          roomId,
          onlineCount: roomPlayers.length,
          player
        }, ws, roomId);
      }

      else if (msg.type === 'move') {
        const id = socketToPlayerId.get(ws) || msg.id;
        if (!id) return;
        const p = connectedPlayers.get(id);
        if (p) {
          if (typeof msg.x === 'number') p.x = msg.x;
          if (typeof msg.y === 'number') p.y = msg.y;
          if (typeof msg.z === 'number') p.z = msg.z;
          const rotY = typeof msg.rotationY === 'number' ? msg.rotationY : (typeof msg.rotY === 'number' ? msg.rotY : p.rotationY);
          if (typeof rotY === 'number' && !isNaN(rotY)) {
            p.rotationY = rotY;
          }
          p.anim = msg.anim || (msg.isMoving ? 'walk' : 'idle');
          if (typeof msg.isMoving === 'boolean') (p as any).isMoving = msg.isMoving;
          if (msg.pos) p.pos = msg.pos;
          if (msg.name) p.name = msg.name;
          if (msg.gender) p.gender = msg.gender;
          p.lastSeen = Date.now();

          const room = p.roomId || 'SDN-TUMBRASANOM';
          broadcast({
            type: 'player:moved',
            id,
            roomId: room,
            name: p.name,
            gender: p.gender,
            pos: p.pos,
            x: p.x,
            y: p.y,
            z: p.z,
            rotationY: p.rotationY,
            rotY: p.rotationY,
            isMoving: !!(p as any).isMoving,
            anim: p.anim
          }, ws, room);
        }
      }

      else if (msg.type === 'update_profile') {
        const id = socketToPlayerId.get(ws) || msg.id;
        if (!id) return;
        const p = connectedPlayers.get(id);
        if (p) {
          const oldRoom = p.roomId || 'SDN-TUMBRASANOM';
          const newRoom = (msg.roomId ? msg.roomId.trim().toUpperCase() : oldRoom);

          if (msg.name) p.name = msg.name;
          if (msg.gender) p.gender = msg.gender;
          if (msg.pos) p.pos = msg.pos;
          if (msg.mode) p.mode = msg.mode;
          p.lastSeen = Date.now();

          // Room switch handling
          if (newRoom !== oldRoom) {
            p.roomId = newRoom;
            socketToRoomId.set(ws, newRoom);

            // Notify old room that player left
            const oldRoomPlayers = getRoomPlayers(oldRoom);
            broadcast({
              type: 'player:left',
              id,
              roomId: oldRoom,
              onlineCount: oldRoomPlayers.length
            }, ws, oldRoom);

            // Send full player list of new room to this player
            const newRoomPlayers = getRoomPlayers(newRoom);
            ws.send(JSON.stringify({
              type: 'init',
              yourId: id,
              roomId: newRoom,
              onlineCount: newRoomPlayers.length,
              players: newRoomPlayers
            }));

            // Notify new room that player joined
            broadcast({
              type: 'player:joined',
              roomId: newRoom,
              onlineCount: newRoomPlayers.length,
              player: p
            }, ws, newRoom);
          } else {
            const roomPlayers = getRoomPlayers(newRoom);
            broadcast({
              type: 'player:updated',
              roomId: newRoom,
              onlineCount: roomPlayers.length,
              player: p
            }, undefined, newRoom);
          }
        }
      }

      else if (msg.type === 'throw_pebble') {
        const id = socketToPlayerId.get(ws) || msg.id;
        if (!id) return;
        const p = connectedPlayers.get(id);
        const room = p ? p.roomId : (socketToRoomId.get(ws) || 'SDN-TUMBRASANOM');
        broadcast({
          type: 'player:threw_pebble',
          id,
          roomId: room,
          pillarKey: msg.pillarKey || 'AQABAH',
          x: msg.x,
          y: msg.y,
          z: msg.z
        }, ws, room);
      }

      else if (msg.type === 'chat') {
        const id = socketToPlayerId.get(ws) || msg.id;
        const p = id ? connectedPlayers.get(id) : null;
        const room = p ? p.roomId : (socketToRoomId.get(ws) || 'SDN-TUMBRASANOM');
        broadcast({
          type: 'chat',
          id: id || 'system',
          roomId: room,
          name: msg.name || (p ? p.name : 'Santri'),
          text: msg.text || '',
          x: msg.x,
          y: msg.y,
          z: msg.z
        }, ws, room);
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
      const p = connectedPlayers.get(id);
      const room = p ? p.roomId : (socketToRoomId.get(ws) || 'SDN-TUMBRASANOM');
      connectedPlayers.delete(id);
      socketToPlayerId.delete(ws);
      socketToRoomId.delete(ws);
      const remainingCount = getRoomPlayers(room).length;
      broadcast({ type: 'player:left', id, roomId: room, onlineCount: remainingCount }, undefined, room);
    }
  });
});

// Periodic cleanup of stale players (inactive > 35s)
setInterval(() => {
  pruneInactivePlayers(35000);
}, 8000);

// Setup Vite middleware in dev or static serving in prod
// Ganti seluruh fungsi startServer() yang lama dengan yang ini:
async function startServer() {
  // Render akan menjalankan server langsung tanpa perlu Vite
  server.listen(Number(PORT), '0.0.0.0', () => {
    console.log(`Server backend berjalan di port ${PORT}`);
  });
}

startServer();
